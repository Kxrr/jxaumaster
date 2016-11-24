import React from 'react';
import {stringify} from 'qs';
import axios from 'axios';


function Welcome(props) {
    return <div>{`Hello, ${props.name}`}</div>

}


class Login extends React.Component {
    constructor(props) {
        super(props);

        this.state = {'username': '', 'password': '', 'online': false};

        this.handleUsernameInput = this.handleUsernameInput.bind(this);
        this.handlePasswordInput = this.handlePasswordInput.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
        this.handleLogout = this.handleLogout.bind(this);
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
            const user = rsp.data.user;
            this.setState({'online': true});
            this.props.afterLogin(user);  // 登录成功后通知上层组件
        }
    }

    requestLogin(username, password) {
        // axios.post('/login', stringify({'username': username.toString(), 'password': password.toString()}))
        //     .then((rsp) => (this.processLogin(rsp)))
        //     .catch((e) => (alert('error')))
        this.processLogin({status: 200, 'data': {'user': {'name': 'Roy'}}});
    }

    handleUsernameInput(event) {
        this.setState({'username': event.target.value});
    }

    handlePasswordInput(event) {
        this.setState({'password': event.target.value});
    }

    handleSubmit(event) {
        event.preventDefault();
        let {username, password} = this.state;

        if (this.isValid(username) && this.isValid(password)) {
            this.requestLogin(username, password);
        } else {

        }
    }

    requestLogout() {

    }

    handleLogout(event) {
        event.preventDefault();
        this.requestLogout();
        this.setState({'online': false});
        this.props.afterLogout();
    }

    render() {
        const _Login = <div>
            <form className="login-form" onSubmit={this.handleSubmit}>
                <label>Username:</label>
                <input type="text" value={this.state.username} onChange={this.handleUsernameInput}/>
                <label>Password:</label>
                <input type="text" value={this.state.password} onChange={this.handlePasswordInput}/>
                <input type="submit" value="Submit"/>

            </form>
        </div>;

        const _LoginOut = <button onClick={this.handleLogout}>Logout</button>;

        return (this.state.online ? _LoginOut : _Login)

    }
}


export default class LoginScreen extends React.Component {
    constructor(props) {
        super(props);
        this.state = {user: null};
        this.handleAfterLogin = this.handleAfterLogin.bind(this);
        this.handleAfterLogout = this.handleAfterLogout.bind(this);

    }

    handleAfterLogin(user) {
        this.setState({user});
    }

    handleAfterLogout() {
        this.setState({user: null});
    }

    render() {
        const user = this.state.user;
        return (
            <div>
                {user && <Welcome name={user.name}/>}
                <Login afterLogin={this.handleAfterLogin} afterLogout={this.handleAfterLogout}/>
            </div>
        )
    }

}
