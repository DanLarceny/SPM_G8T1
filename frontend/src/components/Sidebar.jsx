import useState from 'react';
import { Typography, Button, Drawer, List, ListItem, ListItemIcon, ListItemText, Box, Toolbar } from '@mui/material';
import { useNavigate } from 'react-router-dom';
import { Schedule, Group, Assignment, Description, Person, ExitToApp, Margin  } from '@mui/icons-material';
import { styled } from '@mui/system';

const Sidebar = ({ logout }) => {

    const BlurredListItem = styled(ListItem)(({ theme }) => ({
      opacity: 0.5,                // Reduced opacity
      filter: 'grayscale(100%)',   // Grayscale effect to make it look blurred
      cursor: 'not-allowed',       // Change cursor to indicate non-clickable
      pointerEvents: 'none',       // Prevent interaction if necessary
    }));

    const navigate = useNavigate();
    const isManager = (localStorage.getItem("role") === 'manager');
    const isHR = (localStorage.getItem("role") === 'HR');

    const handleLogout = () => {
      localStorage.clear();
      logout(); // Clear authentication state
      navigate('/login'); // Redirect to login page
    };

    const handleNavigation = (route) => {
      navigate(route);
    };
    
    return (

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

            <ListItem button 
            disabled={!isManager} 
            onClick={() => {
              if (isManager) {
                handleNavigation('/manage-applications'); // Only navigate if condition is true
              } else {
                console.log('User does not have permission to navigate');
              }
            }}
            sx={{
              opacity: !isManager ? 0.5 : 1,                 // Reduced opacity when disabled
              filter: !isManager ? 'grayscale(100%)' : 'none', // Apply grayscale when disabled
              cursor: !isManager ? 'not-allowed' : 'pointer',  // Change cursor
            }}
          >
              <ListItemIcon>
                <Description />
              </ListItemIcon>
              <ListItemText primary="Approve/Reject requests" />
            </ListItem>
            <ListItem button 
            disabled={!isHR} 
            onClick={() => {
              if (isHR) {
                handleNavigation('/hr-schedule'); // Only navigate if condition is true
              } else {
                console.log('User does not have permission to navigate');
              }
            }}
            sx={{
              opacity: !isHR ? 0.5 : 1,                 // Reduced opacity when disabled
              filter: !isHR ? 'grayscale(100%)' : 'none', // Apply grayscale when disabled
              cursor: !isHR ? 'not-allowed' : 'pointer',  // Change cursor
            }}
          >
              <ListItemIcon>
                <Description />
              </ListItemIcon>
              <ListItemText primary="View all schedules" />
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
    );
}
export default Sidebar;