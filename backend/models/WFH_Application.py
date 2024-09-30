from extensions import db
from models.Employee import Employee

class WFHApplication(db.Model):
    __tablename__ = 'WFH_Application'
    
    Application_ID = db.Column(db.Integer, primary_key=True)
    Staff_ID = db.Column(db.Integer, db.ForeignKey('Employee.staff_id'), nullable=False, index=True)
    Start_Date = db.Column(db.DateTime, nullable=False)
    End_Date = db.Column(db.DateTime, nullable=False)
    Status = db.Column(db.Enum('Pending', 'Rejected', 'Approved', 'Withdrawn'), nullable=False)
    Time_Slot = db.Column(db.Enum('AM', 'PM', 'Day'), nullable=False)
    Type = db.Column(db.Enum('AdHoc', 'Recurring'), nullable=False)
    Email = db.Column(db.String(50), nullable=False)
    Reporting_Manager = db.Column(db.String(50), nullable=False)

    employee = db.relationship('Employee', foreign_keys=[Staff_ID], backref='applications')

    def __repr__(self):
        return f"WFHApplication({self.Application_ID}, {self.Staff_ID}, {self.Status})"

    def approve(self):
        self.Status = 'Approved'
        db.session.commit()

    def reject(self):
        self.Status = 'Rejected'
        db.session.commit()

    def createApplication(cls, staff_id, start_date, end_date, time_slot, type, email, reporting_manager):

        try:

            new_application = cls(
                Staff_ID=staff_id,
                Start_Date=start_date,
                End_Date=end_date,
                Time_Slot=time_slot,
                Type=type,
                Email=email,
                Reporting_Manager=reporting_manager,
                Status='Pending'  #new application->pending
            )

            db.session.add(new_application)
            db.session.commit()
            return new_application
        
        except Exception as e:
            db.session.rollback()
            raise e

