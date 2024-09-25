from app import db  # Import the db instance
from models.WFH_Schedule import WFHSchedule
from models.WFH_Application import WFHApplication
from models.Role import Role  


class Employee(db.Model):
    __tablename__ = 'Employee'
    
    staff_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    staff_f_name = db.Column(db.String(50))
    staff_l_name = db.Column(db.String(50))
    dept = db.Column(db.String(50))
    position = db.Column(db.String(50))
    country = db.Column(db.String(50))
    email = db.Column(db.String(50))
    reporting_manager = db.Column(db.Integer, db.ForeignKey('Employee.staff_id'))
    role = db.Column(db.Integer, db.ForeignKey(Role.role))
    password = db.Column(db.String(50))

    def __repr__(self):
        return f"Employee({self.staff_id}, {self.staff_f_name}, {self.staff_l_name}, {self.role})"
   
#   method to get own schedule
    def getOwnSchudules(self):
        return self.schedules

#   method to get team schedule
    def getTeamSchedules(self):
        return WFHSchedule.query.filter(
            (WFHSchedule.team_id == self.reporting_manager) & 
            (WFHSchedule.staff_id != self.staff_id)
        ).all()

#   method to get all my WFH_Application
    def getAppliactions(self):
        return WFHApplication.query.filter_by(staff_id=self.staff_id).all()

#   method to cancel/withdraw schedule
    def withDrawSchedule(self, schedule_id):
        schedule = WFHSchedule.query.get(schedule_id)
        if schedule and schedule.staff_id == self.staff_id:
            schedule.status = 'Cancelled'
            db.session.commit()
            return True
        return False
        

#   method to cancel/withdraw WFH_Application
    def withDrawApplication(self, application_id):
        application = WFHApplication.query.get(application_id)
        if application and application.staff_id == self.staff_id:
            # Change the status to 'Withdrawn'
            application.status = 'Withdrawn'
            db.session.commit()
            return True
        return False
        









    