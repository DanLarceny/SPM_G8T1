from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

db = SQLAlchemy()

# Define the engine and session handling here
def create_engine_and_session(app):
    # Create the engine using the app config (e.g., from the DATABASE_URI)
    engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])

    # Create a session factory bound to the engine
    session_factory = sessionmaker(bind=engine)
    
    # Scoped session to ensure thread safety in web apps
    Session = scoped_session(session_factory)
    
    return engine, Session
