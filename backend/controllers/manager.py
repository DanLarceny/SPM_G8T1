from flask import Blueprint, jsonify, request
from models.Employee import Employee
from models.WFH_Application import WFHApplication
manager_bp = Blueprint('manager', __name__)

@manager_bp.route('/viewPendingWFHRequests/<staff_id>', methods=['GET'])
def view_pending_wfh_requests(staff_id):
    try:
        manager = Employee.query.filter_by(Staff_ID=staff_id).first()
        if not manager:
            return jsonify({'error': 'Manager not found'}), 404
        
        pending_req = WFHApplication.query.filter_by(Reporting_Manager=staff_id, Status='Pending').all()
        print(pending_req)
        
        if not pending_req:
            return jsonify({'message': 'No pending requests found'}), 200
        
        pending_wfh_list = [
            {
                "application_id": wfh_request.Application_ID,
                "staff_id": wfh_request.Staff_ID,
                "start_date": wfh_request.Start_Date,
                "end_date": wfh_request.End_Date,
                "status": wfh_request.Status,
                "time_slot": wfh_request.Time_Slot,
                "type": wfh_request.Type,
                "email": wfh_request.Email
            }
            for wfh_request in pending_req
        ]
        return jsonify(pending_wfh_list), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    

@manager_bp.route('/approveWFHRequest/<application_id>', methods=['POST'])
def approve_wfh_request(application_id):
    try:
        wfh_request = WFHApplication.query.get(application_id)
        if not wfh_request:
            return jsonify({'error': 'Request not found'}), 404

        return jsonify({'message': 'Request approved'}), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@manager_bp.route('/rejectWFHRequest/<application_id>', methods=['POST'])
def reject_wfh_request(application_id): 
    try: 
        # Fetch the WFH application
        wfh_request = WFHApplication.query.get(application_id)
        
        # Check if the application exists
        if not wfh_request:
            return jsonify({'error': 'Request not found'}), 404
        
        # Check if the application is pending and the current user is the reporting manager
        if wfh_request.Status != 'Pending':
            return jsonify({'error': 'Cannot reject this request'}), 400
        else: 
            # Reject the application
            wfh_request.reject()

        return jsonify({'message': 'Request rejected'}), 200
    except Exception as e: 
        return jsonify({'error': str(e)}), 500

