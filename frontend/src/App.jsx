// import logo from './logo.svg';
import './App.css';

import React, { useState } from 'react';
import { BrowserRouter as Router, Route, Routes, Navigate } from 'react-router-dom';
// import ProtectedRoutes from './components/ProtectedRoutes';

import { LoginPage } from './pages/Login';
import  RegisterPage  from './pages/Register';
import { HomePage } from './pages/Home';
import { ProfilePage} from './pages/Profile';
import { PersonalSchedulePage} from './pages/PersonalSchedule';
import { TeamSchedulePage} from './pages/TeamSchedule';
import {ApplyArrangementsPage} from './pages/ApplyArrangements';
import {ArrangementDetailsPage} from './pages/Arrangements';


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
          <Route path="/" element={<Navigate to="/login" />} />
          <Route path="/register" element={<RegisterPage />} />
          <Route path="/login" element={ 
            isAuthenticated ? <Navigate to ="/home" /> :  <LoginPage login = {login}/>}/>
          <Route path="/home" element = {
            isAuthenticated ? <HomePage logout={logout} /> : <Navigate to="/login" />
            }/>
            {/* Will implement a Protected Route component that handles redirection back to login if user not logged in/already logged out */}
          <Route path="/profile" element={<ProfilePage />} />
          <Route path="/schedule" element={<PersonalSchedulePage />} />
          <Route path="/team-schedule" element={<TeamSchedulePage />} />
          <Route path="/apply-arrangements" element={<ApplyArrangementsPage />} />
          <Route path="/arrangement-details" element={<ArrangementDetailsPage />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
