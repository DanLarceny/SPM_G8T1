import { React, useState } from 'react';
import axios from 'axios';
import { format } from 'date-fns';

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

    const [staffId, setStaffId] = useState(() => localStorage.getItem('username') || 'dummy01');
    const [email, setEmail] = useState(() => localStorage.getItem('email') || 'dannytan@allinone.com');
    const [supervisor, setSupervisor] = useState(() => localStorage.getItem('supervisor') || 'super01');
    const [file, setFile] = useState(null);
    const [selectedValue1, setSelectedValue1] = useState(null);
    const [selectedValue2, setSelectedValue2] = useState(null);
    const [type, setType] = useState('');
    const [timeslot, setTimeslot] = useState('');
    const [reason, setReason] = useState('');
    const [minDate, setMinDate] = useState(new Date());
    const [selectedDays, setSelectedDays] = useState([]);

    const daysOfWeek = [
        { id: "Monday", label: 'Monday' },
        { id: "Tuesday", label: 'Tuesday' },
        { id: "Wednesday", label: 'Wednesday' },
        { id: "Thursday", label: 'Thursday' },
        { id: "Friday", label: 'Friday' },
    ];

    const handleCheckboxChange = (id) => {
        setSelectedDays((prev) => {
            if (prev.includes(id)) {
                return prev.filter(day => day !== id); // Uncheck
            } else {
                return [...prev, id]; // Check
            }
        });
    };

    const onchange1 = (args) => {
        if (args) {
            setSelectedValue1(format(args.value, 'yyyy-MM-dd'));
            setMinDate(args.value);
            console.log(args.value.toLocaleDateString());
        }
    };

    const onchange2 = (args) => {
        if (args) {
            setSelectedValue2(format(args.value, 'yyyy-MM-dd'));
            console.log(args.value.toLocaleDateString());
        }
    };


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

    const handleSubmit = async (event) => {
        event.preventDefault();
        try {
            alert("Sent request");
            
            const application = { staffId, email, reason, type, timeslot, selectedDays, selectedValue1, selectedValue2, supervisor,file };
            
            console.log(application.staffId);
            console.log(application.selectedDays);
            console.log(application.selectedValue1, application.selectedValue2, application.file, application.supervisor);
            const response = await axios.post('http://127.0.0.1:5001/createApplication', {
                'employee_id': application.staffId,
                'start_date': application.selectedValue1, 
                'end_date': application.selectedValue2,
                'timeslot': application.timeslot,
                'selected_days': application.selectedDays,
                'email': application.email,
                'reason': application.reason,
                'supervisor': application.supervisor,
                'type': application.type,
            }, {
                headers: {
                    'Content-Type': 'application/json'
                }
            });

            // Handle successful response
            alert(`${response.data.message}`);

        } catch (error) {
            console.error("Form submission failed", error);
            alert("form submission failed");
        }
    };

    const handleTypeChange = (e) => {
        e.preventDefault();
        setType(e.target.value);
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
            
            <label for="arrangement-type-select">Arrangement type:</label>
                <select
                id="arrangement-type-select"
                value={type}
                style ={{margin:'10px'}}
                label="timeslot"
                onChange={handleTypeChange}
                >
                <option value={'AdHoc'}>Ad-Hoc</option>
                <option value={'Recurring'}>Recurring</option>
               
                </select>
            </div>
            <div className="arrange-timeslot" style={{width:'50%',flexDirection: 'row',display: 'flex',alignItems: 'center'}}>
            
                <label for="arrangement-select">Arrangement timeslot:</label>
                    <select
                    id="arrangement-select"
                    value={timeslot}
                    style ={{margin:'10px'}}
                    label="timeslot"
                    onChange={handleTimeslotChange}
                    >
                    <option value={'AM'}>AM</option>
                    <option value={'PM'}>PM</option>
                    <option value={"Full-day"}>Full-day</option>
                    </select>
            </div>
            {type == "Recurring" && ( 
            <div className="arrange-days" style={{width:'50%',flexDirection: 'row',display: 'flex',alignItems: 'center'}}>
            
                <label for="arrangement-days">Days for recurring:</label>
                {daysOfWeek.map(day => (
                     <label>
                        <input
                            type="checkbox"
                            id={day.id}
                            label={day.label}
                            checked={selectedDays.includes(day.id)}
                            onChange={() => handleCheckboxChange(day.id)}
                        />
                        {day.label}
                    </label>
            ))}
            </div>
            )}
            <div className="date-select" >
            <span >Date(s):</span> 
            <div style = {{display: "flex", flexDirection: "row"}}>
                <CalendarComponent 
                    id="calendar" 
                    renderDayCell={disabledDate} 
                    isMultiSelection={false}
                    change={onchange1}
                >
                </CalendarComponent> 
                {type == "Recurring" && ( 
                <CalendarComponent 
                    id="calendar" 
                    renderDayCell={disabledDate} 
                    isMultiSelection={false}
                    change={onchange2}
                    min={minDate}
                >
                </CalendarComponent>  
                )}
            </div>
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