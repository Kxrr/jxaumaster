import React from 'react';
import Login from './Login';


export default class App extends React.Component {
  constructor(props) {
    super(props);
  }

  render() {
    return (
        <div className="application">
            <Login />
        </div>
    );
  }

}
