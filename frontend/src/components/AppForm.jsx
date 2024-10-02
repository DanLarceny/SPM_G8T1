import { React, useState } from 'react';

import { Typography ,Box, Button} from '@mui/material';
import InputLabel from '@mui/material/InputLabel';
import MenuItem from '@mui/material/MenuItem';
import FormControl from '@mui/material/FormControl';
import Select from '@mui/material/Select';
import Grid from '@mui/material/Grid2';
import TextField from '@mui/material/TextField';
import { CalendarComponent } from '@syncfusion/ej2-react-calendars';

import '../Form.css';

const AppForm = () =>{

    const [username, setUsername] = useState(() => localStorage.getItem('username') || '');
    const [staffId, setStaffId] = useState(() => localStorage.getItem('username') || 'dummy01');
    const [email, setEmail] = useState(() => localStorage.getItem('email') || 'dannytan@allinone.com');
    const [supervisor, setSupervisor] = useState(() => localStorage.getItem('supervisor') || 'super01');
    const [selectedValues, setSelectedValues] = useState([]);
    const [type, setType] = useState('');
    const [timeslot, setTimeslot] = useState('');
    const [reason, setReason] = useState('');

    const disabledDate = (args) => {
        let today = new Date();
        if (args.date < today) {
            args.isDisabled = true;
        }
    };

    const handleSubmit = (event) => {
        event.preventDefault();
        try {
            alert("Sent request");
            
            const application = { staffId, email, reason, type, selectedValues, supervisor };
            // const response = await axios.post('http://127.0.0.1:5000/createApplication', application);
            console.log(application);
        } catch (error) {
            console.error("Form submission failed", error);
            alert("form submission failed");
        }
    };



    const handleTimeslotChange = (e) => {
        e.preventDefault();
        setTimeslot(e.target.value);
    };

    const handleReasonChange = (event) => {
        setReason(event.target.value);
  };


    const onchange = (args) => {
        if (args) {
            setSelectedValues(args.values);
            console.log(args.values);
            if (args.values.length>1) {
                setType("Recurring");
            } 
            if (args.values.length===1) {
                setType("One-off");
            }
        }
    };

    return (
        <form onSubmit={(e) => handleSubmit(e)}  method="POST" className='application-form' >
            <div className="reason" style={{flexDirection: 'row',display: 'flex',alignItems: 'center',width:'50%'}}>
            <span>Reason:</span> 
            <TextField
                    required
                    value= {reason}
                    id="outlined-required"
                    label="Required"
                    onChange={handleReasonChange}
                    defaultValue="eg. Pet appointment"
                    style ={{margin:'10px'}}
                    />
            </div>
            <div className="arrange-type" style={{width:'50%',flexDirection: 'row',display: 'flex',alignItems: 'center'}}>
            
                <label for="arrangement-select">Arrangement type:</label>
                    <select
                    id="arrangement-select"
                    value={timeslot}
                    style ={{margin:'10px'}}
                    label="type"
                    onChange={handleTimeslotChange}
                    >
                    <option value={'ML'}>ML</option>
                    <option  value={'AL'}>AL</option>
                    <option value={"full"}>Full-day</option>
                    </select>
            </div>
            <div className="date-select" >
            <span >Date(s):</span> 
            <CalendarComponent id="calendar" renderDayCell={disabledDate} isMultiSelection={true} values={selectedValues} change={onchange.bind(this)} created={onchange.bind(this)}></CalendarComponent>  
            </div>
        
            <input className='form-submit' type="submit" value = 'submit' style = {{margin: "5px"}} />
       

        
        </form>
    );
}
export default AppForm;