from flask import Blueprint, jsonify, request
from extensions import db
from models.Employee import Employee
from models.WFH_Application import WFHApplication

wfh_application_bp = Blueprint('wfh_application', __name__)

@wfh_application_bp.route('/apply_wfh', methods=['POST'])
def apply_wfh():
    data = request.json
    employee_id = data.get('employee_id')
    employee = Employee.get_employee(employee_id)
    if employee:
        application = WFHApplication(
            employee_id=employee_id,
            start_date=data.get('start_date'),
            end_date=data.get('end_date'),
            reason=data.get('reason')
        )
        db.session.add(application)
        db.session.commit()
        return jsonify({"message": "WFH application submitted successfully"}), 200
    else:
        return jsonify({"error": "Employee not found"}), 404
