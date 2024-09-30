import { React, useState } from 'react';
import { Navigate, useNavigate } from 'react-router-dom';
import datejs from 'datejs';

// import css
import '../App.css';
import '../Form.css';

import { Typography ,Box} from '@mui/material';
import InputLabel from '@mui/material/InputLabel';
import MenuItem from '@mui/material/MenuItem';
import FormControl from '@mui/material/FormControl';
import Select from '@mui/material/Select';
import Grid from '@mui/material/Grid2';
import TextField from '@mui/material/TextField';
import { CalendarComponent } from '@syncfusion/ej2-react-calendars';
import Sidebar from '../components/Sidebar';

export function ApplyArrangementsPage ({ logout }) {

    const [type, setType] = useState('');

    const disabledDate = (args) => {
        let today = Date.today() ;
        if (args.date < today) {
            /*set 'true' to disable the weekends*/
            args.isDisabled = true;
        }
    };

    const handleTypeChange = (event) => {
        setType(event.target.value);
        console.log(type);
    };

    const [selectedValues, setSelectedValues] = useState([]);

    const onchange = (args) => {
        if (args) {
            setSelectedValues(args.values);
            console.log(selectedValues);
        }
    };
    
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
            <div className='application-form' >
                <Box component="form"
                            sx={{ '& .MuiTextField-root': { m: 1, width: '25ch' } }}
                            noValidate
                            autoComplete="off">
                <div className="reason" style={{flexDirection: 'row',display: 'flex',alignItems: 'center'}}>
                   <span>Reason:</span> <TextField
                        required
                        id="outlined-required"
                        label="Required"
                        defaultValue="eg. Pet appointment"
                        />
                </div>
                <div className="arrange-type" style={{width:'50%',flexDirection: 'row',display: 'flex',alignItems: 'center'}}>
                   <span>Arrangement type: </span> 
                   <div style={{width:'50%'}}> 
                    <FormControl fullWidth>
                        <InputLabel id="demo-simple-select-label">Type</InputLabel>
                            <Select
                              labelId="select-label"
                              id="arrangement-select"
                              value={type}
                              label="Age"
                              onChange={handleTypeChange}
                            >
                              <MenuItem value={'ML'}>ML</MenuItem>
                              <MenuItem value={'AL'}>AL</MenuItem>
                              <MenuItem value={'full'}>full-day</MenuItem>
                            </Select>
                        </FormControl>
                      </div>
                      
                </div>
                <div className="date-select" >
                   <span >Date(s):</span> 
                   <CalendarComponent id="calendar" renderDayCell={disabledDate} isMultiSelection={true} values={selectedValues} change={onchange.bind(this)} created={onchange.bind(this)}></CalendarComponent>
                    
                </div>
                

                </Box>
            </div>
            


            <script type="text/javascript" src="date.js"></script>
            <link href="https://cdn.syncfusion.com/ej2/material.css" rel="stylesheet" type="text/css"/>
        </Box>
      </Box>
      
        )
};

export default ApplyArrangementsPage;