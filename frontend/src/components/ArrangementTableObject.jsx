import { React, useState, useRef } from 'react';
import Box from '@mui/material/Box';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Paper from '@mui/material/Paper';
import Select from '@mui/material/Select';
import MenuItem from '@mui/material/MenuItem';

import ArrangementOverlay from './ArrangementOverlay';

const ArrangementTableObject = ({mode, rows, onUpdateStatus}) =>{
    const [openOverlay, setOpenOverlay] = useState(false);
    const [selectedRow, setSelectedRow] = useState(null);
    const [selectedType, setSelectedType] = useState(''); // For Type dropdown
    const [selectedStatus, setSelectedStatus] = useState(''); // For Status dropdown
    

    const handleRowClick = (row) => {
        setSelectedRow(row);
        setOpenOverlay(true);
    };

    const handleCloseOverlay = () => {
        setOpenOverlay(false);
        setSelectedRow(null);
    };

    const filteredRows = rows.filter(row => {
        const typeMatches = selectedType ? row.type === selectedType : true;
        const statusMatches = selectedStatus ? row.status === selectedStatus : true;
        return typeMatches && statusMatches;
    });

    return(
        <div style={{width:'90%', margin:'auto' , padding:'25px'}} >
             {/* Dropdown filters */}
             <Box sx={{ display: 'flex', justifyContent: 'right', marginBottom: '10px' }}>
                <Select
                    value={selectedType}
                    onChange={(e) => setSelectedType(e.target.value)}
                    displayEmpty
                    sx={{ minWidth: 120 }}
                >
                    <MenuItem value="">All Types</MenuItem>
                    <MenuItem value="Ad-hoc">Adhoc</MenuItem>
                    <MenuItem value="Recurring">Recurring</MenuItem>
                </Select>

                <Select
                    value={selectedStatus}
                    onChange={(e) => setSelectedStatus(e.target.value)}
                    displayEmpty
                    sx={{ minWidth: 120 }}
                >
                    <MenuItem value="">All Status</MenuItem>
                    <MenuItem value="Pending">Pending</MenuItem>
                    <MenuItem value="Approved">Approved</MenuItem>
                    <MenuItem value="Rejected">Rejected</MenuItem>
                    <MenuItem value="Cancelled">Cancelled</MenuItem>
                    <MenuItem value="Withdrawn">Withdrawn</MenuItem>
                </Select>
            </Box>
            <TableContainer component={Paper}>
                <Table sx={{ minWidth: 650 }} aria-label="simple table">
                <TableHead>
                    <TableRow>
                        <TableCell>Application ID</TableCell>
                        {mode === 'leaveApproval' && (
                        <TableCell align="left">Employee Name</TableCell>
                        )}
                        <TableCell align="left">Start date</TableCell>
                        <TableCell align="left">End date</TableCell>
                        <TableCell align="left">Type</TableCell>
                        <TableCell align="left">Days</TableCell>
                        <TableCell align="left">Reason</TableCell>
                        <TableCell align="left">Status</TableCell>
                    </TableRow>
                </TableHead>
                <TableBody>
                    {filteredRows.map((row) => (
                        <TableRow
                        key={row.applicationId}
                        sx={{ '&:last-child td, &:last-child th': { border: 0 } }}
                        onClick={() => handleRowClick(row)} style={{ cursor: 'pointer' }}
                        >
                        <TableCell component="th" scope="row">
                            {row.applicationId}
                        </TableCell>
                        {mode === 'leaveApproval' && (
                        <TableCell align="left">{row.name}</TableCell>
                        )}
                        <TableCell align="left">{row.startDate.toLocaleDateString()}</TableCell>
                        <TableCell align="left">{row.endDate.toLocaleDateString()}</TableCell>
                        <TableCell align="left">{row.type}</TableCell>
                        <TableCell align="left">{row.days.length > 0 ? row.days.join(', ') : '-'}</TableCell>
                        <TableCell align="left">{row.reason}</TableCell>
                        <TableCell align="left">{row.status}</TableCell>
                    </TableRow>
                    ))}
        </TableBody>

                </Table>
            </TableContainer>
            {selectedRow && (
                <ArrangementOverlay mode={mode}  open={openOverlay} onClose={handleCloseOverlay} rowData={selectedRow} 
                    onCancel={(reason) => {  // TODO: ensure methods update WFH application on db side
                    onUpdateStatus(selectedRow.applicationId, 'Cancelled');
                    alert(`Status updated for ${selectedRow.applicationId} to cancelled.`); 
                    setSelectedRow(null); 
                            }}
                    onWithdraw={(reason) => {
                        onUpdateStatus(selectedRow.applicationId, 'Withdrawn');
                        alert(`Status updated for ${selectedRow.applicationId} to withdrawn.`); 
                        setSelectedRow(null); 
                                }}
                    onApprove={() => {
                        onUpdateStatus(selectedRow.applicationId, 'Approved');
                        alert(`Status updated for ${selectedRow.applicationId} to approved.`); 
                        setSelectedRow(null); 
                                }}
                    onReject={() => {
                        onUpdateStatus(selectedRow.applicationId, 'Rejected');
                        alert(`Status updated for ${selectedRow.applicationId} to rejected.`); 
                        setSelectedRow(null); 
                                }}
                />
            )}
        </div>
        


    );

}
export default ArrangementTableObject;