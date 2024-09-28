# ALL the employee(general user) logic goes here

from flask import request, jsonify, Blueprint, session
from models.Employee import Employee
from models.WFH_Schedule import WFHSchedule
from models.WFH_Application import WFHApplication
employee_bp = Blueprint('employee', __name__)
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from config import SECRET_KEY  # Make sure to create a SECRET_KEY in your config file
from extensions import db

@employee_bp.route('/register', methods=['POST'])
def register_user():
    data = request.get_json()
    print(data)
    employee_id = data.get('employee_id')
    password = data.get('password')
    reconfirm_password = data.get('reconfirm_password')

    if not employee_id or not password or not reconfirm_password:
        return jsonify({"error": "All fields are required"}), 400

    if password != reconfirm_password:
        return jsonify({"error": "Passwords do not match"}), 400
    
    check_employee = Employee.get_employee(employee_id)
    print(check_employee)
    if not check_employee:
        return jsonify({"error": "No such employee exists"}), 404
    else:
        hashed_password = generate_password_hash(password)
        check_employee.Password = hashed_password
        db.session.commit()
        return jsonify({"message": "User registered successfully"}), 200


@employee_bp.route('/login', methods=['POST'])
def login_user():
    data = request.get_json()
    
    employee_id = data.get('username')
    password = data.get('password')

    if not employee_id or not password:
        return jsonify({"error": "Employee ID and password are required"}), 400

    employee = Employee.get_employee(employee_id)
    if not employee:
        return jsonify({"error": "Employee not found"}), 404

    if check_password_hash(employee.Password, password):
        # Generate the JWT token
        token = jwt.encode({
            'employee_id': employee.Staff_ID,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
        }, SECRET_KEY, algorithm='HS256')
        return jsonify({
            "message": "User logged in successfully",
            "token": token,
            "username": employee.Staff_FName,
            "email": employee.Email
        }), 200
    else:
        return jsonify({"error": "Invalid password"}), 401


@employee_bp.route('/logout', methods=['POST'])
def logout_user():
    session.clear()  # Clear the server-side session
    return jsonify({"message": "User logged out successfully"}), 200

@employee_bp.route('/viewOwnSchedule', methods=['GET'])
#retrieve one 
def retrieve_one_schedule():
    
    try:

        data = request.get_json()
    
        staff_id = data.get('staff_id')
        schedule_id = data.get('schedule_id')

        if not staff_id or not schedule_id:
            return jsonify({"error": "Staff ID or Schedule ID invalid."}), 400

        #check employee exists
        employee = Employee.get_employee(staff_id)
        if not employee:
            return jsonify({"error": "Employee not found"}), 404
    
        #if employee and schedule exists, retrieve schedule
        else:
            schedule_retrieved = employee.getOwnSchedules()
            if schedule_retrieved:

                return jsonify({"schedule": schedule_retrieved,}), 200
            
            return jsonify({"error": "Schedule not found"}), 404

    except Exception as e:
        raise e
    
@employee_bp.route('/viewTeamSchedules', methods=['GET'])
#get team schedule
def view_team_schedules():
    try:

        data = request.get_json()
        staff_id = data.get('staff_id')

        if not staff_id:
            return jsonify({"error": "Staff ID is required."}), 400

        # Check if employee exists
        employee = Employee.get_employee(staff_id)
        if not employee:
            return jsonify({"error": "Employee not found."}), 404

        # Retrieve team schedules
        team_schedules = employee.get_team_schedules()
        if team_schedules:
            return jsonify({"team_schedules": team_schedules}), 200
        else:
            return jsonify({"message": "No team schedules found."}), 404

    except Exception as e:
        raise e
    
@employee_bp.route('/createSchedule', methods=['POST'])
#create

def createSchedule():

    try:

        data = request.get_json()
    
        staff_id = data.get('staff_id')
        schedule_id = data.get('schedule_id')
        application_id = data.get('application_id')
        date = data.get('date')
        timeslot = data.get('timeslot')

        if not staff_id or not schedule_id or not application_id or not date or not timeslot:
            return jsonify({"error": "Some fields are invalid."}), 400

        #check employee exists
        employee = Employee.get_employee(staff_id)
        if not employee:
            return jsonify({"error": "Employee not found"}), 404

        # if employee exists, create schedule 
        else:
            try:
                new_schedule = WFHSchedule.createSchedule(staff_id, application_id, date, timeslot)
                return jsonify({"message": "Schedule created successfully.", "schedule": new_schedule}), 200
            
            except Exception as e:
                return jsonify({"error": "An error occurred while creating the schedule."}), 500

    except Exception as e:
        raise e

#update  
@employee_bp.route('/updateSchedule', methods=['PUT'])

def updateSchedule():

    try:

        data = request.get_json()

        schedule_id = data.get('schedule_id')
        date = data.get('date')
        timeslot = data.get('timeslot')

        if not schedule_id or not date or not timeslot:
            return jsonify({"error": "Some fields are invalid."}), 400
    
        try:
            updated_schedule = WFHSchedule.updateSchedule(schedule_id, timeslot, date)
            return jsonify({"message": "Schedule updated successfully.", "schedule": updated_schedule}), 200
        
        except Exception as e:
            return jsonify({"error": "An error occurred while updating the schedule."}), 500


    except Exception as e:
        raise e
    
#create application 
@employee_bp.route('/createApplication', methods=['POST'])

def createApplication():

    try:

        data = request.get_json()

        staff_id = data.get('staff_id')
        schedule_id = data.get('schedule_id')
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        timeslot = data.get('timeslot')
        type = data.get('type')
        email = data.get('email')
        reporting_manager = data.get('reporting_manager')

        if not schedule_id or not staff_id or not start_date or not end_date or not timeslot:
            return jsonify({"error": "Some fields are invalid."}), 400
            
        #check employee, schedules exists
        employee = Employee.query.get(staff_id)
    
        # if employee exists, create application
        if employee:

            try:
                new_application = WFHApplication.createApplication(staff_id, start_date, end_date, timeslot, type, email, reporting_manager)
                return jsonify({"message": "Application created successfully.", "application": new_application}), 200
            
            except Exception as e:
                raise e

        return new_application

    except Exception as e:
        raise e
    
# withdraw schedule