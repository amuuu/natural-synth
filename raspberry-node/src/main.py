from flask import Blueprint

main = Blueprint('main', __name__)

@main.route('/')
def flask_check():
    print("Flask is running...")
    return "<h1>Flask is running...</h1>"