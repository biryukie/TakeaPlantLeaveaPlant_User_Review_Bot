import praw
from time import sleep
from praw.models import Message
from enum import Enum

class Review(Enum):
    UNKNOWN = 0
    TRADE = 1
    SALE = 2

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

	# See if it is a trade, sale, or uknown
	reviewType = GET_REVIEW_TYPE(url)
	reviewTypeText = ""

	if reviewType == Review.TRADE:
		reviewTypeText = "Trade"
	elif reviewType == Review.SALE:
		reviewTypeText = "Sale"

	if userFound:
		ratingIndex = i + 1

		# get the first review column
		firstReviewIndex = i + 4

		# find the last review, get how many reviews total
		numOfReviews = 0

		while contents[firstReviewIndex + numOfReviews].find("|") != -1:
			reviews.append(((contents[firstReviewIndex + numOfReviews].strip()).replace(" ", "")).split("|")[1])  # [1] because Python likes to have [0] be newline. epic.
			storedUrl = ((contents[firstReviewIndex + numOfReviews].strip()).replace(" ", "")).split("|")[3]
			isUrlComment = -1
			isStoredComment = -1
			post1 = ""
			post2 = ""
			# set the given url to comment/submission/other
			try:
				post1 = reddit.comment(url = url)
				isUrlComment = 1
			except:
				try:
					post1 = reddit.submission(url = url)
					isUrlComment = 0
				except:
					isUrlComment = -1
			# set the stored url to comment/submission/other
			try:
				post2 = reddit.comment(url = storedUrl)
				isStoredComment = 1
			except:
				try:
					post2 = reddit.submission(url = storedUrl)
					isStoredComment = 0
				except:
					isStoredComment = -1
			# check if they're both a comment or a submission, then check if they're both the same or not
			if isUrlComment == 1 and isStoredComment == 1:  # both comments
				if post1.id == post2.id:
					print("    [!] NOTICE: Duplicate comment URL, not inputting review")
					result = "Your command was **not** executed, duplicate review submission. If this error is incorrect, please contact /u/eggpl4nt."
					return result
			if isUrlComment == 0 and isStoredComment == 0:  # both submissions
				if post1.id == post2.id:
					print("    [!] NOTICE: Duplicate submission URL, not inputting review")
					result = "Your command was **not** executed, duplicate review submission. If this error is incorrect, please contact /u/eggpl4nt."
					return result
			numOfReviews += 1
		
		insertionIndex = firstReviewIndex + len(reviews)

		# Insert a row into existing table.
		s = "|" + rating + "|" + reviewTypeText + "|" + url + "|\r\n"
		contents.insert(insertionIndex, s)

	if not userFound:
		print("    User [" + username + "] not found... creating section...")
		#print("we're at index " + str(i))
		insertionIndex = i - 1;
		#print("insert new row at index " + str(insertionIndex))
		text = list()
		text.append("\r\n##" + username + "\r\n")
		text.append("###" + GET_FLAIR_TEXT(float(rating), 1) + "\r\n")
		text.append("|Rating|Type|Comments|\r\n")
		text.append("|:-|:-|:-|\r\n")
		text.append("|" + rating + "|" + reviewTypeText + "|" + url + "|\r\n")
		
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
	userRatingText = GET_FLAIR_TEXT(avgRating, len(reviews))

	# get location text
	if contents[ratingIndex].find("|") != -1:
		locationText = contents[ratingIndex].split("|")[1].strip()
	else:
		locationText = ""

	flairText = userRatingText
	wikiText = userRatingText

	if locationText != "":
		wikiText = userRatingText + " | " + locationText
		flairText = userRatingText + " " + locationText

	print("    LOCATION = [" + locationText + "]")

	print("    User [" + username + "] now has rating [" + userRatingText + "]")

	print("    flair text = [" + flairText + "]")

	# update flair in wikipage
	contents[ratingIndex] = contents[ratingIndex].replace(contents[ratingIndex], "###" + wikiText + "\n")

	print("    Setting flair for [" + username + "]...")
	SET_FLAIR(username, flairText)

	contents = "".join(contents)

	# upload the updated wikipage
	print("    Uploading to [" + page.name + "]...")
	page.edit(contents, "Update user " + username + ".")
	print("    Finished uploading to [" + page.name + "]...")

	result = "Your command has been executed successfully."

	#leave a comment on the post
	comment = "Your review for `" + username + "` has been added to the [User Review Directory](https://www.reddit.com/r/TakeaPlantLeaveaPlant/wiki/userdirectory).\n\n----\n\n^([This is an automated message.])  \n[^(About User Reviews)](https://www.reddit.com/r/TakeaPlantLeaveaPlant/wiki/userreviews) ^(|) [^(User Review Directory)](https://www.reddit.com/r/TakeaPlantLeaveaPlant/wiki/userdirectory) ^(|) [^(Message the Moderation Team)](https://www.reddit.com/message/compose?to=%2Fr%2FTakeaPlantLeaveaPlant)"
	try:
		post = reddit.comment( url = url)
		post.reply(comment)
	except:
		try:
			post = reddit.submission(url = url)
			if reviewType == Review.TRADE:
				post.flair.select('78849dec-aa89-11e8-9f59-0e4fa42e5020', ':star: Trade Review')
			if reviewType == Review.SALE:
				post.flair.select('6c2e82e0-89d2-11ea-b090-0e642cf8d7e9', ':star: Sale Review')
			post.reply(comment)
		except:
			print("    [!] NOTICE: submission url invalid, could not leave a review confirmation comment.")
			result = "Your command has been executed successfully.\n\n**Notice:** Submission url was invalid, bot could not leave a review confirmation comment."
	
	return result

def GET_REVIEW_TYPE(url):
	"""Figures out which Review enum value the post/comment is.
	Args:
		url: the comment/post URL to examine
	Returns:
		The Review Enum value 
	"""
	try:
		comment = reddit.comment(url = url)
		#print("{" + comment.body + "}")
		if (str(comment.body)).strip().lower().startswith("[trade]"):
			return Review.TRADE
		if (str(comment.body)).strip().lower().startswith("[sales]"):
			return Review.SALE
	except:
		try:
			submission = reddit.submission(url = url)
			#print("{" + submission.link_flair_text + "}")
			if "Trade Review" in submission.link_flair_text:
				return Review.TRADE
			if "Sale Review" in submission.link_flair_text:
				return Review.SALE
		except:
			#print("submission unknown")
			return Review.UNKNOWN

	# Fall through to unknown
	return Review.UNKNOWN

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

def CHECK_PMS():
	mods = sub.moderator()
	while True:
		print("Checking pms...")
		#messages = self.r.get_unread()
		messages = reddit.inbox.unread()
		for item in messages:
			if isinstance(item, Message):
				if (item.author in mods):
					command = item.body
					print(command)
					VERIFY_COMMAND(item.author, command, item)
				else:
					print(item.author + " was not a moderator.")
			item.mark_read()
		sleep(15)

def VERIFY_COMMAND(sender, command, message):
	userInput = command.split()

	if len(userInput) != 3:
		message.reply("Command [" + command + "] had invalid arguments. Please check that you have [USERNAME RATING URL] and try again.")
		print("Invalid arguments, sending reply.")
		return

	redditor = userInput[0]

	try:
		reddit.redditor(redditor).id
	except:
		message.reply("Command [" + command + "]\n\nCould not find username [" + redditor + "], please verify correct username and try again.")
		print("Couldn't find user, sending reply.")
		return

	rating = userInput[1]

	try:
		if float(rating) < 0 or float(rating) > 5:
			message.reply("Command [" + command + "]\n\nRating must be between 0 and 5, please verify rating and try again.")
			print("Rating number incorrect, sending reply.")
			return
	except:
		message.reply("Command [" + command + "]\n\nRating must be between 0 and 5, please verify rating and try again.")
		print("Rating number incorrect, sending reply.")
		return

	url = userInput[2]
			
	reply = ADD_USER_RATING(redditor, rating, url)
	message.reply("Command [" + command + "]\n\n" + reply)
	print("Done with this message.")

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

		redditor = reddit.redditor(userInput[0])

		try:
			validCheck = redditor.id
		except:
			print("    [!] ERROR: could not find username [" + userInput[0] + "], please verify correct username")
			continue

		rating = userInput[1]

		try:
			if float(rating) < 0 or float(rating) > 5:
				print("    [!] ERROR: rating must be between 0 and 5")
				continue
		except:
			print("    [!] ERROR: rating must be between 0 and 5")
			continue

		url = userInput[2]
			
		ADD_USER_RATING(redditor.name, rating, url)

def SET_FLAIR(username, flairtext):
	redditUser = reddit.redditor(username)
	sub.flair.set(redditUser, "test", css_class = "userorange")  # this is because reddit's api is being weird and doing weird things...
	sub.flair.set(redditUser, flairtext, css_class = "usergreen")
	

def main():
	global reddit
	reddit = praw.Reddit(client_id = cid, client_secret = csc, password = pwd, user_agent = "/r/TakeaPlantLeaveaPlant Rating Bot by /u/eggpl4nt", username = usn)

	# test to make sure PRAW is working
	print(reddit.user.me().name + " is ready!")

	# set the sub to TakeaPlantLeaveaPlant
	global sub
	sub = reddit.subreddit("TakeaPlantLeaveaPlant")

	# perform commands
	#CHECK_PMS()
	GET_COMMANDS()

if __name__ == '__main__':
    main()
