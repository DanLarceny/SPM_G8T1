from app import db  


class Role(db.Model):
    __tablename__ = "Role"
    
    role = db.Column(db.Integer, primary_key=True) 
    roleName = db.Column(db.String(50), nullable=False)  

    def __repr__(self):
        return f'<Role {self.role} - {self.roleName}>'
