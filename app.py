import datetime
import json
import logging
import myfitnesspal
from os import environ as env
from sys import argv
from datetime import datetime, date
from bottle import Bottle, route, run, response, request
################################################################################

### Setup logging
log_format = '===> [%(levelname)s] %(message)s'
logging.basicConfig(format=log_format, level=logging.INFO)

### Read env vars
username_a = env.get('MFP_USERNAME_A')
password_a = env.get('MFP_PASSWORD_A')
username_b = env.get('MFP_USERNAME_B')
password_b = env.get('MFP_PASSWORD_B')

### MFP
#######################################################
def init_mfp_client(uname, password):
    logging.info("Initialising MFP client for user: " + uname)
    return myfitnesspal.Client(uname, password)

def get_mfp_data(user, date):
    logging.info("Fetching data from MFP...")
    mfp_day = 'n/a'
    if user == 'a':
        mfp_day = mfp_client_a.get_date(date)
    elif user == 'b':
        mfp_day = mfp_client_b.get_date(date)
    logging.info("MFP response: " + str(mfp_day))
    return mfp_day

def to_json(mfp_data):
    logging.info("Serializing as JSON...")
    payload = { "date": str(mfp_data.date), "totals": mfp_data.totals }
    return json.dumps(payload)

@route('/mfp/<user>/totals/<date>')
def totals(user, date):
    logging.info("Requesting totals for " + str(date))
    response.content_type = 'application/json'
    formatted_date = datetime.strptime(date, "%Y-%m-%d")
    mfp_data = get_mfp_data(user, formatted_date)
    return to_json(mfp_data)


### Connect to MFP
mfp_client_a = init_mfp_client(username_a, password_a)
mfp_client_b = init_mfp_client(username_b, password_b)

### Start the server
run(host='0.0.0.0', port=argv[1])

