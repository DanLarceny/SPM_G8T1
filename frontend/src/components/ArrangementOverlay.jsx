import React, { useState } from 'react';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import CardActions from '@mui/material/CardActions';
import Button from '@mui/material/Button';
import { Modal, Box } from '@mui/material';

function useForceUpdate() {
    const [, setTick] = React.useState(0);
    const update = React.useCallback(() => {
      setTick((tick) => tick + 1);
    }, []);
    return update;
  }

const ArrangementOverlay = ({ mode, open, onClose, rowData, onCancel, onWithdraw, onApprove, onReject }) => {

    const [reason, setReason] = useState(''); // State to store cancellation reason
    const [successMessage, setSuccessMessage] = useState('');
    const [errorMessage, setErrorMessage] = useState(''); 

    const errResponse = { //mock err response obj
        ok: false, // Set this to true to simulate a success scenario
        status: 404, // Simulate 404 error
        json: async () => ({ message: 'Service not found' }) // Mock error message
      };

    const handleCancel = async (e) => {
        e.preventDefault();
        try {
          console.log({
            id: rowData.applicationId,
            reason: reason, // Pass cancellation reason to API
          });

          // TODO: Change this to actual connection string
          const response = await fetch('/api/cancel-arrangement', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({
              id: rowData.applicationId,
              reason: reason, // Pass cancellation reason to API
            }),
          });
          

// TODO: Implement erroneous response
//  use bottom block when connected to BE
        //   if (!response.ok) {
        //     const errorResponse = errResponse; // Get mock error response
        //     throw new Error(errorResponse.message || 'Failed to cancel the arrangement.');
        //   }
    
    
          if (!response.ok) {
            // Update status, close overlay, and show success message
            onCancel(reason);
            setSuccessMessage('Arrangement successfully cancelled.');
          } else {
            setSuccessMessage('Failed to cancel the arrangement.');
          }
        } catch (error) {
          console.error('Error:', error);
          setSuccessMessage('Error while cancelling the arrangement.');
        }
      };

      const handleWithdraw = async (e) => {
        e.preventDefault();
        try {
          console.log({
            id: rowData.applicationId,
            reason: reason, // Pass cancellation reason to API
          });

          // TODO: Change this to actual connection string
          const response = await fetch('/api/withdraw-arrangement', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({
              id: rowData.applicationId,
              reason: reason, // Pass cancellation reason to API
            }),
          });
          

// TODO: Implement erroneous response
//  use bottom block when connected to BE
        //   if (!response.ok) {
        //     const errorResponse = errResponse; // Get mock error response
        //     throw new Error(errorResponse.message || 'Failed to cancel the arrangement.');
        //   }
    
    
          if (!response.ok) {
            // Update status, close overlay, and show success message
            onWithdraw(reason);
            setSuccessMessage('Arrangement successfully withdrawn.');
          } else {
            setSuccessMessage('Failed to withdraw the arrangement.');
          }
        } catch (error) {
          console.error('Error:', error);
          setSuccessMessage('Error while withdrawing the arrangement.');
        }
      };

      const handleApprove = async (e) => {
        e.preventDefault();
        try {
          console.log({
            id: rowData.applicationId,
            reason: reason, // Pass cancellation reason to API
          });

          // TODO: Change this to actual connection string
          const response = await fetch('/api/approve-arrangement', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({
              id: rowData.applicationId,
              reason: reason, // Pass cancellation reason to API
            }),
          });
          

// TODO: Implement erroneous response
//  use bottom block when connected to BE
        //   if (!response.ok) {
        //     const errorResponse = errResponse; // Get mock error response
        //     throw new Error(errorResponse.message || 'Failed to cancel the arrangement.');
        //   }
    
    
          if (!response.ok) {
            // Update status, close overlay, and show success message
            onApprove(reason);
            setSuccessMessage('Arrangement application successfully approved.');
          } else {
            setSuccessMessage('Failed to approve the application.');
          }
        } catch (error) {
          console.error('Error:', error);
          setSuccessMessage('Error while approving the application.');
        }
      };

      const handleReject = async (e) => {
        e.preventDefault();
        try {
          console.log({
            id: rowData.applicationId,
            reason: reason, // Pass cancellation reason to API
          });

          // TODO: Change this to actual connection string
          const response = await fetch('/api/reject-arrangement', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({
              id: rowData.applicationId,
              reason: reason, // Pass cancellation reason to API
            }),
          });
          

// TODO: Implement erroneous response
//  use bottom block when connected to BE
        //   if (!response.ok) {
        //     const errorResponse = errResponse; // Get mock error response
        //     throw new Error(errorResponse.message || 'Failed to cancel the arrangement.');
        //   }
    
    
          if (!response.ok) {
            // Update status, close overlay, and show success message
            onReject(reason);
            setSuccessMessage('Arrangement application successfully rejected.');
          } else {
            setSuccessMessage('Failed to reject the application.');
          }
        } catch (error) {
          console.error('Error:', error);
          setSuccessMessage('Error while rejecting the application.');
        }
      };

    const forceUpdate = useForceUpdate();

  // Function to update row status in external data source (or rows array)

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
                <form onSubmit={onCancel}>
                <h2>{rowData.reason}</h2>
                <p>Type: {rowData.type}</p>
                <p>Status: {rowData.status}</p>
                <p>Period: {rowData.period}</p>
                <p>Approving supervisor: {rowData.approvingSupervisor}</p>
                <p>Date of submission: {rowData.dos.toLocaleDateString()}</p>
                <p>Dates: {rowData.date.map((iDate) => (
                            <div >
                                {iDate.toLocaleDateString()} {/* Format the date here */}
                            </div>
                                ))}</p>
                
              {mode === 'taskManagement' ? (
                <>
                <p>Reason for cancellation/withdrawal: <input
                                                type="text"
                                                value={reason}
                                                onChange={(e) => setReason(e.target.value)} // Update the reason state
                                                placeholder="Enter reason"
                                                required
                                            /></p>
               {(rowData.status == "Pending" && reason) && (
                    <Button onClick={handleCancel}>Cancel Arrangement</Button>
                    )}
                {(rowData.status == "Approved" && reason) && (
                <Button onClick={handleWithdraw}>Withdraw Arrangement</Button>
                )}
                </>
              ) : mode === 'leaveApproval' ? (
                <>
                {(
                  <>
                    <Button onClick={handleApprove}>Approve Application</Button>
                    <Button onClick={handleReject}>Reject Application</Button>
                  </>
                    )}
                </>
              ) : null}
                </form>
                
                <Button onClick={onClose}>Close</Button> 
               
            </Box>
        </Modal>
    );
};

export default ArrangementOverlay;