from flask import Flask
from extensions import db
from flask_cors import CORS
from dotenv import load_dotenv
import os
from config import DevelopmentConfig
from controllers.employee import employee_bp, schedule_bp, application_bp

# Load environment variables from .env file
load_dotenv()


def create_app(config_type=None):
    app = Flask(__name__)
    CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})
    # Set the config based on the provided argument or the FLASK_ENV environment variable
    
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

    # Register blueprints
    app.register_blueprint(employee_bp)
    app.register_blueprint(schedule_bp)
    app.register_blueprint(application_bp)

    @app.route('/')
    def welcome():
        return 'hi'
    
    
        

    return app


if __name__ == '__main__':
    app = create_app(DevelopmentConfig)
    port_num = os.getenv('FLASK_PORT')
    app.run(port=port_num, debug=True)
   
    
    