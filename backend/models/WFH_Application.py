from extensions import db
from models.Employee import Employee
from datetime import datetime, timedelta
from sqlalchemy import Enum as SqlEnum

class WFHApplication(db.Model):
    __tablename__ = 'WFH_Application'
    
    Application_ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Staff_ID = db.Column(db.Integer, db.ForeignKey('Employee.Staff_ID'), nullable=False, index=True)
    Start_Date = db.Column(db.DateTime, nullable=False)
    End_Date = db.Column(db.DateTime, nullable=False)
    Status = db.Column(SqlEnum('Pending', 'Rejected', 'Approved', 'Withdrawn'), nullable=False)
    Time_Slot = db.Column(SqlEnum('AM', 'PM', 'Day'), nullable=False)
    Type = db.Column(SqlEnum('AdHoc', 'Recurring'), nullable=False)
    Email = db.Column(db.String(50), nullable=False)
    Reporting_Manager = db.Column(db.Integer, nullable=False)
    Days = db.Column(db.String(50))  # Store the days as a comma-separated string
    Reason = db.Column(db.String(255))

    employee = db.relationship('Employee', foreign_keys=[Staff_ID], backref='applications')

    def __repr__(self):
        return f"WFHApplication({self.Application_ID}, {self.Staff_ID}, {self.Status})"
    
    def to_dict(self):
        return {
            'Application_ID': self.Application_ID,
            'Staff_ID': self.Staff_ID,
            'Start_Date': self.Start_Date.strftime('%Y-%m-%d'), 
            'End_Date': self.End_Date.strftime('%Y-%m-%d'),
            'Status': self.Status,
            'Time_Slot': self.Time_Slot,
            'Type': self.Type,
            'Email': self.Email,
            'Reporting_Manager': self.Reporting_Manager
        }
        
    def get_selected_days(self):
        return self.Days.split(',') if self.Days else []

    def approve(self):
        if self.Status == "pending" or self.Status == "Pending" or self.Status == "PENDING":
            self.Status = "Approved"
            db.session.commit()
        elif self.Status == "approved" or self.Status == "Approved" or self.Status == "APPROVED":
            # Already approved, no action needed
            pass
        elif self.Status == "rejected" or self.Status == "Rejected" or self.Status == "REJECTED":
            raise ValueError("Cannot approve a rejected application")
        else:
            raise ValueError(f"Invalid status: {self.Status}")
        db.session.commit()

    def reject(self):
        if self.Status == "pending" or self.Status == "Pending" or self.Status == "PENDING":
            self.Status = "Rejected"
            db.session.commit()
        elif self.Status == "rejected" or self.Status == "Rejected" or self.Status == "REJECTED":
            # Already rejected, no action needed
            pass
        elif self.Status == "approved" or self.Status == "Approved" or self.Status == "APPROVED":
            raise ValueError("Cannot reject an approved application")
        else:
            raise ValueError(f"Invalid status: {self.Status}")

    @classmethod
    def createApplication(cls, staff_id, start_date, end_date, time_slot, selected_days, email, reason, type, reporting_manager):   
        days = ','.join(selected_days) if selected_days else None
        application = cls(
            Staff_ID=staff_id,
            Start_Date=start_date,
            End_Date=end_date,
            Status='Pending',  # Default status for new applications
            Time_Slot=time_slot,
            Type=type,
            Email=email,
            Reporting_Manager=reporting_manager,
            Days= days, # Convert list of days to a comma-separated string
            Reason=reason,
        )
        db.session.add(application)
        db.session.commit()
        
        return application
        
        
    @classmethod
    def searchForAvailableDates(cls, staff_id, start_date, end_date):

        try:

            start_date = datetime.strptime(start_date, '%Y-%m-%d')
            end_date = datetime.strptime(end_date, '%Y-%m-%d')

            # get avail dates within range that user inputted

            date_range = []
            current_date = start_date
            while current_date <= end_date:
                date_range.append(current_date)
                current_date += timedelta(days=1)

            # get all applications within the date range, if there are dates
            # where they alr applied, block it out and return other dates

            existing_applications = cls.query.filter(
                cls.staff_id == staff_id,
                cls.Start_Date <= end_date,
                cls.End_Date >= start_date
            ).all()

            for app in existing_applications:
                current_date = app.Start_Date
                while current_date <= app.End_Date:
                    if current_date in date_range:
                        date_range.remove(current_date)
                    current_date += timedelta(days=1)

            return [date.strftime('%Y-%m-%d') for date in date_range]


        except Exception as e:
            db.session.rollback()
            raise e

    @classmethod
    def displayAvailableDates(start_date, end_date):
            
        try:

            start_date = datetime.strptime(start_date, '%Y-%m-%d')
            end_date = datetime.strptime(end_date, '%Y-%m-%d')

            date_range = []
            current_date = start_date
            while current_date <= end_date:
                date_range.append(current_date)
                current_date += timedelta(days=1)

            return [date.strftime('%Y-%m-%d') for date in date_range]


        except Exception as e:
            db.session.rollback()
            raise e
        
# get arrangement for staff

    @classmethod
    def getAllArrangement(cls, staff_id, start_date, end_date):

        try:

            start_date = datetime.strptime(start_date, '%Y-%m-%d')
            end_date = datetime.strptime(end_date, '%Y-%m-%d')

            # get all applications within the date range
            applications = cls.query.filter(
                cls.staff_id == staff_id,
                cls.Start_Date <= end_date,
                cls.End_Date >= start_date
            ).all()

            return applications

        except Exception as e:
            db.session.rollback()
            raise e
        
    @classmethod
    def getArrangement(cls, staff_id, application_id):

        try:

            application = cls.query.filter(
                cls.staff_id == staff_id,
                cls.Application_ID == application_id
            ).first()

            return application

        except Exception as e:
            db.session.rollback()
            raise e