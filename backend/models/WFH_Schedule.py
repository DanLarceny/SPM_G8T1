from app import db  # Import the db instance
from models.Employee import Employee  
from models.WFH_Application import WFHApplication

class WFHSchedule(db.Model):
    __tablename__ = 'WFH_Schedule'
    
    schedule_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    staff_id = db.Column(db.Integer, db.ForeignKey(Employee.staff_id), nullable=False)  # Added nullable=False for clarity
    application_id = db.Column(db.Integer, db.ForeignKey(WFHApplication.application_id), nullable=False)  # Added nullable=False
    team_id = db.Column(db.Integer, db.ForeignKey(Employee.staff_id), nullable=False)  # Added team_id column

    date = db.Column(db.DateTime, nullable=False)  # Set nullable to False for required fields
    time_slot = db.Column(db.Enum('AM', 'PM', 'Day'), nullable=False)  # Set nullable to False
    status = db.Column(db.Enum('Passed', 'Upcoming', 'Cancelled'), nullable=False)  # Set nullable to False

    # Relationships
    employee = db.relationship('Employee', foreign_keys=[staff_id], backref='schedules')
    application = db.relationship('WFHApplication', backref=db.backref('schedule', uselist=False))  # One-to-one relationship
    reporting_manager = db.relationship('Employee', foreign_keys=[team_id], backref='managed_schedules')  # Relationship for Team_ID

    def __repr__(self):
        return f"WFHSchedule({self.schedule_id}, Staff ID: {self.staff_id}, Application ID: {self.application_id}, Date: {self.date})"
