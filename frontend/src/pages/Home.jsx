import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';


export function HomePage({ logout }) {
    const navigate = useNavigate();

    const handleLogout = () => {
      logout(); // Clear authentication state
      navigate('/login'); // Redirect to login page
    };

    return (
    <div>
        <h1>Welcome to the Home Page</h1>
        <button onClick={handleLogout}>Log Out</button>
    </div>
    );
}