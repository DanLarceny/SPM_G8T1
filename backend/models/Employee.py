from app import db  # Import the db instance
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
    def get_team_schedules(self):
        # Get all employees with the same reporting manager, excluding self
        team_members = Employee.query.filter(
            Employee.reporting_manager == self.reporting_manager,
            Employee.staff_id != self.staff_id
        ).all()

        # Collect all schedules from team members
        team_schedules = []
        for member in team_members:
            team_schedules.extend(member.schedules)

        return team_schedules

#   method to get all my WFH_Application
    def getAppliactions(self):
        return self.applications

#   method to cancel/withdraw schedule
    def withDrawSchedule(self, schedule_id):
        for schedule in self.schedules:
            if schedule.id == schedule_id:
                schedule.status = 'Cancelled'
                db.session.commit()
                return True
        return False

#   method to cancel/withdraw WFH_Application
    def withDrawApplication(self, application_id):
        for application in self.applications:
            if application.id == application_id:
                application.status = 'Withdrawn'
                db.session.commit()
                return True
        return False
