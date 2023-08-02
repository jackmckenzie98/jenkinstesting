# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import requests
import json
import os
import boto3

base_url = "https://debian-pingfed:9999/pf-admin-api/v1"

#Pull secret from secrets manager
def get_secret():
    secret_name = "debian-pf-api-secret"
    region_name = "us-east-1"
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )
    secret_response = client.get_secret_value(
        SecretId=secret_name
    )
    secrets = json.loads(secret_response['SecretString'])
    return secrets


with open("apiCalls.json") as f:
    endpoint = json.load(f)

session = requests.Session()
secrets = get_secret()
session.auth = (secrets["username"], secrets["pass"])
session.headers.update({'X-XSRF-Header': 'PingFederate'})
session.verify = False
#Create a directory for the artifacts in the current working directory
file_path = os.getcwd()
final_path = os.path.join(file_path, r'artifactsPull')
if not os.path.exists(final_path):
    os.makedirs(os.path.join(file_path, r'artifactsPull'))
def make_calls():
    global clients, spConnections, authPolicies, idpAdapters
    get_secret()
    clients = session.get(base_url + endpoint["oauthClients"]["endpoint"]).json()
    spConnections = session.get(base_url + endpoint["spConnections"]["endpoint"]).json()
    authPolicies = session.get(base_url + endpoint["authPolicies"]["endpoint"]).json()
    idpAdapters = session.get(base_url + endpoint["idpAdapters"]["endpoint"]).json()

def write_to_file():
    list_thing = [clients, spConnections, authPolicies, idpAdapters]
    file_names = ["clients", "spConnections", "authPolicies", "idpAdapters"]
    for name, obj in zip(file_names, list_thing):
        f = open(f"{final_path}/{name}.json", 'w+')
        f.write(json.dumps(obj, indent=3))
        f.close()
make_calls()
write_to_file()


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
