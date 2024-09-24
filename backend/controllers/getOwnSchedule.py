from backend.models.scheduleModel import Schedule
from backend.models.applicationModel import Application

def getSchedule(staff_id): 

    schedule = Schedule.query.get(staff_id)
    return schedule

def getApplication(staff_id, date):

    application = Application.query.get(staff_id, date)
    return application


