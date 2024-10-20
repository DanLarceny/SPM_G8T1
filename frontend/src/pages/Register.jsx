import React, { useState } from 'react';
import { TextField, Button, Typography, Link, IconButton, InputAdornment } from '@mui/material';
import { Visibility, VisibilityOff } from '@mui/icons-material';
import Grid from '@mui/material/Grid2';
import { useNavigate } from 'react-router-dom';
import '../Form.css';
import axios from 'axios';


const Register = () => {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    employeeId: '',
    password: '',
    cpassword: '',
  });
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);
  const [errors, setErrors] = useState({});


  const handleChange = (event) => {
  const { name, value } = event.target;
    setFormData(prevData => ({
      ...prevData,
      [name]: value,
    }));
    setErrors(prevErrors => ({
      ...prevErrors,
      [name]: '',
    }));
    
  };

  const validateForm = () => {
    const newErrors = {};
    if(formData.password != formData.cpassword){
      newErrors.cpassword = 'Passwords do not match';
      alert("Passwords do not match!");
    }
    setErrors(newErrors)
    return Object.keys(newErrors).length === 0;
  }

  const handleSubmit = (event) => {
    event.preventDefault();
    // Handle form submission
    if (validateForm()) {
      console.log('Form data submitted:', formData);
      // Handle registration logic here
      axios.post('http://127.0.0.1:5000/register', {
        employee_id: formData.employeeId,
        password: formData.password,
        reconfirm_password: formData.cpassword,
    })
    .then(response => {
        console.log(response.data);
        alert("Registration successful!");
        navigate('/login');  
    })
    .catch(error => {
        console.error("There was an error registering:", error);
        if (error.response) {
            alert(error.response.data.error || "Registration failed!");
        } else {
            alert("An unexpected error occurred!");
        }
    });
      
    }
  };

  const togglePasswordVisibility = () => {
    setShowPassword(!showPassword);
  };

  const toggleConfirmPasswordVisibility = () => {
    setShowConfirmPassword(!showConfirmPassword);
  };

  return (
    <div className='user-form'>
        <Typography variant="h5" gutterBottom component='p' className='outfit-font'>
          Register
        </Typography>
        <Typography variant="body2" component="p" className="outfit-font2">
          Create your account below
        </Typography>
        <form onSubmit={handleSubmit}>
          <Grid className="input-field" container spacing={2}>
            <Grid item size={{ xs: 6, md: 8 }}>
              <TextField
                name="employeeId"
                label="Enter your Employee ID"
                variant="outlined"
                fullWidth
                required
                value={formData.employeeId}
                onChange={handleChange}
                error={!!errors.employeeId}
                helperText={errors.employeeId}
              />
            </Grid>
            <Grid item size={{ xs: 6, md: 8 }}>
              <TextField
                name="password"
                label="Password"
                variant="outlined"
                type={showPassword ? 'text' : 'password'}
                fullWidth
                required
                value={formData.password}
                onChange={handleChange}
                error={!!errors.password}
              helperText={errors.password}
              InputProps={{
                endAdornment: (
                  <InputAdornment position="end">
                    <IconButton onClick={togglePasswordVisibility} edge="end">
                      {showPassword ? <VisibilityOff /> : <Visibility />}
                    </IconButton>
                  </InputAdornment>
                ),
              }}
              />
            </Grid>
            <Grid item size={{ xs: 6, md: 8 }}>
              <TextField
                name="cpassword"
                label="Confirm Password"
                variant="outlined"
                type={showConfirmPassword ? 'text' : 'password'}
                fullWidth
                required
                value={formData.cpassword}
                onChange={handleChange}
                error={!!errors.cpassword}
                helperText={errors.cpassword}
                InputProps={{
                  endAdornment: (
                    <InputAdornment position="end">
                      <IconButton onClick={toggleConfirmPasswordVisibility} edge="end">
                        {showConfirmPassword ? <VisibilityOff /> : <Visibility />}
                      </IconButton>
                    </InputAdornment>
                  ),
                }}
              />
            </Grid>
          </Grid>
          <div className='login-btn-location'>
            <Button
              type="submit"
              variant="contained"
              className='login-btn'
              onClick={handleSubmit}
            >
              Register
            </Button>
          </div>
        </form>
        <div className='login-link'>
          <Typography variant="body2">
            <Link className='' href="./login">Login here</Link>
          </Typography>
        </div>
    </div>
    
  );
};

export default Register;
