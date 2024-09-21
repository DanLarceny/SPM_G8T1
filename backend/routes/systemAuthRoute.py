from flask import Blueprint
from backend.controllers.registration import register_user

# Create a Blueprint for authentication
auth_bp = Blueprint('auth', __name__)

# Define the registration route
@auth_bp.route('/register', methods=['POST'])
def register():
    return register_user()
