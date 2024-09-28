import { Typography, Button, Drawer, List, ListItem, ListItemIcon, ListItemText, Box, Toolbar } from '@mui/material';
import { useNavigate } from 'react-router-dom';
import { Schedule, Group, Assignment, Description, Person, ExitToApp, Margin  } from '@mui/icons-material';

const Sidebar = ({ logout }) => {

    const navigate = useNavigate();

    const handleLogout = () => {
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