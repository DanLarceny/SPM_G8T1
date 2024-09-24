from flask import Blueprint, jsonify
from backend.controllers.getOwnSchedule import getSchedule, getApplication
from datetime import datetime

schedule_bp = Blueprint('schedule', __name__)

@schedule_bp.route('/schedule/<int:staff_id>/<date>' , methods=['GET'])
def getOwnSchedule(staff_id, date):
    
    parsed_date = datetime.strptime(date, '%Y-%m-%d').date()
    schedule = getSchedule(staff_id)
    application = getApplication(staff_id, parsed_date)

    if schedule and application:
        return jsonify({
            "schedule": schedule.to_dict(),
            "application": application.to_dict()
        }), 200
    
    elif schedule:
        return jsonify({
            "schedule": schedule.to_dict(),
            "application": None,
            "message": 'No application is found for the date.'
        }), 200
    
    elif application:
        return jsonify({
            "schedule": None,
            "application": application.to_dict(),
            "message": 'No schedule is found.'
        }), 200
    
    else:
        return jsonify({
            "message": "Schedule and application not found."
        }), 404
    