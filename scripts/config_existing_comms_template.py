import requests
from flask import json, current_app

headers = {'Content-type': 'application/json'}

# Script which updates existing templates in the comms-service db
# Run with the cmd pipenv run python scripts/config_existing_comms_templates.py
with open('scripts/existing_templates.json') as existing_read_file:
    contents = json.load(existing_read_file)

    user = current_app.config['SECURITY_USER_NAME']
    pwd = current_app.config['SECURITY_USER_PASSWORD']

    for content in contents:
        template_id = content['id']
        url = "http://localhost:8182/templates/" + template_id
        r = requests.put(url, json=content, auth=(user, pwd), headers=headers)

        print('Successfully updated template: ' + template_id + '\n')
