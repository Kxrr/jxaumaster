import React from 'react';
import ReactDOM from 'react-dom';
import App from './components/App';
import LoginScreen from './components/LoginScreen';


ReactDOM.render(
    <div>
      <App />
      <LoginScreen />
    </div>
    , document.body.appendChild(document.createElement('div'))
);
