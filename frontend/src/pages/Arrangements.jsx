import { React, useState, useEffect } from 'react';
import { Navigate, useNavigate } from 'react-router-dom';
import axios from 'axios';

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

export function ArrangementDetailsPage ({ logout }) {

  function createData(applicationId, startDate, endDate, period, type,days, reason, status, approvingSupervisor, dos) {
    return { applicationId, startDate, endDate, period, type,days, reason, status, approvingSupervisor, dos };
  }


  // const fetchAndCreateData = async (localStorage.getItem("staff_id")) => {
  //       try {
  //           // Make GET request to the endpoint, passing staffId as a parameter
  //           const response = await axios.get(http://localhost:3000/viewOwnSchedule', {
  //               params: { localStorage.getItem("staff_id") }
  //           });

  //           // Extract rows from the response data
  //           const rows = response.data; // Assuming response.data is an array of rows

  //           // Loop through each row and call the createData function
  //           const formattedRows = rows.map(row => createData(
  //               row.applicationId,
  //               new Date(row.Start_Date),
  //               new Date(row.End_Date),
  //               row.Time_Slot,
  //               row.Type,  #TODO make sure all rows match db/model side
  //               row.days,
  //               row.reason,
  //               row.Status,
  //               row.Reporting_Manager,
  //               row.dos
  //           ));

  //           // Update state with the formatted rows
  //           setRows(formattedRows);
  //       } catch (error) {
  //           console.error("Error fetching data:", error);
  //       }
  //   };

  // useEffect(() => {
  //     fetchAndCreateData(staffId);  // Pass staffId as argument
  // }, [staffId]);  // Runs when the staffId changes (or on initial load)

  const rowObjects = [
    createData(1, new Date(2024,9,2),new Date(2024,9,2),"AL","Ad-hoc" ,[], "Headache", "Approved", "Super01", new Date),
    createData(2, new Date(2024,9,3), new Date(2024,9,10),"Full-day","Recurring",['Mon','Tues'], "childcare", "Pending", "Super01", new Date),
    createData(3, new Date(2024,9,4),new Date(2024,9,4),"ML","Ad-hoc",[],  "Goldfish funeral",  "Pending", "Super01", new Date),
    createData(4, new Date(2024,9,5),new Date(2024,9,5),"AL","Ad-hoc",[], "Headache", "Pending", "Super01", new Date),
  ];

  const [rows, setRows] = useState(rowObjects);

  const updateRowStatus = (id, newStatus) => {
    setRows((prevRows) =>
      prevRows.map((row) =>
        row.applicationId === id ? { ...row, status: newStatus } : row
      )
    );
  };

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
          <ArrangementListObject
           rows={rows}
           onUpdateStatus={updateRowStatus}
           mode={"taskManagement"}
           ></ArrangementListObject>
          

            <script type="text/javascript" src="date.js"></script>
            <link href="https://cdn.syncfusion.com/ej2/material.css" rel="stylesheet" type="text/css"/>
        </Box>
      </Box>
      
    
    )
};

export default ArrangementDetailsPage;