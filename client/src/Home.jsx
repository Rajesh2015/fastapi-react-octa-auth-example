import { useOktaAuth } from '@okta/okta-react';
import React, { useState, useEffect } from 'react';
import { Button,Header} from 'semantic-ui-react';

const SERVER = 'http://localhost:4000/latest/fruits';


const Home = () => {
  const { authState, oktaAuth } = useOktaAuth();
  const [userInfo, setUserInfo] = useState(null);
  const [token, setToken] = useState(null);
  const { fetchNewItems, setFetchNewItems } = useState(null);
  const [error, setError] = useState(null);
  const [items, setItems] = useState([]);

  const ItemList = (props) => {
    return (
      <ul>
        {props.items.map(item => (
          <li key={item.name}>
            {item.name}: {item.price}
          </li>
        ))}
      </ul>
    )
  }
  
  
  useEffect(() => {
    if (!authState.isAuthenticated) {
      // When user isn't authenticated, forget any user info
      setToken(null);
      setUserInfo(null);
    } else {
      setToken(oktaAuth.getAccessToken());
      oktaAuth.getUser().then((info) => {
        setUserInfo(info);
      });
    }
  }, [authState, oktaAuth]); // Update if authState changes

  useEffect(async () => {
    if (token) {
      const headers = { Authorization: `Bearer ${token}` };
      try {
        const res = await fetch(SERVER, { headers });
        if (res.status === 200) {
          const data = await res.json();
          console.log(data)
          setItems(data.items);
        } else {
          console.error(res.status, res.detail);
          setItems([]);
          setError(res.status)
        }
      } catch (e) {
        console.error(e);
        setError(`Error when calling ${SERVER}`);
      }
    }
  }, [token,fetchNewItems]);




  const login = async () => {
    oktaAuth.signInWithRedirect();
  };

  if (authState.isPending) {
    return (
      <div>Loading...</div>
    );
  }

  return (
    <div>
      <div>
        <Header as="h1">Fruit Demo</Header>

        { authState.isAuthenticated && !userInfo
        && <div>Loading...</div>}

        {authState.isAuthenticated && userInfo
        && (
        <div>
          <p>
            Welcome back,&nbsp;
            {userInfo.name}
            !
          </p>
          <div>
          <div>
            <label>Fruits:</label>
            <ItemList items={items} />
          </div>
          <br />
        </div>
        </div>
        
        )}




        {!authState.isAuthenticated
        && (
        <div>
          <Button id="login-button" primary onClick={login}>Login</Button>
        </div>
        )}

      </div>
    </div>
  );
};
export default Home;
