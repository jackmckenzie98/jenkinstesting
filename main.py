# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import requests
import json
import os

base_url = "https://debian-pingfed:9999/pf-admin-api/v1"
with open("secrets.json") as f:
    secrets = json.load(f)

with open("apiCalls.json") as f:
    endpoint = json.load(f)

session = requests.Session()
session.auth = (secrets["username"], secrets["password"])
session.headers.update({'X-XSRF-Header': 'PingFederate'})
session.verify = False
file_path = 'C:/Users/jack.mckenzie/OneDrive - iC Consult Group GmbH/Documents/Projects/IRS/JackPythonPull'
def make_calls():
    global clients, spConnections, authPolicies, idpAdapters
    clients = session.get(base_url + endpoint["oauthClients"]["endpoint"]).json()
    spConnections = session.get(base_url + endpoint["spConnections"]["endpoint"]).json()
    authPolicies = session.get(base_url + endpoint["authPolicies"]["endpoint"]).json()
    idpAdapters = session.get(base_url + endpoint["idpAdapters"]["endpoint"]).json()

def write_to_file():
    list_thing = [clients, spConnections, authPolicies, idpAdapters]
    file_names = ["clients", "spConnections", "authPolicies", "idpAdapters"]
    for name, obj in zip(file_names, list_thing):
        f = open(f"{file_path}/{name}.json", 'w+')
        f.write(json.dumps(obj, indent=3))
        f.close()
make_calls()
if not os.path.exists(file_path):
    os.mkdir('C:/Users/jack.mckenzie/OneDrive - iC Consult Group GmbH/Documents/Projects/IRS/JackPythonPull')
write_to_file()


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
