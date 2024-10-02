import { React, useState } from 'react';
import { Navigate, useNavigate } from 'react-router-dom';
import axios from 'axios';

// import css
import '../App.css';
import '../Form.css';

import Visibility from '@mui/icons-material/Visibility';
import VisibilityOff from '@mui/icons-material/VisibilityOff';
import { Login } from '@mui/icons-material';


export function LoginPage({login}) {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const navigate = useNavigate();
    
    const handleSubmit = async (event) => {
        event.preventDefault();
        const user = { username, password };
        try {
            // const response = await axios.post('http://127.0.0.1:5000/login', user);
            let response ={data:{  //store response in localStorage
                token: "dummy",
                username: "dummy",
                email: "hi@gmail",
            }}; //dummy obj until user side db settled
            console.log(response.data)
            localStorage.setItem("access_token", response.data.token);
            localStorage.setItem("username", response.data.username);
            setUsername(response.data.username);
            localStorage.setItem("email", response.data.email);
            console.log(username,password);
            login();
            alert("Login successful");
            navigate('/home'); // Redirect to home page
            // setAuth(true)
        } catch (error) {
            alert("Login unsuccessful. Please try again.");
        }
    };

    return (
    <div className="box"> 
        <div className="user-form">
            <p className="outfit-font">Welcome Back!</p>
            <p className="outfit-font2">It's terrific to see you again.</p>
            <form method="POST" name="login_form" onSubmit={handleSubmit}>
                <div className='input-group'>
                    <div className='input-field'>
                        <input 
                            type='text'
                            name='username'
                            required
                            value={username}
                            onChange={(event) => { setUsername(event.target.value) }}
                            className='login-text-field'
                            placeholder='Username'
                            autoComplete="off" />
                    </div>
                    <div className='input-field'>
                        <input
                            type = 'password'
                            name='password'
                            required
                            className='login-text-field'
                            value={password}
                            onChange={(event) => { setPassword(event.target.value) }}
                            placeholder='Password'
                            autoComplete="off" />
                        <div className='visibility-btn' onClick={() => console.log(username,password)}>
                    
                        </div>
                    </div>
                </div>
            
            <div className='login-btn-location'>
                    <input className='login-btn' type='submit' value="Let's Go!" />
                </div>
            </form>

            <div className='register-link'>
                <a href='./register'>First time? Sign up here</a>
            </div>
        </div>
    </div>  

        );
};

export default LoginPage;