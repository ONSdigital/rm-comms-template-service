import argparse
import requests
import json

headers = {'Content-type': 'application/json'}

parser = argparse.ArgumentParser(description='Pass in a service URL, user & password')
default_url = parser.add_argument('default_url', help='Main URL')
arg_user = parser.add_argument('user', help='User')
arg_password = parser.add_argument('password', help='Pass')
args = parser.parse_args()


# Script which adds new templates to the comms-service db along with the associated classifiers
# Run with the cmd pipenv run python scripts/config_comms_templates.py 'url', 'user', 'password'
with open('scripts/templates_to_load.json') as read_file:
    contents = json.load(read_file)

arg_url = args.default_url
username = args.user
password = args.password
url = f'{arg_url}/templates'

region = f'{arg_url}/classificationtypes/REGION'

legal_basis = f'{arg_url}/classificationtypes/LEGAL_BASIS'

communication = f'{arg_url}/classificationtypes/COMMUNICATION_TYPE'

requests.post(region, auth=(username, password), headers=headers)
requests.post(legal_basis, auth=(username, password), headers=headers)
requests.post(communication, auth=(username, password), headers=headers)

for content in contents:
    r = requests.post(url, json=content,  auth=(username, password), headers=headers)

    print('Successfully added template')
