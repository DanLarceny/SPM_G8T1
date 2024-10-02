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
import ArrangementListObject from '../components/ArrangementTableObject';

export function ArrangementDetailsPage (logout) {

  function createData(applicationId, date, type, reason, status) {
    return { applicationId, date, type, reason, status };
  }
  
  const rowObjects = [
    createData(1, [new Date(2024,9,2)], "AL", "Headache", "Pending"),
    createData(2, [new Date(2024,9,3), new Date(2024,9,10)],"Full-day", "childcare", "Pending"),
    createData(3, [new Date(2024,9,4)], "ML", "Goldfish funeral",  "Pending"),
    createData(4, [new Date(2024,9,5)], "AL","Headache", "Pending"),
  ];

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
          <ArrangementListObject rows={rowObjects}></ArrangementListObject>
          

            <script type="text/javascript" src="date.js"></script>
            <link href="https://cdn.syncfusion.com/ej2/material.css" rel="stylesheet" type="text/css"/>
        </Box>
      </Box>
      
    
    )
};

export default ArrangementDetailsPage;