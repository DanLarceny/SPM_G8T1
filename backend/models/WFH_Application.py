from app import db  # Import the db instance

class WFHApplication(db.Model):
    __tablename__ = 'WFH_Application'
    
    application_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    staff_id = db.Column(db.Integer, db.ForeignKey('Employee.staff_id'))
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    status = db.Column(db.Enum('Pending', 'Rejected', 'Approved', 'Withdrawn'))
    time_slot = db.Column(db.Enum('AM', 'PM', 'Day'))
    email = db.Column(db.String(50))
    reporting_manager = db.Column(db.Integer, db.ForeignKey('Employee.staff_id'))
    role = db.Column(db.Integer, db.ForeignKey('Role.role_id'))

    employee = db.relationship('Employee', foreign_keys=[staff_id])
    reporting_manager_rel = db.relationship('Employee', foreign_keys=[reporting_manager])

    def __repr__(self):
        return f"WFHApplication({self.application_id}, {self.staff_id}, {self.status})"
    
    # can only be called by repoting_manager
    def approve(self):
        self.status = 'Approved'
        db.session.commit()
        
    # can only be called by repoting_manager
    def reject(self):
        self.status = 'Rejected'
        db.session.commit()
        
    # can only be called by staff who created this application
    def withdraw(self):
        if self.status == 'Pending':
            self.status = 'Withdrawn'
            db.session.commit()
        else:
            raise Exception("Only pending applications can be withdrawn.")
