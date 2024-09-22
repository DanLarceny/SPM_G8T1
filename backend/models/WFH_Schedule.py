from app import db  # Import the db instance

class WFHSchedule(db.Model):
    __tablename__ = 'WFH_Schedule'
    
    schedule_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    staff_id = db.Column(db.Integer, db.ForeignKey('Employee.staff_id'))
    application_id = db.Column(db.Integer, db.ForeignKey('WFH_Application.application_id'))
    date = db.Column(db.DateTime)
    time_slot = db.Column(db.Enum('AM', 'PM', 'Day'))
    status = db.Column(db.Enum('Passed', 'Upcoming', 'Cancelled'))

    # backref creates a relationship btw the associated models so we can access all schedules of 
    # an employee by writing : employee.schedules
    
    employee = db.relationship('Employee', backref='schedules')
    application = db.relationship('WFHApplication', backref=db.backref('schedule', uselist=False))  # One-to-one relationship

    def __repr__(self):
        return f"WFHSchedule({self.schedule_id}, {self.staff_id}, {self.date})"

    # can only be called by the staff who created this schedule in the employee controller
    def cancel(self):
        if self.status == 'Upcoming':
            self.status = 'Cancelled'
            db.session.commit()
        else:
            raise Exception("Only upcoming schedules can be cancelled.")
