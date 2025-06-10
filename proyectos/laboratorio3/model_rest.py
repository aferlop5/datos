import requests
base = "http://localhost:5000/twitter"

def addUser(user): 
    resp = requests.post(base + "/users", json=user)
    if resp.status_code < 300: return resp.json()
    else: raise Exception(resp.text)
    
def login(email, passwd): 
    creds = {'email': email, 'password': passwd}
    resp = requests.post(base + "/sessions", json=creds)
    if resp.status_code < 300: return resp.json()['token']
    else: raise Exception(resp.text)

def listUsers(token, filter=""):
    params = {"filter": filter}
    resp = requests.get(base + "/users", params=params)
    if resp.status_code < 300: return resp.json()
    else: raise Exception(resp.text)