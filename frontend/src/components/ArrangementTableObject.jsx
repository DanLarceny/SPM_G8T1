import { React, useState } from 'react';
import Box from '@mui/material/Box';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Paper from '@mui/material/Paper';
// import Moment from 'moment';

import ArrangementOverlay from './ArrangementOverlay';

const ArrangementTableObject = ({rows}) =>{

    const [openOverlay, setOpenOverlay] = useState(false);
    const [selectedRow, setSelectedRow] = useState(null);

    const handleRowClick = (row) => {
        setSelectedRow(row);
        setOpenOverlay(true);
    };

    const handleCloseOverlay = () => {
        setOpenOverlay(false);
        setSelectedRow(null);
    };

    return(
        <div style={{width:'90%', margin:'auto' , padding:'25px'}} >
            <TableContainer component={Paper}>
                <Table sx={{ minWidth: 650 }} aria-label="simple table">
                <TableHead>
                    <TableRow>
                        <TableCell>Application ID</TableCell>
                        <TableCell align="left">Date&nbsp;(s)</TableCell>
                        <TableCell align="left">Type</TableCell>
                        <TableCell align="left">Reason</TableCell>
                        <TableCell align="left">Status</TableCell>
                    </TableRow>
                </TableHead>
                <TableBody>
                    {rows.map((row) => (
                        <TableRow
                        key={row.applicationId}
                        sx={{ '&:last-child td, &:last-child th': { border: 0 } }}
                        onClick={() => handleRowClick(row)} style={{ cursor: 'pointer' }}
                        >
                        <TableCell component="th" scope="row">
                            {row.applicationId}
                        </TableCell>
                        <TableCell align="left">
                            {row.date.map((iDate) => (
                            <div >
                                {iDate.toLocaleDateString()} {/* Format the date here */}
                            </div>
                                ))}
                        </TableCell>
                        <TableCell align="left">{row.type}</TableCell>
                        <TableCell align="left">{row.reason}</TableCell>
                        <TableCell align="left">{row.status}</TableCell>
                    </TableRow>
                    ))}
        </TableBody>

                </Table>
            </TableContainer>
            {selectedRow && (
                <ArrangementOverlay open={openOverlay} onClose={handleCloseOverlay} rowData={selectedRow} />
            )}
        </div>
        


    );

}
export default ArrangementTableObject;