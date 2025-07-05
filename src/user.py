from flask import Blueprint
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

user_bp = Blueprint('user', __name__)

@user_bp.route('/user/ping')
def ping():
    return 'pong'
