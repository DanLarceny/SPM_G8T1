import React from 'react';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import CardActions from '@mui/material/CardActions';
import Button from '@mui/material/Button';
import { Modal, Box } from '@mui/material';

const ArrangementOverlay = ({ open, onClose, rowData }) => {
    return (
        <Modal open={open} onClose={onClose}>
            <Box sx={{ 
                position: 'absolute', 
                top: '50%', 
                left: '50%', 
                transform: 'translate(-50%, -50%)', 
                bgcolor: 'background.paper', 
                boxShadow: 24, 
                p: 4 
            }}>
                <h2>{rowData.reason}</h2>
                <p>{rowData.date.map((iDate) => (
                            <div >
                                {iDate.toLocaleDateString()} {/* Format the date here */}
                            </div>
                                ))}</p>
                <button onClick={onClose}>Close</button>
            </Box>
        </Modal>
    );
};

export default ArrangementOverlay;