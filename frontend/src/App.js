// import logo from './logo.svg';
import './App.css';

import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
// import ProtectedRoutes from './components/ProtectedRoutes';

import { LoginPage } from './pages/Login';

function App() {
  return (
    <Router>
      <div>
        <Routes>
          <Route path="/login" element={<LoginPage />} />
        
        </Routes>
      </div>
    </Router>
  );
}

export default App;
