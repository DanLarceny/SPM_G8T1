from extensions import db 
from models.Role import Role


class Employee(db.Model):
    __tablename__ = 'Employee'
    
    Staff_ID = db.Column(db.Integer, primary_key=True)
    Staff_FName = db.Column(db.String(50), nullable=False)
    Staff_LName = db.Column(db.String(50), nullable=False)
    Dept = db.Column(db.String(50), nullable=False)
    Position = db.Column(db.String(50), nullable=False)
    Country = db.Column(db.String(50), nullable=False)
    Email = db.Column(db.String(50), nullable=False)
    Reporting_Manager = db.Column(db.Integer, db.ForeignKey('Employee.Staff_ID'), nullable=False)
    Role = db.Column(db.Integer, db.ForeignKey('Role.Role'), nullable=False)
    Password = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f"Employee({self.Staff_ID}, {self.Staff_FName}, {self.Staff_LName}, {self.Role})"
    
    @classmethod
    def get_employee(cls,employee_id):
        return cls.query.filter_by(Staff_ID=employee_id).first()
        
        
#   method to get own schedule
    def getOwnSchedules(self):
        return self.schedules

#   method to get team schedule
    def get_team_schedules(self):
        # Get all employees with the same reporting manager, excluding self
        team_members = Employee.query.filter(
            Employee.Reporting_Manager == self.Reporting_Manager,
            Employee.Staff_ID != self.Staff_ID
        ).all()

        # Collect all schedules from team members
        team_schedules = []
        for member in team_members:
            team_schedules.extend(member.schedules)

        return team_schedules

#   method to get all my WFH_Application
    def getApplications(self):
        return self.applications

#   method to cancel/withdraw schedule
    def withdrawSchedule(self, schedule_id):
        for schedule in self.schedules:
            if schedule.Schedule_ID == schedule_id:
                schedule.status = 'Cancelled'
                db.session.commit()
                return True
        return False

#   method to cancel/withdraw WFH_Application
    def withdrawApplication(self, application_id):
        for application in self.applications:
            if application.Application_ID == application_id:
                application.status = 'Withdrawn'
                db.session.commit()
                return True
        return False
