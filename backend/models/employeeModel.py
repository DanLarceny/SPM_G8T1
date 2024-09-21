from backend import db

class User(db.Model):

    __tablename__ = 'User'

# include subclass of type of employee - staff, managers and directors, hr and senior manager