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
    const [file, setFile] = useState(null);
    const [selectedValues, setSelectedValues] = useState([]);
    const [type, setType] = useState('');
    const [timeslot, setTimeslot] = useState('');
    const [reason, setReason] = useState('');

    const addDays = (date, days) => {
        const newDate = new Date(date);
        newDate.setDate(date.getDate() + days);
        return newDate;
    };

    const disabledDate = (args) => {
        let today = new Date();
        if (args.date < today) {
            args.isDisabled = true;
        }
        if (args.date > addDays(today,365)) {
            args.isDisabled = true;
        }
        
    };

    const handleSubmit = (event) => {
        event.preventDefault();
        try {
            alert("Sent request");
            
            const application = { staffId, email, reason, type, selectedValues, supervisor,file };
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

    const handleFileChange = (event) => {
        const file = event.target.files[0];
        const reader = new FileReader();
        const base64String = reader.result;
        reader.readAsDataURL(file);
        reader.onloadend = () => {
            // const base64Data = base64String.split(',')[1]; // Extract only the Base64 data
            // console.log(base64Data);
            setFile(reader.result);
        };
        // reader.readAsDataURL(file);
        
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
            <label htmlFor="readonlyField">Approving supervisor: </label>
            <input 
                type="text" 
                id="readonlyField" 
                value={supervisor}
                disabled
            />
            <div className="arrange-type" style={{width:'50%',flexDirection: 'row',display: 'flex',alignItems: 'center'}}>
            
                <label for="arrangement-select">Arrangement type:</label>
                    <select
                    id="arrangement-select"
                    value={timeslot}
                    style ={{margin:'10px'}}
                    label="type"
                    onChange={handleTimeslotChange}
                    >
                    <option value={'ML'}>AM</option>
                    <option  value={'AL'}>PM</option>
                    <option value={"full"}>Full-day</option>
                    </select>
            </div>
            <div className="date-select" >
            <span >Date(s):</span> 
            <CalendarComponent 
                id="calendar" 
                renderDayCell={disabledDate} 
                isMultiSelection={true} values={selectedValues} 
                change={onchange.bind(this)} 
                created={onchange.bind(this)}>
            </CalendarComponent>  
            </div>
            <div>
            <label for="myfile">Select a file: </label>
            <input type="file" id="myfile" name="myfile" onChange = {handleFileChange} accept=".jpg,.jpeg" />
            </div>
            <div>
                <img src={file} alt="Uploaded" style={{ width: '200px', height: 'auto' }} />
            </div>
        
            <input className='form-submit' type="submit" value = 'submit' style = {{margin: "5px"}} />
       
        </form>

        
    );
}
export default AppForm;