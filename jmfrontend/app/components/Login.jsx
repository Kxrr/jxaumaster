import React from 'react';
import {stringify} from 'qs';
import axios from 'axios';


export default class Login extends React.Component {
    constructor(props) {
        super(props);

        this.state = {'username': '', 'password': '', 'online': false, 'user': {}};

        this.handleUsernameInput = this.handleUsernameInput.bind(this);
        this.handlePasswordInput = this.handlePasswordInput.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
    }

    isValid(s) {
        return true;

    };

    responseSuccess(rsp) {
        return (rsp.status === 200 && !rsp.data.error)
    }

    processLogin(rsp) {
        console.log(rsp);
        if (this.responseSuccess(rsp)) {
            this.setState({'online': true, 'user': rsp.data.user});
        }
    }

    requestLogin(username, password) {
        axios.post('/login', stringify({'username': username.toString(), 'password': password.toString()}))
            .then((rsp) => (this.processLogin(rsp)))
            .catch((e) => (alert('error')))
    }

    handleUsernameInput(event) {
        this.setState({'username': event.target.value});
    }

    handlePasswordInput(event) {
        this.setState({'password': event.target.value});
    }

    handleSubmit(event) {
        let {username, password} = this.state;

        if (this.isValid(username) && this.isValid(password)) {
            this.requestLogin(username, password);
        } else {

        }
    }

    render() {
        return (
            <div>
                <div className="login-form">
                    Username:
                    <input type="text" value={this.state.username} onChange={this.handleUsernameInput}/>
                    Password:
                    <input type="text" value={this.state.password} onChange={this.handlePasswordInput}/>

                    <input type="submit" onClick={this.handleSubmit}/>
                </div>
                <div className="welcome">Hello, {this.state.user.name}</div>
            </div>
        )
    }
}
