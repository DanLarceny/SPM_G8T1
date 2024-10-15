import { React, useState, useEffect } from 'react';
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

export function ManageApplicationPage ({ logout }) {

  function createData(applicationId,name, startDate, endDate, period, type, days, reason, status, approvingSupervisor, dos) {
    return { applicationId,name, startDate, endDate, period, type, days, reason, status, approvingSupervisor, dos };
  }

  const rowObjects = [
    createData(1,'sam', new Date(2024,9,2), new Date(2024,9,2),"AL","Ad-hoc" ,[], "Headache", "Approved", "Super01", new Date),
    createData(2,'whitney', new Date(2024,9,3), new Date(2024,9,10),"Full-day","Recurring",['Monday','Tuesday',"Wednesday","Thursday","Friday"], "childcare", "Pending", "Super01", new Date),
    createData(3,'blake', new Date(2024,9,4), new Date(2024,9,4),"ML","Ad-hoc",[],  "Goldfish funeral",  "Pending", "Super01", new Date),
    createData(4,'alder', new Date(2024,9,5), new Date(2024,9,5),"AL","Ad-hoc",[], "Headache", "Pending", "Super01", new Date),
  ];

  const [rows, setRows] = useState(rowObjects);

  const onPageLoad = () => {
    if (localStorage.getItem('role') !== 'manager') {
        // If the user is not a manager, redirect to home page or previous page
        return <Navigate to="/" replace />;
    }
  };

  useEffect(() => {
    onPageLoad(); // Call the function when the component mounts

    // Optional: Return a cleanup function if necessary (e.g., for clearing intervals)
    return () => {
      console.log("Cleanup if necessary"); // Clean up actions when the component unmounts
    };
  }, []); // The 

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
                Manage applications of arrangements
              </Typography>
            </Grid>
            {/* You can include any additional content here based on the page you are on */}
          </Grid>
          <ArrangementListObject
           rows={rows}
           onUpdateStatus={updateRowStatus}
           mode={"leaveApproval"}
          //  onCancel={() => updateRowStatus(row.id, 'cancelled')}
           ></ArrangementListObject>
          

            <script type="text/javascript" src="date.js"></script>
            <link href="https://cdn.syncfusion.com/ej2/material.css" rel="stylesheet" type="text/css"/>
        </Box>
      </Box>
      
    
    )
};

export default ManageApplicationPage;