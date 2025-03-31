# cli.py
import model

def help():
    print('''
Available commands:
    - help
    - exit
    - addUser <name> <surname> <email> <password> <nick>
    - login <email> <password>
    - updateUser <name> <surname> <email> <password> <nick>
    - removeUser
    - listUsers [<query>]
    - follow <nick>
    - unfollow <nick>
    - listFollowing [<query>]
    - listFollowers [<query>]
    - addTweet <content>
    - addRetweet <tweetId>
    - listTweets [<query>]
    - like <tweetId>
    - dislike <tweetId>
    - listLikes <tweetId>
    - listDislikes <tweetId>
    ''')

token = None

while True:
    cmd = input("twitter > ").split(" ")
    if len(cmd) == 0 or len(cmd[0]) == 0:
        continue
    try:
        if cmd[0] == "help":
            help()
        elif cmd[0] == "exit":
            break

        elif cmd[0] == "addUser":
            if len(cmd) < 6:
                print("ERROR: Missing parameters for addUser")
                continue
            user = {
                "name": cmd[1],
                "surname": cmd[2],
                "email": cmd[3],
                "password": cmd[4],
                "nick": cmd[5]
            }
            model.addUser(user)
            print("User added.")

        elif cmd[0] == "login":
            if len(cmd) < 3:
                print("ERROR: Missing parameters for login")
                continue
            token = model.login(cmd[1], cmd[2])
            print("Welcome!")

        elif cmd[0] == "updateUser":
            if token is None:
                print("ERROR: You must log in first.")
                continue
            # Se esperan los 5 parámetros para actualizar (se pueden usar '-' para no modificar un campo)
            if len(cmd) < 6:
                print("ERROR: Missing parameters for updateUser")
                continue
            new_data = {}
            fields = ["name", "surname", "email", "password", "nick"]
            for i, field in enumerate(fields, start=1):
                if cmd[i] != "-":
                    new_data[field] = cmd[i]
            updated = model.updateUser(token, new_data)
            print("User updated:", updated)

        elif cmd[0] == "removeUser":
            if token is None:
                print("ERROR: You must log in first.")
                continue
            model.removeUser(token)
            token = None
            print("User removed.")

        elif cmd[0] == "listUsers":
            if token is None:
                print("ERROR: You must log in first.")
                continue
            query = cmd[1] if len(cmd) > 1 else ""
            users = model.listUsers(token, query)
            for user in users:
                print("- " + str(user))

        elif cmd[0] == "follow":
            if token is None:
                print("ERROR: You must log in first.")
                continue
            if len(cmd) < 2:
                print("ERROR: Missing parameter for follow")
                continue
            model.follow(token, cmd[1])
            print("Now following", cmd[1])

        elif cmd[0] == "unfollow":
            if token is None:
                print("ERROR: You must log in first.")
                continue
            if len(cmd) < 2:
                print("ERROR: Missing parameter for unfollow")
                continue
            model.unfollow(token, cmd[1])
            print("Unfollowed", cmd[1])

        elif cmd[0] == "listFollowing":
            if token is None:
                print("ERROR: You must log in first.")
                continue
            query = cmd[1] if len(cmd) > 1 else ""
            users = model.listFollowing(token, query)
            for user in users:
                print("- " + str(user))

        elif cmd[0] == "listFollowers":
            if token is None:
                print("ERROR: You must log in first.")
                continue
            query = cmd[1] if len(cmd) > 1 else ""
            users = model.listFollowers(token, query)
            for user in users:
                print("- " + str(user))

        elif cmd[0] == "addTweet":
            if token is None:
                print("ERROR: You must log in first.")
                continue
            # Todo lo que sigue se considera contenido del tweet
            content = " ".join(cmd[1:])
            tweet = model.addTweet(token, content)
            print("Tweet added:", tweet)

        elif cmd[0] == "addRetweet":
            if token is None:
                print("ERROR: You must log in first.")
                continue
            if len(cmd) < 2:
                print("ERROR: Missing tweetId for retweet")
                continue
            retweet = model.addRetweet(token, cmd[1])
            print("Retweet added:", retweet)

        elif cmd[0] == "listTweets":
            if token is None:
                print("ERROR: You must log in first.")
                continue
            query = cmd[1] if len(cmd) > 1 else ""
            tweets = model.listTweets(token, query)
            for tweet in tweets:
                print("- " + str(tweet))

        elif cmd[0] == "like":
            if token is None:
                print("ERROR: You must log in first.")
                continue
            if len(cmd) < 2:
                print("ERROR: Missing tweetId for like")
                continue
            model.like(token, cmd[1])
            print("Tweet liked.")

        elif cmd[0] == "dislike":
            if token is None:
                print("ERROR: You must log in first.")
                continue
            if len(cmd) < 2:
                print("ERROR: Missing tweetId for dislike")
                continue
            model.dislike(token, cmd[1])
            print("Tweet disliked.")

        elif cmd[0] == "listLikes":
            if token is None:
                print("ERROR: You must log in first.")
                continue
            if len(cmd) < 2:
                print("ERROR: Missing tweetId for listLikes")
                continue
            users = model.listLikes(token, cmd[1])
            for user in users:
                print("- " + str(user))

        elif cmd[0] == "listDislikes":
            if token is None:
                print("ERROR: You must log in first.")
                continue
            if len(cmd) < 2:
                print("ERROR: Missing tweetId for listDislikes")
                continue
            users = model.listDislikes(token, cmd[1])
            for user in users:
                print("- " + str(user))

        else:
            help()

    except Exception as e:
        print(f"ERROR: {e}")
