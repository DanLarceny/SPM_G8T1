import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

import Calendar from '../components/Calendar.jsx';
import Navbar from '../components/Navbar.jsx';



export function HomePage({ logout }) {
    const navigate = useNavigate();

    const handleLogout = () => {
      logout(); // Clear authentication state
      navigate('/login'); // Redirect to login page
    };

    return (
    <div>
        <h1>Welcome to the Home Page</h1>
        <Navbar></Navbar>
        <div>
          <Calendar></Calendar>
        </div>
        <button onClick={handleLogout}>Log Out</button>
    </div>
    );
}