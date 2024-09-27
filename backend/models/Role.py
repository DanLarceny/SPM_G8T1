from sqlalchemy import CheckConstraint
from extensions import db

class Role(db.Model):
    __tablename__ = "Role"
    
    Role = db.Column(db.Integer, primary_key=True)
    Role_Name = db.Column(db.String(50), nullable=False)

    __table_args__ = (
        CheckConstraint('role >= 1 AND role <= 3', name='check_role_range'),
    )

    def __repr__(self):
        return f'<Role {self.role} - {self.roleName}>'
