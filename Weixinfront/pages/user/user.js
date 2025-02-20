import React, { useState, useEffect } from 'react';
import axios from 'axios';

const UserPage = () => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [email, setEmail] = useState('');
    const [message, setMessage] = useState('');
    const [isLoggedIn, setIsLoggedIn] = useState(false);

    useEffect(() => {
        // 检查用户是否已经登录
        axios.get('/api/user/check_login')
            .then(response => {
                setIsLoggedIn(response.data.isLoggedIn);
            })
            .catch(error => {
                setIsLoggedIn(false);
            });
    }, []);

    const handleRegister = async () => {
        try {
            const response = await axios.post('/api/user/register', {
                username,
                password,
                email
            });
            setMessage(response.data.message);
            setUsername('');
            setPassword('');
            setEmail('');
        } catch (error) {
            setMessage(error.response.data.message);
        }
    };

    const handleLogin = async () => {
        try {
            const response = await axios.post('/api/user/login', {
                username,
                password
            });
            setMessage(response.data.message);
            setIsLoggedIn(true);
            setUsername('');
            setPassword('');
        } catch (error) {
            setMessage(error.response.data.message);
        }
    };

    const handleLogout = async () => {
        try {
            const response = await axios.post('/api/user/logout');
            setMessage(response.data.message);
            setIsLoggedIn(false);
        } catch (error) {
            setMessage(error.response.data.message);
        }
    };

    return (
        <div>
            <h1>User Management</h1>
            {isLoggedIn ? (
                <div>
                    <h2>Welcome, {username}!</h2>
                    <button onClick={handleLogout}>Logout</button>
                </div>
            ) : (
                <div>
                    <div>
                        <h2>Register</h2>
                        <input
                            type="text"
                            placeholder="Username"
                            value={username}
                            onChange={(e) => setUsername(e.target.value)}
                        />
                        <input
                            type="password"
                            placeholder="Password"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                        />
                        <input
                            type="email"
                            placeholder="Email"
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                        />
                        <button onClick={handleRegister}>Register</button>
                    </div>
                    <div>
                        <h2>Login</h2>
                        <input
                            type="text"
                            placeholder="Username"
                            value={username}
                            onChange={(e) => setUsername(e.target.value)}
                        />
                        <input
                            type="password"
                            placeholder="Password"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                        />
                        <button onClick={handleLogin}>Login</button>
                    </div>
                </div>
            )}
            <div>
                <p>{message}</p>
            </div>
        </div>
    );
};

export default UserPage;