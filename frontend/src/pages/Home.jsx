import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Typography, Button, Drawer, List, ListItem, ListItemIcon, ListItemText, Box, Toolbar } from '@mui/material';
import { Schedule, Group, Assignment, Description, Person, ExitToApp  } from '@mui/icons-material';
import Grid from '@mui/material/Grid2';
import { Visibility, VisibilityOff } from '@mui/icons-material';
import Calendar from '../components/Calendar';
import axios from 'axios';


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
        <Drawer
          variant="permanent"
          sx={{
            width: 200,
            flexShrink: 0,
            [`& .MuiDrawer-paper`]: { width: 240, boxSizing: 'border-box' },
          }}>;
        
        <Toolbar />
          <List>
            <ListItem button onClick={() => handleNavigation('/profile')}>
              <ListItemIcon>
                <Person />
              </ListItemIcon>
              <ListItemText primary="Profile" />
            </ListItem>
            
            <ListItem button onClick={() => handleNavigation('/schedule')}>
              <ListItemIcon>
                <Schedule />
              </ListItemIcon>
              <ListItemText primary="Your Schedule" />
            </ListItem>

            <ListItem button onClick={() => handleNavigation('/team-schedule')}>
              <ListItemIcon>
                <Group />
              </ListItemIcon>
              <ListItemText primary="Team Schedule" />
            </ListItem>

            <ListItem button onClick={() => handleNavigation('/apply-arrangements')}>
              <ListItemIcon>
                <Assignment />
              </ListItemIcon>
              <ListItemText primary="Apply for Arrangements" />
            </ListItem>

            <ListItem button onClick={() => handleNavigation('/arrangement-details')}>
              <ListItemIcon>
                <Description />
              </ListItemIcon>
              <ListItemText primary="Arrangement Details" />
            </ListItem>
          </List>

        {/* Logout Button at the Bottom */}
        <Box sx={{ flexGrow: 1 }} /> {/* This pushes the logout button to the bottom */}
          <Box sx={{ p: 2 }}>
            <Button
              variant="contained"
              color="secondary"
              startIcon={<ExitToApp />}
              fullWidth
              onClick={handleLogout}
            >
              Logout
            </Button>
          </Box>
        </Drawer>
        
        {/* Main Content */}
        <Box component="main" sx={{ flexGrow: 1, p: 3 }}>
          <Toolbar />
          <Grid container spacing={4} className="homepage-container">
            <Grid item xs={12}>
              <Typography variant="h4" className='outfit-font' component="p">
                Welcome! 
                {/* can match login username with db and retrieve name */}
              </Typography>
            </Grid>
            {/* You can include any additional content here based on the page you are on */}
            <Calendar pos={{marginTop: "5px"}}></Calendar>
          </Grid>
        </Box>
      </Box>
    );
};

export default HomePage;