import praw

global THE_FILE
THE_FILE = "userReviews_test_sept_2019.txt"

credentials = open(open("loc.txt", "r").readline().strip(), "r")

cid = credentials.readline().strip()
csc = credentials.readline().strip()
usn = credentials.readline().strip()
pwd = credentials.readline().strip()

def ADD_USER_RATING(username, rating, url):
	# get the wikipage
	directory = (GET_DIRECTORY(username[0].lower()))
	page = sub.wiki["userdirectory/" + directory]
	file = open(THE_FILE, "wb")
	file.write(page.content_md.encode("utf-8"))
	file.close()

	f = open(THE_FILE, "r", encoding = "utf-8")
	contents = f.readlines()
	f.close()

	userFound = False;
	i = 0

	# find username
	for i in range(len(contents)):
		if contents[i].count("#") != 2:
			continue
		if ("##" + username).lower() == (contents[i].strip()).lower():
			#print(username + " in position " + str(i)) 
			userFound = True
			break
		# stop once we go past potential usernames
		if LESS_THAN(("##" + username), contents[i].strip()):
			#print(("##" + username) + " is less than " + contents[i].strip())
			break

	reviews = list()
	ratingIndex = -1

	if userFound:
		ratingIndex = i + 1

		# get the first review column
		firstReviewIndex = i + 4

		# find the last review, get how many reviews total
		numOfReviews = 0

		while contents[firstReviewIndex + numOfReviews].find("|") != -1:
			reviews.append(((contents[firstReviewIndex + numOfReviews].strip()).replace(" ", "")).split("|")[1])  # [1] because Python likes to have [0] be newline. epic.
			numOfReviews += 1
		
		insertionIndex = firstReviewIndex + len(reviews)
		#print("insert new row at index " + str(insertionIndex))
		s = "|" + rating + "|" + url + "|\r\n"
		contents.insert(insertionIndex, s)

	if not userFound:
		print("    User [" + username + "] not found... creating section...")
		#print("we're at index " + str(i))
		insertionIndex = i - 1;
		#print("insert new row at index " + str(insertionIndex))
		text = list()
		text.append("\r\n##" + username + "\r\n")
		text.append("###" + GET_FLAIR_TEXT(float(rating), 1) + "\r\n")
		text.append("|Rating|Comments|\r\n")
		text.append("|:-|:-|\r\n")
		text.append("|" + rating + "|" + url + "|\r\n")
		
		for s in reversed(text):
			contents.insert(insertionIndex, s)

		ratingIndex = insertionIndex + 1

	# add current review
	reviews.append(rating)

	# calculate average
	avgRating = 0
	for review in reviews:
		avgRating += float(review)
	
	avgRating /= len(reviews)

	# get flair text
	flairText = GET_FLAIR_TEXT(avgRating, len(reviews))

	print("    User [" + username + "] now has rating [" + flairText + "]")

	# update rating in wikipage
	contents[ratingIndex] = contents[ratingIndex].replace(contents[ratingIndex], "###" + flairText + "\n")

	print("    Setting flair for [" + username + "]...")
	SET_FLAIR(username, flairText)

	contents = "".join(contents)

	# upload the updated wikipage
	print("    Uploading to [" + page.name + "]...")
	page.edit(contents, "Update user " + username + ".")
	print("    Finished uploading to [" + page.name + "]...")

	#leave a comment on the post
	comment = "Your **" + rating + "**-star review for **" + username + "** has been added to the [User Review Directory](https://www.reddit.com/r/TakeaPlantLeaveaPlant/wiki/userdirectory).\n\n----\n\n^([*I am a bot, this message was sent automatically.*])  \n[^(About User Reviews)](https://www.reddit.com/r/TakeaPlantLeaveaPlant/wiki/userreviews) ^(|) [^(User Review Directory)](https://www.reddit.com/r/TakeaPlantLeaveaPlant/wiki/userdirectory) ^(|) [^(Message the Moderation Team)](https://www.reddit.com/message/compose?to=%2Fr%2FTakeaPlantLeaveaPlant)"
	try:
		post = reddit.comment( url = url)
		post.reply(comment)
	except:
		try:
			post = reddit.submission(url = url)
			post.reply(comment)
		except:
			print("    [!] WARNING: submission url invalid, could not leave a review confirmation comment.")


def GET_FLAIR_TEXT(rating, trades):
	"""Generates the text to be used in a user's user flair.

	Args:
		rating: The average rating for the user (float).
		trades: The number of trades the user has done (int).

	Returns:
		A string in the format of "***** (X, Y trades)"

	"""
	flairText = ""
	roundedNum = round(rating + 0.0000001) # adding 0.0000001 because Python is stupid and does stupid rounding. Like all its stupid everything. SURPRISE!!

	# Append stars
	for i in range(roundedNum):
		flairText += "\u2605"
	# Append empty (no) stars
	for i in range(5 - roundedNum):
		flairText += "\u2606"

	number = str(int(rating)) if rating.is_integer() else str(round(rating, 2))

	flairText += " (" + number + ", " + str(trades) + (" trades" if trades > 1 else " trade") + ")"

	return flairText

def LESS_THAN(a, b):
	"""Used to sort username strings in alphanumeric order.

	Python's own comparator would say that "Zebra" is less than "apple."
	Length also needs to be taken into consideration, "Cat" is smaller than "Catty."

	Args:
		a: left string.
		b: right string.

	Returns:
		True if a is smaller than b, False otherwise.

	"""
	length = a if len(a) < len(b) else b

	_a = a.lower()
	_b = b.lower()

	for i in range(len(length)):
		if _a[i] < _b[i]:
			return True
		if _a[i] > _b[i]:
			return False

	if len(a) < len(b):
		return True
	
	return False

def GET_DIRECTORY(char): 
	if char == 'a':
		return "a"
	elif char == 'b':
		return "b"
	elif char == 'c':
		return "c"
	elif char == 'd':
		return "d"
	elif char == 'e':
		return "e"
	elif char == 'f':
		return "f"
	elif char == 'g':
		return "g"
	elif char == 'h':
		return "h"
	elif char == 'i':
		return "i"
	elif char == 'j':
		return "j"
	elif char == 'k':
		return "k"
	elif char == 'l':
		return "l"
	elif char == 'm':
		return "m"
	elif char == 'n':
		return "n"
	elif char == 'o':
		return "o"
	elif char == 'p':
		return "p"
	elif char == 'q':
		return "q"
	elif char == 'r':
		return "r"
	elif char == 's':
		return "s"
	elif char == 't':
		return "t"
	elif char == 'u':
		return "u"
	elif char == 'v':
		return "v"
	elif char == 'w':
		return "w"
	elif char == 'x':
		return "x"
	elif char == 'y':
		return "y"
	elif char == 'z':
		return "z"
	else:
		return "etc"

def GET_COMMANDS():
	while True:
		userInput = input("\nEnter USER RATING URL: ")

		# end program if no input
		if userInput == "":
			break

		userInput = userInput.split()
			
		if len(userInput) != 3:
			print("    [!] ERROR: invalid arguments")
			continue
		redditor = userInput[0]

		try:
			reddit.redditor(redditor).id
		except:
			print("    [!] ERROR: could not find username [" + redditor + "], please verify correct username")
			continue

		rating = userInput[1]
		if float(rating) < 0 or float(rating) > 5:
			print("    [!] ERROR: rating must be between 0 and 5")
			continue

		url = userInput[2]
			
		ADD_USER_RATING(redditor, rating, url)

def SET_FLAIR(username, flairtext):
	redditUser = reddit.redditor(username)
	sub.flair.set(redditUser, "test", css_class = "userorange")
	sub.flair.set(redditUser, flairtext, css_class = "usergreen")
	

def main():
	global reddit
	reddit = praw.Reddit(client_id = cid, client_secret = csc, password = pwd, user_agent = "/r/TakeaPlantLeaveaPlant Rating Bot by /u/eggpl4nt", username = usn)

	# test to make sure PRAW is working
	print(reddit.user.me())

	# set the sub to TakeaPlantLeaveaPlant
	global sub
	sub = reddit.subreddit("TakeaPlantLeaveaPlant")

	# perform commands
	GET_COMMANDS()

if __name__ == '__main__':
    main()
