import argparse
import requests
import json

headers = {'Content-type': 'application/json'}

parser = argparse.ArgumentParser(description='Pass in a service URL, user & password')
default_url = parser.add_argument('default_url', help='Main URL')
arg_user = parser.add_argument('user', help='User')
arg_password = parser.add_argument('password', help='Pass')
args = parser.parse_args()

# Script which updates existing templates in the comms-service db
# Run with the cmd pipenv run python ./scripts/config_existing_comms_templates.py 'url', 'user', 'password'
with open('scripts/existing_templates.json') as existing_read_file:
    contents = json.load(existing_read_file)

arg_url = args.default_url
username = args.user
password = args.password

for content in contents:
    template_id = content['id']
    url = f'{arg_url}/templates/{template_id}'
    requests.put(url, json=content, auth=(username, password), headers=headers)

    print('Successfully updated template: ' + template_id + '\n')
