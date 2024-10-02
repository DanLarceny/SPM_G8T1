import { React, useState } from 'react';
import axios from 'axios';

// import css
import '../App.css';
import '../Form.css';

import { Typography ,Box, Button} from '@mui/material';
import InputLabel from '@mui/material/InputLabel';
import MenuItem from '@mui/material/MenuItem';
import FormControl from '@mui/material/FormControl';
import Select from '@mui/material/Select';
import Grid from '@mui/material/Grid2';
import TextField from '@mui/material/TextField';
import { CalendarComponent } from '@syncfusion/ej2-react-calendars';
import Sidebar from '../components/Sidebar';
import AppForm from '../components/AppForm';

export function ApplyArrangementsPage ({ logout }) {
  
    return (
        // <Typography variant="h4" className='outfit-font' component="p">
        //     Will work on this subsequently
        //     {/* can match login username with db and retrieve name */}
        // </Typography>

        <Box sx={{ display: 'flex' }}>
        {/* Sidebar Drawer */}
        <Sidebar logout = {logout}></Sidebar>
        
        {/* Main Content */}
        <Box component="main" sx={{ flexGrow: 1, p: 3 }}>
          <Grid container spacing={4} className="homepage-container">
            <Grid item xs={12}>
              <Typography variant="h4" className='outfit-font' component="p">
                Apply for an arrangement
                {/* can match login username with db and retrieve name */}
              </Typography>
            </Grid>
            {/* You can include any additional content here based on the page you are on */}
          </Grid>
          <AppForm></AppForm>

            <script type="text/javascript" src="date.js"></script>
            <link href="https://cdn.syncfusion.com/ej2/material.css" rel="stylesheet" type="text/css"/>
        </Box>
      </Box>
      
        )
};

export default ApplyArrangementsPage;