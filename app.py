def FILE_READING():
	f = open("test.txt" , 'r+')   
	# get array of lines
	file_Contents = f.readlines()
	print("file number of lines = " + str(len(file_Contents)))

	for x in file_Contents:
		print(x, end='')

	print()

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
		stars = ""
		roundedNum = round(float(rating) + 0.0000001) # adding 0.0000001 because Python is stupid and does stupid rounding. Like all its stupid everything. SURPRISE!!
		for i in range(roundedNum):
			stars += "\u2605"
		for i in range(5 - roundedNum):
			stars += "\u2606"
		text.append("###" + stars + " (" + rating + ", 1 trade)\r\n")
		text.append("| Rating | Comments |\r\n")
		text.append("|--------|:-------|\r\n")
		text.append("| " + rating + " | " + url + " |\r\n")
		print("-----")
		for s in text:
			print(s, end='')
		print("-----")
		for s in reversed(text):
			contents.insert(insertionIndex, s)

	# add current review
	reviews.append(rating)

	print("USER [" + username + "] HAS [" + str(len(reviews)) + "] REVIEWS")

	# calculate average
	avgRating = 0
	for review in reviews:
		avgRating += float(review)
	
	avgRating /= len(reviews)

	print("USER [" + username + "] HAS RATING [" + (str(int(avgRating)) if avgRating.is_integer() else str(round(avgRating, 2))) + "]")

	f = open("userStuff.txt", "wb")
	contents = "".join(contents)
	f.write(contents.encode("utf-8"))
	f.close()

def INSERT_AFTER(keyword, value):
	f = open("test.txt", "r")
	contents = f.readlines()
	f.close()

	# find index
	for i in range(len(contents)):
		if keyword in contents[i]:
			print(keyword + " in position " + str(i)) 
			break

	print (str(i) + " & " + contents[i])

	if keyword not in contents[i]:
		print("Could not find this keyword: " + keyword)
		return

	contents.insert(i + 1, value + "\n")

	f = open("test.txt", "wb")
	contents = "".join(contents)
	f.write(contents.encode("utf-8"))
	f.close()

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