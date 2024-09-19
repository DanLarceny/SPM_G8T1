import React, { useState } from 'react';
import { TextField, Button, Typography, Container, Link } from '@mui/material';
import Grid from '@mui/material/Grid2';

const Register = () => {
  const [formData, setFormData] = useState({
    employeeId: '',
    password: '',
    cpassword: '',
  });

  const handleChange = (event) => {
    setFormData({
      ...formData,
      [event.target.name]: event.target.value,
    });
    console.log(formData)
    
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    // Handle form submission
    console.log('Form data submitted:', formData);
    // Handle case where user inputs incorrect employeeId
    if(formData.password != formData.cpassword){
      alert("Passwords do not match!");
    }
  };

  return (
    <Container component="main" fixed>
      <Typography variant="h5" gutterBottom>
        Register
      </Typography>
      <form onSubmit={handleSubmit}>
        <Grid container spacing={2}>
          <Grid item size={{ xs: 6, md: 8 }}>
            <TextField
              name="employeeId"
              label="Enter your employee Id"
              variant="outlined"
              fullWidth
              required
              value={formData.employeeId}
              onChange={handleChange}
            />
          </Grid>
          <Grid item size={{ xs: 6, md: 8 }}>
            <TextField
              name="password"
              label="password"
              variant="outlined"
              type="password"
              fullWidth
              required
              value={formData.password}
              onChange={handleChange}
            />
          </Grid>
          <Grid item size={{ xs: 6, md: 8 }}>
            <TextField
              name="cpassword"
              label="Confirm Password"
              variant="outlined"
              type="password"
              fullWidth
              required
              value={formData.cpassword}
              onChange={handleChange}
            />
          </Grid>
        </Grid>
        <Button
          type="submit"
          variant="contained"
          color="primary"
          style={{ marginTop: 16 }}

        >
          Register
        </Button>
      </form>
      <div>
        <Typography variant="body2">
          <Link href="./login">Login here</Link>
        </Typography>
      </div>
    </Container>
    
  );
};

export default Register;
