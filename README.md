# Getting Started with Auth App

This project was bootstrapped with [Create React App](https://github.com/facebook/create-react-app).


## Prerequisites

- [Okta CLI][]
- Python 3.6 or later
- A recent version of [Node.js][].

[Okta blog]: https://developer.okta.com/blog/2021/06/23/okta-oso-fastapi-sqlalchemy
[Compare the two branches]: https://github.com/osohq/fastapi-sqlalchemy-okta-oso-example/compare/authorized
[Okta CLI]: https://github.com/okta/okta-cli
[Node.js]: https://nodejs.org/

## Available Scripts

In the project directory, you can run:

### `npm start`

Runs the app in the development mode.\
Open [http://localhost:8080](http://localhost:8080) to view it in your browser.

The page will reload when you make changes.\
You may also see any lint errors in the console.

### `npm test`

Launches the test runner in the interactive watch mode.\
See the section about [running tests](https://facebook.github.io/create-react-app/docs/running-tests) for more information.


### How to use Okta (If creating a differnt account )
- Install the Okta CLI and run okta register to sign up for a new account. If you already have an account, run okta login. Then, run okta apps create. Select the default app name, or change it as you see fit. Choose Single-Page App and press Enter.
- Enter your callback  and Logout Redirect URI.Default value set to http://localhost:8080/login/callback for the Redirect URI and Logout Redirect URI to http://localhost:8080

- Once your new Okta application is created, the Okta CLI will print out its Issuer and Client ID properties:

### How to run

First time ```docker-compose --build``` then ```docker-compose up``` 

