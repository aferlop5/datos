import model_rest as rest  # Para operaciones síncronas (login, listas)
import model_mq as mq      # Para operaciones asíncronas (crear/actualizar)

def help():
    print('''
Available commands:
    - help
    - exit
    - addUser <name> <surname> <email> <password> <nick>
    - login <email> <password>
    - updateUser <name> <surname> <email> <password> <nick> (usa "-" para no modificar un campo)
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
            mq.addUser(user)  # Operación asíncrona
            print("Solicitud de registro en cola (asíncrona)")

        elif cmd[0] == "login":
            if len(cmd) < 3:
                print("ERROR: Missing parameters for login")
                continue
            token = rest.login(cmd[1], cmd[2])
            print("Welcome!")

        elif cmd[0] == "updateUser":
            if token is None:
                print("ERROR: You must log in first.")
                continue
            if len(cmd) < 6:
                print("ERROR: Missing parameters for updateUser")
                continue
            new_data = {}
            fields = ["name", "surname", "email", "password", "nick"]
            for i, field in enumerate(fields, start=1):
                if cmd[i] != "-":
                    new_data[field] = cmd[i]
            mq.updateUser(token, new_data)
            print("Solicitud de updateUser en cola.")

        elif cmd[0] == "removeUser":
            if token is None:
                print("ERROR: You must log in first.")
                continue
            mq.removeUser(token)
            token = None
            print("Solicitud de removeUser en cola.")

        elif cmd[0] == "listUsers":
            if token is None:
                print("ERROR: You must log in first.")
                continue
            query = cmd[1] if len(cmd) > 1 else ""
            users = rest.listUsers(token, query)
            for user in users:
                print("- " + str(user))

        elif cmd[0] == "follow":
            if token is None:
                print("ERROR: You must log in first.")
                continue
            if len(cmd) < 2:
                print("ERROR: Missing parameter for follow")
                continue
            mq.follow(token, cmd[1])
            print("Solicitud de follow en cola.")

        elif cmd[0] == "unfollow":
            if token is None:
                print("ERROR: You must log in first.")
                continue
            if len(cmd) < 2:
                print("ERROR: Missing parameter for unfollow")
                continue
            mq.unfollow(token, cmd[1])
            print("Solicitud de unfollow en cola.")

        elif cmd[0] == "listFollowing":
            if token is None:
                print("ERROR: You must log in first.")
                continue
            query = cmd[1] if len(cmd) > 1 else ""
            users = rest.listFollowing(token, query)
            for user in users:
                print("- " + str(user))

        elif cmd[0] == "listFollowers":
            if token is None:
                print("ERROR: You must log in first.")
                continue
            query = cmd[1] if len(cmd) > 1 else ""
            users = rest.listFollowers(token, query)
            for user in users:
                print("- " + str(user))

        elif cmd[0] == "addTweet":
            if token is None:
                print("ERROR: You must log in first.")
                continue
            content = " ".join(cmd[1:])
            mq.addTweet(token, content)  # Operación asíncrona
            print("Tweet en cola de procesamiento")

        elif cmd[0] == "addRetweet":
            if token is None:
                print("ERROR: You must log in first.")
                continue
            if len(cmd) < 2:
                print("ERROR: Missing tweetId for addRetweet")
                continue
            mq.addRetweet(token, cmd[1])
            print("Solicitud de addRetweet en cola.")

        elif cmd[0] == "listTweets":
            if token is None:
                print("ERROR: You must log in first.")
                continue
            query = cmd[1] if len(cmd) > 1 else ""
            tweets = rest.listTweets(token, query)
            for tweet in tweets:
                print("- " + str(tweet))

        elif cmd[0] == "like":
            if token is None:
                print("ERROR: You must log in first.")
                continue
            if len(cmd) < 2:
                print("ERROR: Missing tweetId for like")
                continue
            mq.like(token, cmd[1])
            print("Solicitud de like en cola.")

        elif cmd[0] == "dislike":
            if token is None:
                print("ERROR: You must log in first.")
                continue
            if len(cmd) < 2:
                print("ERROR: Missing tweetId for dislike")
                continue
            mq.dislike(token, cmd[1])
            print("Solicitud de dislike en cola.")

        elif cmd[0] == "listLikes":
            if token is None:
                print("ERROR: You must log in first.")
                continue
            if len(cmd) < 2:
                print("ERROR: Missing tweetId for listLikes")
                continue
            users = rest.listLikes(token, cmd[1])
            for user in users:
                print("- " + str(user))

        elif cmd[0] == "listDislikes":
            if token is None:
                print("ERROR: You must log in first.")
                continue
            if len(cmd) < 2:
                print("ERROR: Missing tweetId for listDislikes")
                continue
            users = rest.listDislikes(token, cmd[1])
            for user in users:
                print("- " + str(user))

        else:
            help()

    except Exception as e:
        print(f"ERROR: {e}")
