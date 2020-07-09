import os
import asyncio
import utils

import discord
from discord.ext import commands

import praw
from praw.models import Message

from time import sleep
from enum import Enum

class Review(Enum):
    UNKNOWN = 0
    TRADE = 1
    SALE = 2

class Submission(Enum):
    INVALID = 0
    POST = 1
    COMMENT = 2

global THE_FILE
THE_FILE = "tempReviewWikipg.txt"

global FILE_LOCK
FILE_LOCK = asyncio.Lock()

credentials = open(open("loc.txt", "r").readline().strip(), "r")

cid = credentials.readline().strip()
csc = credentials.readline().strip()
usn = credentials.readline().strip()
pwd = credentials.readline().strip()

def ADD_USER_RATING(username, rating, url):
	# get the wikipage
	directory = (utils.GET_DIRECTORY(username[0].lower()))
	filepath = THE_FILE
	page = sub.wiki["userdirectory/" + directory]
	file = open(filepath, "wb")
	file.write(page.content_md.encode("utf-8"))
	file.close()

	f = open(filepath, "r", encoding = "utf-8")
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
		if utils.LESS_THAN(("##" + username), contents[i].strip()):
			#print(("##" + username) + " is less than " + contents[i].strip())
			break

	reviews = list()
	ratingIndex = -1

	# Check if the URL is valid and get the submission type
	submissionType = GET_SUBMISSION_TYPE(url)

	# See if the URL is a trade, sale, or unknown
	reviewType = GET_REVIEW_TYPE(url, submissionType)
	reviewTypeText = ""

	if reviewType == Review.TRADE:
		reviewTypeText = "Trade"
	elif reviewType == Review.SALE:
		reviewTypeText = "Sale"

	# Set the Comment or Submission object for the review we're inputting
	givenContent = "";

	if submissionType == Submission.COMMENT:
		givenContent = reddit.comment(url = url)
	if submissionType == Submission.POST:
		givenContent = reddit.submission(url = url)

	if userFound:
		ratingIndex = i + 1

		# get the first review column
		firstReviewIndex = i + 4

		# find the last review, get how many reviews total
		numOfReviews = 0

		while contents[firstReviewIndex + numOfReviews].find("|") != -1:
			reviews.append(((contents[firstReviewIndex + numOfReviews].strip()).replace(" ", "")).split("|")[1])  # [1] because Python likes to have [0] be newline. epic.
			storedUrl = ((contents[firstReviewIndex + numOfReviews].strip()).replace(" ", "")).split("|")[3]  # If more columns are ever added, be sure to update this index.
			storedContent = ""

			storedSubmissionType = GET_SUBMISSION_TYPE(storedUrl)

			if storedSubmissionType != Submission.INVALID and submissionType == storedSubmissionType:
				if storedSubmissionType == Submission.COMMENT:
					storedContent = reddit.comment(url = storedUrl)
					if givenContent.id == storedContent.id:
						print("    [!] NOTICE: Duplicate comment URL, not inputting review")
						result = "Your command was **not** executed, duplicate review submission. If this error is incorrect, please contact /u/eggpl4nt."
						return result
				if storedSubmissionType == Submission.POST:
					storedContent = reddit.submission(url = storedUrl)
					if givenContent.id == storedContent.id:
						print("    [!] NOTICE: Duplicate submission URL, not inputting review")
						result = "Your command was **not** executed, duplicate review submission. If this error is incorrect, please contact /u/eggpl4nt."
						return result
			
			# Increase the count of reviews for this user
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

	print("    User [" + username + "] now has rating [" + userRatingText + "], location = [" + locationText + "]")

	print("    Flair text = [" + flairText + "]")

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
		if submissionType == Submission.COMMENT:
			givenContent.reply(comment)
		elif submissionType == Submission.POST:
			if reviewType == Review.TRADE:
				givenContent.flair.select('78849dec-aa89-11e8-9f59-0e4fa42e5020', ':star: Trade Review')
			if reviewType == Review.SALE:
				givenContent.flair.select('6c2e82e0-89d2-11ea-b090-0e642cf8d7e9', ':star: Sale Review')
			givenContent.reply(comment)
		else:
			print("    [!] NOTICE: submission url invalid, could not leave a review confirmation comment.")
			result = "Your command has been executed successfully.  \n**Notice:** Submission url was invalid, bot could not leave a review confirmation comment."
	except Exception as e:
		exceptionMsg = str(e)
		print("    [!] NOTICE: Error occurred during sending comment, could not leave a review confirmation comment.")
		print("        ERROR: " + exceptionMsg)
		result = "Your command has been executed successfully.  \n**Notice:** Error occurred during sending comment, bot could not leave a review confirmation comment.  \n**Error: **" + exceptionMsg

	return result

def GET_SUBMISSION_TYPE(url):
	try:
		comment = reddit.comment(url = url)
		return Submission.COMMENT
	except:
		try:
			submission = reddit.submission(url = url)
			return Submission.POST
		except:
			return Submission.INVALID

	# Fall through to invalid
	return Submission.INVALID

def GET_REVIEW_TYPE(url, submissionType):
	"""Figures out which Review enum value the post/comment is.
	Args:
		url: the comment/post URL to examine
		submissionType: the Enum Submission value
	Returns:
		The Review Enum value 
	"""
	if submissionType == Submission.INVALID:
		return Review.UNKNOWN

	if submissionType == Submission.COMMENT:
		try:
			comment = reddit.comment(url = url)
			commentBody = (str(comment.body)).strip().replace("\\","").replace("*","").replace("_","").lower()
			#print("{" + comment.body + "}")
			if commentBody.startswith("[trade]") or commentBody.startswith("(trade)"):
				return Review.TRADE
			if commentBody.startswith("[sale]") or commentBody.startswith("(sale)"):
				return Review.SALE
			if ("[trade]" in commentBody) or ("(trade)" in commentBody):
				return Review.TRADE
			if ("[sale]" in commentBody) or ("(sale)" in commentBody):
				return Review.SALE
		except:
			return Review.UNKNOWN

	if submissionType == Submission.POST:
		try:
			submission = reddit.submission(url = url)
			#print("{" + submission.link_flair_text + "}")
			if "Trade Review" in submission.link_flair_text:
				return Review.TRADE
			if "Sale Review" in submission.link_flair_text:
				return Review.SALE
		except:
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
					VERIFY_REDDIT_COMMAND(item.author, command, item)
				else:
					print(item.author + " was not a moderator.")
			item.mark_read()
		sleep(15)

def VERIFY_REDDIT_COMMAND(sender, command, message):
	userInput = command.split()

	if len(userInput) != 3:
		message.reply("Command [" + command + "] had invalid arguments. Please check that you have [USERNAME RATING URL] and try again.")
		print("Invalid arguments, sending reply.")
		return

	redditor = reddit.redditor(userInput[0])

	try:
		validCheck = redditor.id
	except:
		message.reply("Command [" + command + "]\n\nCould not find username [" + userInput[0] + "], please verify correct username and try again.")
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
			
	reply = ADD_USER_RATING(redditor.name, rating, url)
	message.reply("Command [" + command + "]\n\n" + reply)
	print("Done with this message.")

def GET_CONSOLE_COMMANDS():
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

		if not url.startswith("https://"):
			url = "https://" + url
			
		ADD_USER_RATING(redditor.name, rating, url)

def PROCESS_DISCORD_INPUT(username, rating, url):
	result = ""

	redditor = reddit.redditor(username)

	try:
		validCheck = redditor.id
	except:
		result = ":wilted_rose: Could not find username [`" + username + "`], please verify correct username and try again."
		#print(result)
		return result

	try:
		if float(rating) < 0 or float(rating) > 5:
			result = ":wilted_rose: Rating must be between 0 and 5, please verify rating and try again."
			#print(result)
			return result
	except:
			result = ":wilted_rose: Rating must be between 0 and 5, please verify rating and try again."
			#print(result)
			return result

	if not url.startswith("https://"):
		url = "https://" + url

	result = ":sunflower: " + ADD_USER_RATING(redditor.name, rating, url)
	#print(result)
	return result

def SET_FLAIR(username, flairtext):
	redditUser = reddit.redditor(username)
	#sub.flair.set(redditUser, "test", css_class = "userorange")  # this is because reddit's api is being weird and doing weird things...
	sub.flair.set(redditUser, flairtext, css_class = "usergreen")
	

def START_DISCORD_BOT():
	TOKEN = open(open("locd.txt", "r").readline().strip(), "r").readline().strip()

	bot = commands.Bot(command_prefix=',')

	@bot.command(name='r')
	@commands.has_role('plantfriend')
	async def inputReview(ctx, username: str, rating: str, url: str):
		result = ""
		async with FILE_LOCK:
			result = "`" + username + "` `" + rating + "` `" + url + "`\n" + await ctx.bot.loop.run_in_executor(None, PROCESS_DISCORD_INPUT, username, rating, url)

		await ctx.send(result)

	@inputReview.error
	async def inputReviewError(ctx, error):
		if isinstance(error, commands.errors.CheckFailure):
			await ctx.send(":wilted_rose: Sorry, you don't have permissions!")
		if isinstance(error, commands.errors.MissingRequiredArgument):
			await ctx.send(":wilted_rose: You are missing an argument:\n`input` `USERNAME` `RATING` `URL`.")
		if isinstance(error, commands.errors.BadArgument):
			await ctx.send(":wilted_rose: Ensure correct format:\n`input` `USERNAME` `RATING` `URL`.")

	bot.run(TOKEN)

def main():
	global reddit
	reddit = praw.Reddit(client_id = cid, client_secret = csc, password = pwd, user_agent = "/r/TakeaPlantLeaveaPlant Rating Bot by /u/eggpl4nt", username = usn)

	# Make sure PRAW is working
	print(reddit.user.me().name + " is ready!")

	# Set the sub to TakeaPlantLeaveaPlant
	global sub
	sub = reddit.subreddit("TakeaPlantLeaveaPlant")

	# Perform commands
	#CHECK_PMS()  # For server mode
	#GET_CONSOLE_COMMANDS()  # For manual mode
	START_DISCORD_BOT()

if __name__ == '__main__':
    main()
