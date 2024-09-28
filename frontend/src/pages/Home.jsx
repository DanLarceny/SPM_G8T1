import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Typography, Button, Drawer, List, ListItem, ListItemIcon, ListItemText, Box, Toolbar } from '@mui/material';
import { Schedule, Group, Assignment, Description, Person, ExitToApp, Margin  } from '@mui/icons-material';
import Grid from '@mui/material/Grid2';
import { Visibility, VisibilityOff } from '@mui/icons-material';
import Calendar from '../components/Calendar';
import axios from 'axios';
import Sidebar from '../components/Sidebar';


export function HomePage({ logout }) {
    const navigate = useNavigate();

    const handleLogout = async () => {
      await axios.post('/api/logout'); // Send a request to the logout endpoint
      localStorage.removeItem('token'); // Clear the token from local storage
      logout(); // Clear authentication state
      navigate('/login'); // Redirect to login page
    };

    const handleNavigation = (route) => {
      navigate(route);
    };

    return (
      <Box sx={{ display: 'flex' }}>
        {/* Sidebar Drawer */}
        <Sidebar logout = {logout}></Sidebar>
        
        {/* Main Content */}
        <Box component="main" sx={{ flexGrow: 1, p: 3 }}>
          <Grid container spacing={4} className="homepage-container">
            <Grid item xs={12}>
              <Typography variant="h4" className='outfit-font' component="p">
                Welcome! 
                {/* can match login username with db and retrieve name */}
              </Typography>
            </Grid>
            {/* You can include any additional content here based on the page you are on */}
            
          </Grid>
          <Calendar ></Calendar>
          
        </Box>
      </Box>
    );
};

export default HomePage;