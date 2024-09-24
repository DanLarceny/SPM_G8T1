from flask import request, jsonify
from backend.models.userModel import User
from backend.models.employeeModel import db, RegisteredEmployee, Staff, ManagerDirector, HRSeniorManagement

def register_user():
    data = request.get_json()

    employee_id = data.get('employee_id')
    password = data.get('password')
    cpassword = data.get('cpassword')


    company_employee = User.query.filter_by(employee_id=employee_id).first()
    if not company_employee:
        return jsonify({"error": "Invalid ID: Employee not found in company records!"}), 400

    
    if company_employee.isRegistered:
        return jsonify({"error": "Employee is already registered! Please proceed to log in."}), 400

   
    role = company_employee.role


    new_employee = RegisteredEmployee(
        employee_id=employee_id,
        email=company_employee.email,  
        password=password
    )

    # Add to appropriate subclass based on role number
    if role == 1:
        manager_director = ManagerDirector(
            employee_id=employee_id,
            email=company_employee.email,
            password=password
        )
        db.session.add(manager_director)

    elif role == 2:
        hr_management = HRSeniorManagement(
            employee_id=employee_id,
            email=company_employee.email,
            password=password
        )
        db.session.add(hr_management)

    elif role == 3:
        staff_member = Staff(
            employee_id=employee_id,
            email=company_employee.email,
            password=password
        )
        db.session.add(staff_member)

    db.session.add(new_employee)
    db.session.commit()

    return jsonify({"message": "Registration successful!"}), 201
