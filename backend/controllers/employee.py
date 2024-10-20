# ALL the employee(general user) logic goes here

from flask import request, jsonify, Blueprint, session
from models.Employee import Employee
from models.WFH_Schedule import WFHSchedule
from models.WFH_Application import WFHApplication
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from datetime import datetime, timedelta
from config import SECRET_KEY  # Make sure to create a SECRET_KEY in your config file
from extensions import db
from sqlalchemy.exc import SQLAlchemyError

employee_bp = Blueprint('employee', __name__)

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
        if check_employee.Password != "":
            return jsonify({"error": "Employee already exists"}), 400
        
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

# @employee_bp.route('/viewOwnSchedule', methods=['GET'])
# #retrieve one 
# def retrieve_one_schedule():
    
#     try:

#         data = request.get_json()
#         if not data:
#             return jsonify({"error": "Request body is empty"}), 400
    
#         staff_id = data.get('staff_id')
#         schedule_id = data.get('schedule_id')

#         if not staff_id or not schedule_id:
#             return jsonify({"error": "Staff ID or Schedule ID invalid."}), 400

#         #check employee exists
#         employee = Employee.get_employee(staff_id)
#         if not employee:
#             return jsonify({"error": "Employee not found"}), 404
    
#         #if employee and schedule exists, retrieve schedule
        
#         schedule_retrieved = employee.getOwnSchedules()
#         if schedule_retrieved:

#             return jsonify({"schedule": schedule_retrieved,}), 200
        
#         return jsonify({"error": "Schedule not found"}), 404

#     except Exception as e:
#         return jsonify({"error": str(e)}), 500
    
# @employee_bp.route('/viewTeamSchedules', methods=['GET'])
# #get team schedule
# def view_team_schedules():
#     try:

#         data = request.get_json()
#         if not data:
#             return jsonify({"error": "Request body is empty"}), 400
        
#         staff_id = data.get('staff_id')
#         if not staff_id:
#             return jsonify({"error": "Staff ID is required."}), 400

#         # Check if employee exists
#         employee = Employee.get_employee(staff_id)
#         if not employee:
#             return jsonify({"error": "Employee not found."}), 404

#         # Retrieve team schedules
#         team_schedules = employee.get_team_schedules()
#         if team_schedules:
#             return jsonify({"team_schedules": team_schedules}), 200
#         else:
#             return jsonify({"message": "No team schedules found."}), 404

#     except Exception as e:
#         return jsonify({"error": str(e)}), 500
    
# @schedule_bp.route('/createSchedule', methods=['POST'])
# #create

# def createSchedule():

#     try:

#         data = request.get_json()
#         if not data:
#             return jsonify({"error": "Request body is empty"}), 400
    
#         staff_id = data.get('staff_id')
#         schedule_id = data.get('schedule_id')
#         application_id = data.get('application_id')
#         date = data.get('date')
#         timeslot = data.get('timeslot')

#         if not staff_id or not schedule_id or not application_id or not date or not timeslot:
#             return jsonify({"error": "Some fields are invalid."}), 400

#         #check employee exists
#         employee = Employee.get_employee(staff_id)
#         if not employee:
#             return jsonify({"error": "Employee not found"}), 404
        
#         # Convert date from string to datetime object
#         try:
#             date = datetime.strptime(date, '%Y-%m-%d')
#         except ValueError:
#             return jsonify({"error": "Invalid date format. Use YYYY-MM-DD"}), 400

#         # if employee exists, create schedule 
        
#         try:
#             new_schedule = WFHSchedule.createSchedule(staff_id, application_id, date, timeslot)
#             return jsonify({"message": "Schedule created successfully.", "schedule": new_schedule}), 200
        
#         except Exception as e:
#             return jsonify({"error": "An error occurred while creating the schedule."}), 500

#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

# #update  
# @schedule_bp.route('/updateSchedule', methods=['PUT'])

# def updateSchedule():

#     try:

#         data = request.get_json()

#         schedule_id = data.get('schedule_id')
#         date = data.get('date')
#         timeslot = data.get('timeslot')

#         if not schedule_id or not date or not timeslot:
#             return jsonify({"error": "Some fields are invalid."}), 400
    
#         try:
#             updated_schedule = WFHSchedule.updateSchedule(schedule_id, timeslot, date)
#             return jsonify({"message": "Schedule updated successfully.", "schedule": updated_schedule}), 200
        
#         except Exception as e:
#             return jsonify({"error": "An error occurred while updating the schedule."}), 500


#     except Exception as e:
#         raise e
    
# #create application 
# @application_bp.route('/createApplication', methods=['POST'])

# def createApplication():

#     try:

#         data = request.get_json()

#         staff_id = data.get('staff_id')
#         schedule_id = data.get('schedule_id')
#         start_date = data.get('start_date')
#         end_date = data.get('end_date')
#         timeslot = data.get('timeslot')
#         type = data.get('type')
#         email = data.get('email')
#         reporting_manager = data.get('reporting_manager')

#         if not schedule_id or not staff_id or not start_date or not end_date or not timeslot:
#             return jsonify({"error": "Some fields are invalid."}), 400
        
        # try:
        #     start_date = datetime.strptime(start_date, '%Y-%m-%d')
        #     end_date = datetime.strptime(end_date, '%Y-%m-%d')
        # except ValueError:
        #     return jsonify({"error": "Invalid date format. Use YYYY-MM-DD"}), 400
            
        #check employee, schedules exists
        # employee = Employee.query.get(staff_id)
    
#         # if employee exists, create application
#         if employee:

#             try:
#                 new_application = WFHApplication.createApplication(staff_id, start_date, end_date, timeslot, type, email, reporting_manager)
#                 return jsonify({"message": "Application created successfully.", "application": new_application}), 200
            
#             except Exception as e:
#                 raise e

#         return new_application

#     except Exception as e:
#         return jsonify({"error": str(e)}), 500
    
# # search avail dates for app: 

# @application_bp.route('/availableDates', methods=['GET'])
# def searchAvailableDates():

#     try:
#         data = request.get_json()
#         staff_id = data.get('staff_id')
#         start_date = request.args.get('start_date')
#         end_date = request.args.get('end_date')

#         if not staff_id or not start_date or not end_date:
#             return jsonify({"error": "Staff ID , start date, and end date are required."}), 400
        
#         availDates = WFHApplication.searchForAvailableDates(staff_id, start_date, end_date)
#         return jsonify({"available_dates": availDates}), 200

#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

# # display dates for app 
# @application_bp.route('/displayDates', methods=['GET'])
# def displayDates():
#     try: 
#         availDates = WFHApplication.displayAvailableDates()       
#         return jsonify({"available_dates": availDates}), 200
        
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500
    
# @application_bp.route('/getApplication', methods=['GET'])
# def getApplication():

#     try:
#         data = request.get_json()

#         staff_id = data.get('staff_id')
#         application_id = data.get('application_id')
#         application = WFHApplication.getArrangement(staff_id, application_id)
#         return jsonify({"application": application}), 200
        
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500
    
# # withdraw schedule
# @schedule_bp.route('/withdrawSchedule', methods=['DELETE'])

# def withdrawSchedule(): 
#     try: 
#         data = request.get_json()

#         staff_id = data.get('staff_id')
#         schedule_id = data.get('schedule_id')
#         reason = data.get('reason')

#         if not staff_id or not schedule_id or not reason: 
#             return jsonify({"error": "Staff ID, Schedule ID, and Reason are all required"}), 400

#         employee = Employee.get_employee(staff_id)
#         if not employee:
#             return jsonify({"error": "Employee not found"}), 404
        
#         schedule = WFHSchedule.query.get(schedule_id)
#         if not schedule:
#             return jsonify({"error": "Schedule not found"}), 404
        
#         if schedule.Staff_ID != staff_id: 
#             return jsonify({"error": "You can only withdraw your own schedules"}), 403
        
#         if datetime.now() >= schedule.Date:
#             return jsonify({"error": "Cannot withdraw a schedule that has already started or passed"}), 400
        
        # if not schedule.can_withdraw():
        #     return jsonify({"error": "Cannot withdraw a schedule within 24 hours of its start date."}), 400
        
        # # Prompt for confirmation
        # confirmation = data.get('confirmation')
        # if not confirmation or confirmation.lower() != 'confirm':
        #     return jsonify({"message": "Please confirm your intention to withdraw this schedule. Send the request again with 'confirmation': 'confirm' in the payload."}), 200

        # #Withdraw schedule
        # try: 
        #     schedule.withdraw(reason)
        # except Exception as e:
        #     return jsonify({"error": str(e)}), 400

#         # Notify the manager
#         notify_manager(employee.manager_id, staff_id, schedule_id, reason)

#         # Return updated schedules
#         updated_schedules = WFHSchedule.query.filter_by(Staff_ID=staff_id).all()
#         return jsonify({"message": "Schedule withdrawn successfully", "updated_schedules": [s.to_dict() for s in updated_schedules]}), 200

    # except Exception as e:
    #     db.session.rollback()
    #     return jsonify({"error": "An error occurred while withdrawing the schedule. No changes were made."}), 500

# def notify_manager(manager_id, staff_id, schedule_id, reason):
#     # Implement your notification logic here
#     # This could involve sending an email, creating a notification in the database, etc.
#     pass