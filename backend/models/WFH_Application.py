from extensions import db
from models.Employee import Employee
from datetime import datetime, timedelta

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

    @classmethod
    def createApplication(cls, staff_id, start_date, end_date, time_slot, type, email, reporting_manager):

        try:
            start_date = datetime.strptime(start_date, '%Y-%m-%d')
            end_date = datetime.strptime(end_date, '%Y-%m-%d')

            if type == 'Recurring':
                #recurring is how recurring? 
                interval = timedelta(days=14)

                date_arr = []
                current_start_date = start_date
                
                while current_start_date <= end_date:
                    current_end_date = current_start_date + timedelta(days=13)
                    date_arr.append((current_start_date, current_end_date))
                    current_start_date += interval
                    
                for start, end in date_arr:

                    new_application = cls(
                        Staff_ID=staff_id,
                        Start_Date=start,
                        End_Date=end,
                        Time_Slot=time_slot,
                        Type=type,
                        Email=email,
                        Reporting_Manager=reporting_manager,
                        Status='Pending'  #new application->pending
                    )
                    db.session.add(new_application)
                    
            else:

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
    def displayAvailableDates():
            
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