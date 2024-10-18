from flask import Flask, Blueprint, jsonify
from extensions import db, create_engine_and_session
from flask_cors import CORS
from dotenv import load_dotenv
import os
from config import DevelopmentConfig
from controllers.employee import employee_bp
from controllers.WFHApplication import wfh_application_bp
from controllers.manager import manager_bp

# Load environment variables from .env file
load_dotenv()


def create_app(config_type=None):
    app = Flask(__name__)
    # Set the config based on the provided argument or the FLASK_ENV environment variable
    CORS(app,  resources={r"/*": {"origins": "http://localhost:3000"}})
    
    if config_type:
        app.config.from_object(config_type)
    else:
        env_config = os.getenv('FLASK_ENV', 'development')
        if env_config == 'development':
            app.config.from_object('config.DevelopmentConfig')
        else:
            app.config.from_object('config.TestingConfig')

    # Bind the app with SQLAlchemy
    db.init_app(app)
    engine, Session = create_engine_and_session(app)
    
     # Store session in app context for access in routes
    app.config['SESSION'] = Session

    # Register blueprints
    app.register_blueprint(employee_bp)
    app.register_blueprint(wfh_application_bp)
    app.register_blueprint(manager_bp)
    
    @app.teardown_appcontext
    def shutdown_session(exception=None):
        # Remove the session to ensure it is properly closed
        Session.remove()

    @app.route('/')
    def welcome():
        return 'hi'
    
 
        

    return app


if __name__ == '__main__':
    app = create_app(DevelopmentConfig)
    port_num = os.getenv('FLASK_PORT')
    app.run(port=port_num, debug=True)
   
    
    