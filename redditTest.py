import praw

credentials = open(open("loc.txt", "r").readline().strip(), "r")

id = credentials.readline().strip()
sc = credentials.readline().strip()
un = credentials.readline().strip()
pw = credentials.readline().strip()

reddit = praw.Reddit(client_id = id, client_secret = sc, password = pw, user_agent = "testscript by /u/eggpl4nt", username = un)

print(reddit.user.me())

page = reddit.subreddit("TakeaPlantLeaveaPlant").wiki["userdirectory"]

file = open("userStuff.txt", "wb")
file.write(page.content_md.encode("utf-8"))
file.close()