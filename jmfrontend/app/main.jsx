import React from 'react';
import ReactDOM from 'react-dom';
import App from './components/App';
import Login from './components/Login.jsx'

ReactDOM.render(
    <div>
      <App />
      <Login />
    </div>
    , document.body.appendChild(document.createElement('div'))
);
