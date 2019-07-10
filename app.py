def ADD_USER_RATING(username, rating, url):
	f = open("userStuff.txt", "r", encoding = "utf-8")
	contents = f.readlines()
	f.close()
	userFound = False;
	i = 0

	# find username
	for i in range(len(contents)):
		if contents[i].count("#") != 2:
			continue
		if ("##" + username) == contents[i].strip():
			print(username + " in position " + str(i)) 
			userFound = True
			break
		# stop once we go past potential usernames
		if LESS_THAN(("##" + username), contents[i].strip()):
			print(("##" + username) + " is less than " + contents[i].strip())
			break

	reviews = list()
	ratingIndex = -1

	if userFound:
		ratingIndex = i + 1

		# get the first review column
		firstReviewIndex = i + 4
		firstReview = contents[firstReviewIndex].strip()
		firstReview = firstReview.replace(" ", "")
		#print(firstReview)
		ratingNum = list(filter(None, firstReview.split("|")))[0]
		#print("Rating is [" + ratingNum + "]")

		# find the last review, get how many reviews total
		numOfReviews = 0

		while contents[firstReviewIndex + numOfReviews].find("|") != -1:
			#print(contents[firstReviewIndex + numOfReviews])
			reviews.append(((contents[firstReviewIndex + numOfReviews].strip()).replace(" ", "")).split("|")[1])
			#print("{" + ((contents[firstReviewIndex + numOfReviews].strip()).replace(" ", "")).split("|")[1] + "}")
			numOfReviews += 1
		
		insertionIndex = firstReviewIndex + len(reviews)
		print("insert new row at index " + str(insertionIndex))
		s = "| " + rating + " | " + url + " |\r\n"
		contents.insert(insertionIndex, s)

	if not userFound:
		print("USER [" + username + "] NOT FOUND")
		print("we're at index " + str(i))
		insertionIndex = i - 1;
		print("insert new row at index " + str(insertionIndex))
		text = list()
		text.append("\r\n##" + username + "\r\n")
		text.append("###" + GET_FLAIR_TEXT(float(rating), 1) + "\r\n")
		text.append("| Rating | Comments |\r\n")
		text.append("|--------|:-------|\r\n")
		text.append("| " + rating + " | " + url + " |\r\n")
		
		print("-----")
		for s in text:
			print(s, end='')
		print("-----")
		
		for s in reversed(text):
			contents.insert(insertionIndex, s)

		ratingIndex = insertionIndex + 1

	print("rating index " + str(ratingIndex) + " : " + contents[ratingIndex])

	# add current review
	reviews.append(rating)

	print("USER [" + username + "] HAS [" + str(len(reviews)) + "] REVIEWS")

	# calculate average
	avgRating = 0
	for review in reviews:
		avgRating += float(review)
	
	avgRating /= len(reviews)

	flairText = GET_FLAIR_TEXT(avgRating, len(reviews))

	print("USER [" + username + "] HAS RATING [" + flairText + "]")

	contents[ratingIndex] = contents[ratingIndex].replace(contents[ratingIndex], "###" + flairText + "\n")

	f = open("userStuff.txt", "wb")
	contents = "".join(contents)
	f.write(contents.encode("utf-8"))
	f.close()

def GET_FLAIR_TEXT(rating, trades):
	flairText = ""
	roundedNum = round(rating + 0.0000001) # adding 0.0000001 because Python is stupid and does stupid rounding. Like all its stupid everything. SURPRISE!!

	for i in range(roundedNum):
		flairText += "\u2605"
	for i in range(5 - roundedNum):
		flairText += "\u2606"

	number = str(int(rating)) if rating.is_integer() else str(round(rating, 2))

	flairText += "(" + number + ", " + str(trades) + (" trades" if trades > 1 else " trade") + ")"

	return flairText

def LESS_THAN(a, b):
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

def GET_COMMAND():
	while True:
		userInput = input("Enter USER RATING URL: ")
		if userInput != "":
			userInput = userInput.split()
			if len(userInput) != 3:
				print("ERROR: invalid arguments")
				continue
			redditor = userInput[0]
			rating = userInput[1]
			if float(rating) < 1 or float(rating) > 5:
				print("ERROR: rating must be between 1 and 5")
				continue
			url = userInput[2]
			ADD_USER_RATING(redditor, rating, url)
		else:
			break

GET_COMMAND()