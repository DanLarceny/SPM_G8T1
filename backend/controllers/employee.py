# ALL the employee(general user) logic goes here

from flask import request, jsonify, Blueprint, session
from models.Employee import Employee
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