import { React, useState } from 'react';
import Box from '@mui/material/Box';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Paper from '@mui/material/Paper';

const ArrangementListObject = () =>{

    return(
        <div style={{width:'90%', margin:'auto' }} >
            <TableContainer component={Paper}>
                <Table sx={{ minWidth: 650 }} aria-label="simple table">
                <TableHead>
            <TableRow>
                <TableCell>Application ID</TableCell>
                <TableCell align="right">Date(s)</TableCell>
                <TableCell align="right">Reason</TableCell>
                <TableCell align="right">Status</TableCell>
            </TableRow>
            </TableHead>
                </Table>
            </TableContainer>
        </div>
        


    );

}
export default ArrangementListObject;