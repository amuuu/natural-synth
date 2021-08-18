from flask import Blueprint, render_template
from flask_login import login_required, current_user
from . import db

from . import mqtthandler

main = Blueprint('main', __name__)

@main.route('/')
@login_required
def index():
    return render_template('index.html', email=current_user.email)

@main.route('/nodes', methods=['GET'])
def node_divs():
    return render_template('nodediv.html', node_info=mqtthandler.divs)