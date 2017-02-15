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
username = env.get('MFP_USERNAME')
password = env.get('MFP_PASSWORD')

### MFP
#######################################################
def init_mfp_client(uname, password):
    logging.info("Initialising MFP client...")
    return myfitnesspal.Client(uname, password)

def get_mfp_data(client, date):
    logging.info("Fetching data from MFP...")
    mfp_day = client.get_date(date)
    logging.info("MFP response: " + str(mfp_day))
    return mfp_day

def to_json(mfp_data):
    logging.info("Serializing as JSON...")
    payload = { "date": str(mfp_data.date), "totals": mfp_data.totals }
    return json.dumps(payload)

@route('/mfp/totals/<date>')
def totals(date):
    logging.info("Requesting totals for " + str(date))
    response.content_type = 'application/json'
    formatted_date = datetime.strptime(date, "%Y-%m-%d")
    mfp_data = get_mfp_data(mfp_client, formatted_date)
    return to_json(mfp_data)

### Connect to MFP
mfp_client = init_mfp_client(username, password)

### Start the server
run(host='0.0.0.0', port=argv[1])

