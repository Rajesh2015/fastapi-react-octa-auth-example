import os
import json
import requests
from typing import Dict
from fastapi import FastAPI, Depends, Header, HTTPException,Request, APIRouter
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi_versioning import VersionedFastAPI, version
from okta_jwt.jwt import validate_token
from sqlalchemy.orm import Session
from .database import SessionLocal, engine
from starlette.config import Config
from . import models
from .models import FruitsModel
from .schemas import Fruits
from typing import List, Optional
from fastapi.security import OAuth2PasswordBearer
import httpx
from okta_jwt.jwt import validate_token as validate_locally


conf = Config(".env")
issuer, audience, client_id = conf("ISSUER"), conf("AUDIENCE"), conf("CLIENT_ID")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')


# Database migration, see https://fastapi.tiangolo.com/tutorial/sql-databases/
models.Base.metadata.create_all(bind=engine)


# Dependency for database session, see https://fastapi.tiangolo.com/tutorial/sql-databases/
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def retrieve_token(authorization, issuer, scope='items'):
    headers = {
        'accept': 'application/json',
        'authorization': authorization,
        'cache-control': 'no-cache',
        'content-type': 'application/x-www-form-urlencoded'
    }
    data = {
        'grant_type': 'client_credentials',
        'scope': scope,
    }
    url = issuer + '/v1/token'

    response = httpx.post(url, headers=headers, data=data)

    if response.status_code == httpx.codes.OK:
        return response.json()
    else:
        raise HTTPException(status_code=400, detail=response.text)


def get_token(authorization: Optional[str] = Header(None)) -> str:
    if not authorization:
        raise HTTPException(403, "Missing 'Authorization' header.")
    try:
        return authorization.split()[1]
    except IndexError:
        raise HTTPException(403, "Malformed 'Authorization' header.")

def validate(
    request: Request, token: str = Depends(get_token)):
    try:
        email = validate_locally(token, issuer, audience, client_id)["sub"]
    except Exception as e:
        try:
            validate_locally(token, issuer, audience, conf("OKTA_CLIENT_ID"))["sub"]
        except Exception as e:
            raise HTTPException(403, str(e))

# Fast API app, see https://fastapi.tiangolo.com/
app = FastAPI(dependencies=[Depends(get_token)])
root = APIRouter(tags=['root'])
app_route = APIRouter()


@root.get("/")
def read_root(request: Request):
    url_list = [
        route.path
        for route in request.app.routes
    ]

    app_router_list = [route.path
                       for route in app_route.routes]

    return {"endpoints": set(url_list+app_router_list)}


# Get auth token
@root.post('/token')
def login(request: Request):
    return retrieve_token(
        request.headers['authorization'],
        issuer,
         'items'
    )
@app_route.get('/foo')
@version(1)
def foo():
    return "foo V1"


@app_route.get('/foo')
@version(2)
def foo():
    return "foo V2"


@app_route.get('/fruits')
@version(1)
def get_fruits(valid: bool = Depends(validate),db: Session = Depends(get_db)):
    """Handle fruits (Postgres integration)"""
    seed(db)
    fruits = db.query(models.FruitsModel).all()
    results = [
        {
            "name": fruit.name,
            "price": fruit.price
        } for fruit in fruits]
    return JSONResponse({"items": results})


@app_route.post('/fruits')
@version(1)
def post_fruits(fruit: Fruits, db: Session = Depends(get_db)):
    new_fruit = FruitsModel(name=fruit.name, price=fruit.price)
    db.add(new_fruit)
    db.commit()
    return {"message": f"fruit {new_fruit.name} has been created successfully."}


@app_route.post('/predict')
@version(1)
def predict_response(request: Dict):
    """Execute a prediction."""
    try:
        data = json.dumps(request)
        headers = {'Content-type': 'application/json'}
        url = os.environ.get('MLFLOW_ENDPOINT')
        post_response = requests.post(url, data=data, headers=headers)
        return post_response.json()
    except Exception as exc:
        return JSONResponse(status_code=500, content={'error': 'Error calling model engine: ' + str(exc)})


# Versioned Fast API app, see https://github.com/DeanWay/fastapi-versioning
app.include_router(app_route)

app = VersionedFastAPI(app, enable_latest=True, version_format='{major}', prefix_format='/v{major}')
app.include_router(root)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


def seed(db: Session = Depends(get_db)):
    fruits = db.query(models.FruitsModel).all()
    if len(fruits) == 0:
        db.add(FruitsModel(name='Apples', price=1.2))
        db.add(FruitsModel(name='Oranges', price=3.4))
        db.commit()
