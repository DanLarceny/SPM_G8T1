// import { Navigate, useNavigate } from 'react-router-dom';
import Navbar from "../components/Navbar";
import "../User.css";
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';

const UserPage = () => {
    
    const data = {staffId:1001,
                  username:"user1",
                  firstName:"Danny",
                  lastName:"Tan",
                  dept:"SPM",
                  position:"Product Manager",
                  country:"SG",
                  email:"danny@smu.sg",
                  reportMgr:2001,
                  role:"staff"
                };
    return (
        <div className="main" style={{marginTop: '10px'}}>
            <h1>Welcome, {data.username}</h1>
            <Navbar></Navbar>
            <div className="user" style={{paddingLeft: '20px',marginTop:'50px'}}>
                <h2>Your role is staff</h2>
                <h2>ID: {data.staffId}</h2>
                <h2>Full name: {data.firstName+data.lastName}</h2>
                <h2>Email: {data.email}</h2>
                <h2>Department: {data.dept}, Position: {data.position}</h2>
                <h2>Country: {data.country}</h2>
                <h2>Reporting Manager's ID: {data.reportMgr}</h2>
                
            </div>
            
        </div>
    );

};

export default UserPage;