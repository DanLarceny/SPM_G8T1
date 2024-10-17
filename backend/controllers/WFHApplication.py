from flask import Blueprint, jsonify, request
from models.Employee import Employee
from models.WFH_Application import WFHApplication
from datetime import datetime, timedelta

wfh_application_bp = Blueprint('wfh_application', __name__)

def parse_date(date_str):
    return datetime.strptime(date_str, "%Y-%m-%d").date()

def validate_dates(start_date, end_date):
    if start_date < datetime.now().date() or end_date < datetime.now().date():
        return "Cannot apply for past time blocks."
    
    if start_date > end_date:
        return "Start Date cannot be after End Date."
    
    if start_date > datetime.now().date() + timedelta(days=365):
        return "Cannot apply for dates which are one year away from the present date."
    
    return None  # No validation errors

def create_application(application_type, staff_id, start_date, end_date, time_slot, selected_days, email, reason, reporting_manager):
    if application_type == "AdHoc" and len(selected_days) == 0:
        return WFHApplication.createApplication(
            staff_id, 
            start_date, 
            end_date, 
            time_slot, 
            None, 
            email, 
            reason, 
            application_type, 
            reporting_manager
        )
    elif application_type == "Recurring" and len(selected_days) > 0 and start_date != end_date:
        return WFHApplication.createApplication(
            staff_id, 
            start_date, 
            end_date, 
            time_slot, 
            selected_days, 
            email, 
            reason, 
            application_type, 
            reporting_manager
        )
    return None  # For other types

@wfh_application_bp.route('/createApplication', methods=['POST'])
def apply_wfh():
    data = request.get_json()
    employee_id = data.get('employee_id')

    # Fetch the employee
    employee = Employee.get_employee(employee_id)
    
    if not employee:
        return jsonify({"error": "Employee not found"}), 404

    # Extracting values from the data dictionary
    staff_id = data.get("employee_id")
    start_date_str = data.get("start_date")
    end_date_str = data.get("end_date")
    time_slot = data.get("time_slot")
    selected_days = data.get('selected_days', [])
    email = data.get('email')
    reason = data.get('reason')
    application_type = data.get('type')

    # Check for required fields
    required_fields = [staff_id, start_date_str, end_date_str, time_slot, application_type, email, reason]
    if any(field is None for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400
    
    # Parse the input date strings
    try:
        start_date = parse_date(start_date_str)
        end_date = parse_date(end_date_str)
    except ValueError as e:
        return jsonify({"error": f"Invalid date format: {str(e)}"}), 400

    # Validate date range
    validation_error = validate_dates(start_date, end_date)
    if validation_error:
        return jsonify({"error": validation_error}), 400
    
    # Create the application
    application = create_application(application_type, staff_id, start_date, end_date, time_slot, selected_days, email, reason, employee.Reporting_Manager)
    
    if application:
        return jsonify(application.to_dict()), 201
    else:
        return jsonify({"error": "Invalid request"}), 400

        