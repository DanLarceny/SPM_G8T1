from .Employee import Employee;
from .WFH_Schedule import WFHSchedule
from .WFH_Application import WFHApplication

class Manager(Employee):
    """Manager role inheriting from Employee"""

    def approve_application(self, application_id):
        application = WFHApplication.query.get(application_id)  # Query the application using the provided ID
        if application and application.status == "Pending" and application.reporting_manager == self.staff_id:
            application.approve()  # Calls the approve method of WFHApplication
            return True
        return False

    def reject_application(self, application_id):
        application = WFHApplication.query.get(application_id)  # Query the application using the provided ID
        if application and application.status == "Pending" and application.reporting_manager == self.staff_id:
            application.reject()  # Calls the reject method of WFHApplication
            return True
        return False
    
    # Returns schedules for employees reporting to the manager
    def get_team_schedules(self):
        return WFHSchedule.query.filter_by(team_id=self.staff_id).all()