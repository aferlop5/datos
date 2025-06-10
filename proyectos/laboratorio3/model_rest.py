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
    params = {"token": token, "filter": filter}
    resp = requests.get(base + "/users", params=params)
    if resp.status_code < 300: return resp.json()
    else: raise Exception(resp.text)

def updateUser(token, user_data):
    # Se asume que el id del usuario es el token y se envía en la URL
    params = {"token": token}
    resp = requests.put(base + f"/users/{token}", json=user_data, params=params)
    if resp.status_code < 300: return resp.json()
    else: raise Exception(resp.text)

def removeUser(token):
    params = {"token": token}
    resp = requests.delete(base + f"/users/{token}", params=params)
    if resp.status_code < 300: return True
    else: raise Exception(resp.text)

def listFollowing(token, filter="", ini=0, count=10, sort=""):
    params = {"token": token, "filter": filter, "ini": ini, "count": count, "sort": sort}
    # Se obtiene la lista de following del usuario id=token
    resp = requests.get(base + f"/users/{token}/following", params=params)
    if resp.status_code < 300: return resp.json()
    else: raise Exception(resp.text)

def follow(token, nick):
    params = {"token": token}
    data = {"nick": nick}
    resp = requests.post(base + f"/users/{token}/following", json=data, params=params)
    if resp.status_code < 300: return True
    else: raise Exception(resp.text)

def unfollow(token, other_id):
    params = {"token": token}
    resp = requests.delete(base + f"/users/{token}/following/{other_id}", params=params)
    if resp.status_code < 300: return True
    else: raise Exception(resp.text)

def listFollowers(token, filter="", ini=0, count=10, sort=""):
    params = {"token": token, "filter": filter, "ini": ini, "count": count, "sort": sort}
    resp = requests.get(base + f"/users/{token}/followers", params=params)
    if resp.status_code < 300: return resp.json()
    else: raise Exception(resp.text)

def listTweets(token, filter="", ini=0, count=10, sort=""):
    params = {"token": token, "filter": filter, "ini": ini, "count": count, "sort": sort}
    resp = requests.get(base + "/tweets", params=params)
    if resp.status_code < 300: return resp.json()
    else: raise Exception(resp.text)

def getTweet(token, tweet_id):
    params = {"token": token}
    resp = requests.get(base + f"/tweets/{tweet_id}", params=params)
    if resp.status_code < 300: return resp.json()
    else: raise Exception(resp.text)

def addTweet(token, content):
    params = {"token": token}
    data = {"content": content}
    resp = requests.post(base + "/tweets", json=data, params=params)
    if resp.status_code < 300: return resp.json()
    else: raise Exception(resp.text)

def addRetweet(token, tweet_id):
    params = {"token": token}
    resp = requests.post(base + f"/tweets/{tweet_id}/retweets", params=params)
    if resp.status_code < 300: return resp.json()
    else: raise Exception(resp.text)

def listLikes(token, tweet_id, ini=0, count=10):
    params = {"token": token, "ini": ini, "count": count}
    resp = requests.get(base + f"/tweets/{tweet_id}/likes", params=params)
    if resp.status_code < 300: return resp.json()
    else: raise Exception(resp.text)

def like(token, tweet_id):
    params = {"token": token}
    resp = requests.post(base + f"/tweets/{tweet_id}/likes", params=params)
    if resp.status_code < 300: return True
    else: raise Exception(resp.text)

def listDislikes(token, tweet_id, ini=0, count=10):
    params = {"token": token, "ini": ini, "count": count}
    resp = requests.get(base + f"/tweets/{tweet_id}/dislikes", params=params)
    if resp.status_code < 300: return resp.json()
    else: raise Exception(resp.text)

def dislike(token, tweet_id):
    params = {"token": token}
    resp = requests.post(base + f"/tweets/{tweet_id}/dislikes", params=params)
    if resp.status_code < 300: return True
    else: raise Exception(resp.text)