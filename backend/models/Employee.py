from app import db  # Import the db instance

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
    role = db.Column(db.Integer, db.ForeignKey('Role.Role'))
    password = db.Column(db.String(50))

    def __repr__(self):
        return f"Employee({self.staff_id}, {self.staff_f_name}, {self.staff_l_name}, {self.role})"

    