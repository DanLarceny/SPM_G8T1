from models.Employee import Employee;
from models.WFH_Schedule import WFHSchedule
from models.WFH_Application import WFHApplication
from extensions import db

class Manager(Employee):
    """Manager role inheriting from Employee"""

    def approve_application(self, application_id):
        application = db.session.get(WFHApplication, application_id)   # Query the application using the provided ID
        if application and application.Status == 'Pending' and application.Reporting_Manager == self.Staff_ID:
            application.approve()  # Calls the approve method of WFHApplication
            return True
        return False

    def reject_application(self, application_id):
        application = db.session.get(WFHApplication, application_id)    # Query the application using the provided ID
        if application and application.Status == "Pending" and application.Reporting_Manager == self.Staff_ID:
            application.reject()  # Calls the reject method of WFHApplication
            return True
        return False
    
    # Returns schedules for employees reporting to the manager
    def get_team_schedules(self):
        return db.session.query(WFHSchedule).filter_by(Team_ID=self.Staff_ID).all()