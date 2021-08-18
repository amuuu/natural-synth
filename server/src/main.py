from flask import Blueprint, render_template, Response, request
from flask_login import login_required, current_user
from . import db

from . import mqtthandler

import json

main = Blueprint('main', __name__)

@main.route('/')
@login_required
def index():
    return render_template('index.html', email=current_user.email)

@main.route('/nodes', methods=['GET'])
def node_divs():
    return render_template('nodediv.html', node_info=mqtthandler.divs)

@main.route('/changename', methods=['POST'])
def change_name():
    try:
        data = request.json
        new_name = data.get('Data').get('new_name')
        device_name = data.get('Data').get('device_name')

        mqtthandler.peripheral_node_name_update(device_name, new_name)
    except:
        return Response("Error in changing name.", status=400)

    return Response("Name changed successfully.", status=200)

@main.route('/changeactiveself', methods=['POST'])
def change_activeself():
    try:
        data = request.json
        device_name = data.get('Data').get('device_name')
        activeself = data.get('Data').get('activeself')
        mqtthandler.peripheral_node_activeself_update(device_name, activeself)
    
    except:
        return Response("Error in changing activeself.", status=400)

    return Response("Activeself changed successfully.", status=200)

