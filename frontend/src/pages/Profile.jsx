import { React, useState } from 'react';
import { Navigate, useNavigate } from 'react-router-dom';

// import css
import '../App.css';
import '../Form.css';
import { Typography } from '@mui/material';

export function ProfilePage () {

    return (
        <Typography variant="h4" className='outfit-font' component="p">
                Will work on this subsequently
                {/* can match login username with db and retrieve name */}
        </Typography>
    )
};

export default ProfilePage;