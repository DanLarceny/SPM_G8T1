// import logo from './logo.svg';
import './App.css';

import React, { useState } from 'react';
import { BrowserRouter as Router, Route, Routes, Navigate } from 'react-router-dom';
// import ProtectedRoutes from './components/ProtectedRoutes';

import { LoginPage } from './pages/Login';
import  RegisterPage  from './pages/Register';
import { HomePage } from './pages/Home';
import UserPage from './pages/User';

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  const login = () => {
    setIsAuthenticated(true);
  }

  const logout = () => {
    setIsAuthenticated(false);
  }

  return (
    <Router>
      <div>
        <Routes>
        <Route path="/user" element={<UserPage />} />
        <Route path="/" element={<Navigate to="/login" />} />
        <Route path="/login" element={ 
          isAuthenticated ? <Navigate to ="/home" /> :  <LoginPage login = {login}/>}/>
        <Route path="/register" element={<RegisterPage />} />
        <Route path="/home" element = {
          isAuthenticated ? <HomePage logout={logout} /> : <Navigate to="/login" />
          }>
          </Route>
        
        </Routes>
      </div>
    </Router>
  );
}

export default App;
