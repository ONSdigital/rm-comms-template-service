import requests
from flask import json, current_app

headers = {'Content-type': 'application/json'}

# Script which adds new templates to the comms-service db along with the associated classifiers
# Run with the cmd pipenv run python scripts/config_comms_templates.py
with open('scripts/templates_to_load.json') as read_file:
    contents = json.load(read_file)

    region = "http://localhost:8182/classificationtypes/REGION"

    legal_basis = "http://localhost:8182/classificationtypes/LEGAL_BASIS"

    communication = "http://localhost:8182/classificationtypes/COMMUNICATION_TYPE"

    user = current_app.config['SECURITY_USER_NAME']
    pwd = current_app.config['SECURITY_USER_PASSWORD']

    requests.post(region, auth=(user, pwd), headers=headers)
    requests.post(legal_basis, auth=(user, pwd), headers=headers)
    requests.post(communication, auth=(user, pwd), headers=headers)

    for content in contents:
        url = "http://localhost:8182/templates"
        r = requests.post(url, json=content, auth=(user, pwd), headers=headers)

        print('Successfully added template')
