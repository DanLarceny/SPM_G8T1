// import logo from './logo.svg';
import './App.css';

import React, { useState } from 'react';
import { BrowserRouter as Router, Route, Routes, Navigate } from 'react-router-dom';
// import ProtectedRoute from './components/ProtectedRoute';

import { LoginPage } from './pages/Login';
import  RegisterPage  from './pages/Register';
import { HomePage } from './pages/Home';
import { ProfilePage} from './pages/Profile';
import { PersonalSchedulePage} from './pages/PersonalSchedule';
import { TeamSchedulePage} from './pages/TeamSchedule';
import {ApplyArrangementsPage} from './pages/ApplyArrangements';
import {ArrangementDetailsPage} from './pages/Arrangements';
import {ManageApplicationPage} from './pages/ManageApplications';

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
       
          <Route path="/apply-arrangements" element={
            isAuthenticated ? <ApplyArrangementsPage logout={logout} />: <Navigate to="/login" />
            } />
          <Route path="/arrangement-details" element={
            isAuthenticated ? <ArrangementDetailsPage logout={logout} />: <Navigate to="/login" />
            } />
          <Route path="/manage-applications" element={
            isAuthenticated ? 
              <ManageApplicationPage logout={logout}/>
            : <Navigate to="/login" />
            } />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
