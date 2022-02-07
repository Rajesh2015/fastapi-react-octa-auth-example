import React from 'react';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import { OktaAuth } from '@okta/okta-auth-js';
import { Security, LoginCallback } from '@okta/okta-react';
import { Container } from 'semantic-ui-react';
import config from './config';
import Home from './Home';
import Navbar from './Navbar';

const oktaAuth = new OktaAuth(config.oidc);

const App = () => (
  <Router>
    <Security oktaAuth={oktaAuth}>
      <Navbar />
      <Container text style={{ marginTop: '7em' }}>
        <Switch>
          <Route path="/" exact component={Home} />
          <Route path="/callback" component={LoginCallback} />
        </Switch>
      </Container>
    </Security>
  </Router>
);
export default App;