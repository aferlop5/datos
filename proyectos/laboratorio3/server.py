import model as model
from flask import Flask, request
app = Flask(__name__)

@app.route('/twitter/users', methods=['POST'])
def addUser(): 
    user = request.get_json()
    user = model.addUser(user)
    return user

@app.route('/twitter/sessions', methods=['POST'])
def login():
    creds = request.get_json()
    try:
        token = model.login(creds['email'], creds['password'])
        return {'token': token}
    except Exception as exc:
        return str(exc), 401

@app.route('/twitter/users')
def listUsers():
    token = request.args.get('token')
    filter = request.args.get('filter')
    try:
        return model.listUsers(token, filter)
    except Exception as exc:
        return str(exc), 400

@app.route('/twitter/users/<id>', methods=['GET'])
def getUser(id):
    token = request.args.get('token')
    try:
        users = model.listUsers(token, f"{{'id': '{id}'}}")
        if users:
            return users[0]
        return "User not found", 404
    except Exception as exc:
        return str(exc), 400

@app.route('/twitter/users/<id>', methods=['PUT'])
def updateUser(id):
    token = request.args.get('token')
    if token != id:
        return "Unauthorized", 401
    user_data = request.get_json()
    try:
        updated_user = model.updateUser(token, user_data)
        return updated_user
    except Exception as exc:
        return str(exc), 400

@app.route('/twitter/users/<id>', methods=['DELETE'])
def removeUser(id):
    token = request.args.get('token')
    if token != id:
        return "Unauthorized", 401
    try:
        model.removeUser(token)
        return "", 204
    except Exception as exc:
        return str(exc), 400

@app.route('/twitter/users/<id>/following', methods=['GET'])
def listFollowing(id):
    token = request.args.get('token')
    filter = request.args.get('filter', "")
    ini = int(request.args.get('ini', 0))
    count = int(request.args.get('count', 10))
    sort = request.args.get('sort', "")
    try:
        return model.listFollowing(token, filter, ini, count, sort)
    except Exception as exc:
        return str(exc), 400

@app.route('/twitter/users/<id>/following', methods=['POST'])
def follow(id):
    token = request.args.get('token')
    if token != id:
        return "Unauthorized", 401
    data = request.get_json()
    try:
        model.follow(token, data['nick'])
        return "", 204
    except Exception as exc:
        return str(exc), 400

@app.route('/twitter/users/<id>/following/<other_id>', methods=['DELETE'])
def unfollow(id, other_id):
    token = request.args.get('token')
    if token != id:
        return "Unauthorized", 401
    try:
        users = model.listUsers(token, f"{{'id': '{other_id}'}}")
        if not users:
            return "User to unfollow not found", 404
        model.unfollow(token, users[0]['nick'])
        return "", 204
    except Exception as exc:
        return str(exc), 400

@app.route('/twitter/users/<id>/followers', methods=['GET'])
def listFollowers(id):
    token = request.args.get('token')
    filter = request.args.get('filter', "")
    ini = int(request.args.get('ini', 0))
    count = int(request.args.get('count', 10))
    sort = request.args.get('sort', "")
    try:
        return model.listFollowers(token, filter, ini, count, sort)
    except Exception as exc:
        return str(exc), 400

@app.route('/twitter/tweets', methods=['GET'])
def listTweets():
    token = request.args.get('token')
    filter = request.args.get('filter', "")
    ini = int(request.args.get('ini', 0))
    count = int(request.args.get('count', 10))
    sort = request.args.get('sort', "")
    try:
        return model.listTweets(token, filter, ini, count, sort)
    except Exception as exc:
        return str(exc), 400

@app.route('/twitter/tweets/<id>', methods=['GET'])
def getTweet(id):
    token = request.args.get('token')
    try:
        tweets = model.listTweets(token, f"{{'id': '{id}'}}")
        if tweets:
            return tweets[0]
        return "Tweet not found", 404
    except Exception as exc:
        return str(exc), 400

@app.route('/twitter/tweets', methods=['POST'])
def addTweet():
    token = request.args.get('token')
    data = request.get_json()
    try:
        return model.addTweet(token, data['content'])
    except Exception as exc:
        return str(exc), 400

@app.route('/twitter/tweets/<id>/retweets', methods=['POST'])
def addRetweet(id):
    token = request.args.get('token')
    try:
        return model.addRetweet(token, id)
    except Exception as exc:
        return str(exc), 400

@app.route('/twitter/tweets/<id>/likes', methods=['GET'])
def listLikes(id):
    token = request.args.get('token')
    ini = int(request.args.get('ini', 0))
    count = int(request.args.get('count', 10))
    try:
        return model.listLikes(token, id, ini, count)
    except Exception as exc:
        return str(exc), 400

@app.route('/twitter/tweets/<id>/likes', methods=['POST'])
def like(id):
    token = request.args.get('token')
    try:
        model.like(token, id)
        return "", 204
    except Exception as exc:
        return str(exc), 400

@app.route('/twitter/tweets/<id>/dislikes', methods=['GET'])
def listDislikes(id):
    token = request.args.get('token')
    ini = int(request.args.get('ini', 0))
    count = int(request.args.get('count', 10))
    try:
        return model.listDislikes(token, id, ini, count)
    except Exception as exc:
        return str(exc), 400

@app.route('/twitter/tweets/<id>/dislikes', methods=['POST'])
def dislike(id):
    token = request.args.get('token')
    try:
        model.dislike(token, id)
        return "", 204
    except Exception as exc:
        return str(exc), 400

if __name__ == '__main__':
    app.run(debug=True)

