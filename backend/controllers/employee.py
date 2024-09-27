# ALL the employee(general user) logic goes here

from flask import request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from backend.models.Employee import Employee
from backend.models.HR_CSuite import db, RegisteredEmployee, Staff, ManagerDirector, HRSeniorManagement
from backend.models.Manager import db, RegisteredEmployee, Staff, ManagerDirector, HRSeniorManagement

def register_user():
    data = request.get_json()

    staff_id = data.get('employee_id')
    password = data.get('password')
    cpassword = data.get('cpassword')


    company_employee = Employee.query.filter_by(staff_id=staff_id).first()
    if not company_employee:
        return jsonify({"error": "Invalid ID: Employee not found in company records!"}), 400

    
    if company_employee.password is not None:
        return jsonify({"error": "Employee is already registered! Please proceed to log in."}), 400

    company_employee.set_password(password)

    db.session.commit()

    return jsonify({"message": "Registration successful!"}), 201
