import requests
from datetime import datetime, timedelta
from os import environ

from flask import Flask, send_file, request
from flask_httpauth import HTTPBasicAuth

SIM_ICCID = environ['SIM_ICCID']
LUNER_API_TOKEN = environ['LUNER_API_TOKEN']

app = Flask(__name__, static_folder='static')
auth = HTTPBasicAuth()

@auth.verify_password
def verify_password(username, password):
    if username == environ['USERNAME'] and password == environ['PASSWORD']:
        return username

last_request = None
last_send = None

state = dict(
    current_temp=None,
    target_temp=None,
    thermostat_enabled=None,
    timer_enabled=None,
    now=None,
    timer_millis=None,
    heating=None,
    relay=None,
    updated=None,
)


@app.route("/", methods=['GET'])
def index():
    return send_file("/app/index.html")

@app.route("/update", methods=['GET'])
@auth.login_required
def update():
    return send_file("/app/update.html")

@app.route("/state", methods=['GET'])
def get_state():
    return state

@app.route("/new_state/" + environ['COMM_TOKEN'], methods=['POST'])
def new_state():
    global state
    data = request.data.decode('utf-8')
    parts = data.split('/')
    state['current_temp'] = int(parts[0])
    state['target_temp'] = int(parts[1])
    state['thermostat'] = parts[2] == '1'
    state['timer'] = parts[3] == '1'
    state['now'] = parts[4]
    state['timer_millis'] = parts[5]
    state['heating'] = parts[6] == '1'
    state['relay'] = parts[7] == '1'
    state['updated'] = datetime.now().isoformat()
    return 'ok'

@app.route("/request_update", methods=['POST'])
@auth.login_required
def request_update():
    global last_request

    if last_request is None or datetime.now() - last_request > timedelta(0, 60):
        last_request = datetime.now()
    else:
        return 'not ok'

    requests.post(f'https://api.luner.io/assets/{SIM_ICCID}/sms', json={'dcs': 0, 'message': 'get'}, headers={'x-api-key': LUNER_API_TOKEN})

    return 'ok'

@app.route("/send/temp", methods=['POST'])
@auth.login_required
def send_temp():
    global last_send
    
    if last_send is None or datetime.now() - last_send > timedelta(0, 60):
        last_send = datetime.now()
    else:
        return 'not ok'

    value = request.data.decode('utf-8')
    temp_int = int(float(value) * 1000)
    if temp_int < 0 or temp_int > 30000:
        return 'temp error'
    command = 'set_temperature ' + str(temp_int)
    requests.post(f'https://api.luner.io/assets/{SIM_ICCID}/sms', json={'dcs': 0, 'message': command}, headers={'x-api-key': LUNER_API_TOKEN})

    return 'ok'

@app.route("/send/relay", methods=['POST'])
@auth.login_required
def send_relay():
    global last_send
    
    if last_send is None or datetime.now() - last_send > timedelta(0, 60):
        last_send = datetime.now()
    else:
        return 'not ok'

    value = request.data.decode('utf-8') == '1'
    command = 'relay_on' if value else 'relay_off'
    requests.post(f'https://api.luner.io/assets/{SIM_ICCID}/sms', json={'dcs': 0, 'message': command}, headers={'x-api-key': LUNER_API_TOKEN})

    return 'ok'


@app.route("/send/timer", methods=['POST'])
@auth.login_required
def send_timer():
    global last_send
    
    if last_send is None or datetime.now() - last_send > timedelta(0, 60):
        last_send = datetime.now()
    else:
        return 'not ok'
    
    value = request.data.decode('utf-8')
    minutes_int = int(value)
    if minutes_int < 0 or minutes_int > 65535:
        return 'time error'

    command = 'set_timer ' + value
    requests.post(f'https://api.luner.io/assets/{SIM_ICCID}/sms', json={'dcs': 0, 'message': command}, headers={'x-api-key': LUNER_API_TOKEN})

    return 'ok'

@app.route("/send/thermostat_enabled", methods=['POST'])
@auth.login_required
def send_thermostat_enabled():
    global last_send
    
    if last_send is None or datetime.now() - last_send > timedelta(0, 60):
        last_send = datetime.now()
    else:
        return 'not ok'

    value = request.data.decode('utf-8') == '1'
    command = 'thermostat_on' if value else 'thermostat_off'
    requests.post(f'https://api.luner.io/assets/{SIM_ICCID}/sms', json={'dcs': 0, 'message': command}, headers={'x-api-key': LUNER_API_TOKEN})

    return 'ok'