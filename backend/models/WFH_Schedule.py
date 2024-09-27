from extensions import db
from models.Employee import Employee  
from models.WFH_Application import WFHApplication

class WFHSchedule(db.Model):
    __tablename__ = 'WFH_Schedule'
    
    Schedule_ID = db.Column(db.Integer, primary_key=True)
    Staff_ID = db.Column(db.Integer, db.ForeignKey(Employee.staff_id), nullable=False, index=True)
    Application_ID = db.Column(db.Integer, db.ForeignKey(WFHApplication.application_id), nullable=False, index=True)
    Team_ID = db.Column(db.Integer, db.ForeignKey(Employee.staff_id), nullable=False, index=True)
    Date = db.Column(db.DateTime, nullable=False)
    Time_Slot = db.Column(db.Enum('AM', 'PM', 'Day'), nullable=False)
    Status = db.Column(db.Enum('Passed', 'Upcoming', 'Cancelled'), nullable=False)

    # Relationships
    employee = db.relationship('Employee', foreign_keys=[Staff_ID], backref='schedules')
    application = db.relationship('WFHApplication', backref=db.backref('schedule', uselist=False))
    reporting_manager = db.relationship('Employee', foreign_keys=[Team_ID], backref='managed_schedules')

    def __repr__(self):
        return f"WFHSchedule({self.Schedule_ID}, Staff ID: {self.Staff_ID}, Application ID: {self.Application_ID}, Date: {self.Date})"
