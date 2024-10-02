import { React, useState } from 'react';
import { Navigate, useNavigate } from 'react-router-dom';

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

// import css
import '../App.css';
import '../Form.css';
import ArrangementListObject from '../components/ArrangementListObject';

export function ArrangementDetailsPage (logout) {

    return(
    <Box sx={{ display: 'flex' }}>
        {/* Sidebar Drawer */}
        <Sidebar logout = {logout}></Sidebar>
        
        {/* Main Content */}
        <Box component="main" sx={{ flexGrow: 1, p: 3 }}>
          <Grid container spacing={4} className="homepage-container">
            <Grid item xs={12}>
              <Typography variant="h4" className='outfit-font' component="p">
                See the status of your arrangements
              </Typography>
            </Grid>
            {/* You can include any additional content here based on the page you are on */}
          </Grid>
          <ArrangementListObject></ArrangementListObject>
          

            <script type="text/javascript" src="date.js"></script>
            <link href="https://cdn.syncfusion.com/ej2/material.css" rel="stylesheet" type="text/css"/>
        </Box>
      </Box>
      
    
    )
};

export default ArrangementDetailsPage;