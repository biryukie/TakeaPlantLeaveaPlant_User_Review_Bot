def INPUT():
	name = input("Enter a name: ")
	print("You wrote " + name)

def FILE_READING():
	f = open("test.txt" , 'r+')   
	# get array of lines
	file_Contents = f.readlines()
	print("file number of lines = " + str(len(file_Contents)))

	for x in file_Contents:
		print(x, end='')

	print()

def GET_USER_INFO(username):
	f = open("userStuff.txt", "r")
	contents = f.readlines()
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

	if not userFound:
		print("USER [" + username + "] NOT FOUND")
		print("we're at index " + str(i))
		# to do
		# find the place where to create a section for the new user
		# note! subtract 1 from the "i" value we find. otherwise we're on the username for the next thing.
		return

	print("USER [" + username + "] HAS [" + str(len(reviews)) + "] REVIEWS")

	# calculate average
	rating = 0
	for review in reviews:
		rating += int(review)
	
	rating /= len(reviews)

	print("USER [" + username + "] HAS RATING [" + (str(int(rating)) if rating.is_integer() else str(round(rating, 2))) + "]")

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
			#print(_a[i] + " is less than " + _b[i])
			return True
		if _a[i] > _b[i]:
			#print(_a[i] + " is greater than " + _b[i])
			return False

	if len(a) < len(b):
		return True
	else:
		return False

def ADD_USER_RATING(username, rating, url):
	print("ADDING user = [" + username + "], rating = [" + rating + "], url = [" + url + "]")
	GET_USER_INFO(username)

def GET_COMMAND():
	if "##Dog" < "##allguac420":
		print("yes")
	else:
		print("no")

	if LESS_THAN("##Dog", "##allguac420"):
		print("yes")
	else:
		print("no")

	while True:
		userInput = input("Enter USER RATING URL: ")
		if userInput != "":
			userInput = userInput.split()
			if len(userInput) != 3:
				print("ERROR: invalid arguments")
				continue
			redditor = userInput[0]
			rating = userInput[1]
			url = userInput[2]
			ADD_USER_RATING(redditor, rating, url)
			#GET_USER_INFO(userInput[0])
		else:
			break

def main():
	print("Starting main!")
	#FILE_READING()
	#INSERT_AFTER("banana", "peach")
	GET_USER_INFO("CatTut")
	while True:
		name = input("Enter a name: ")
		if name != "":
			GET_USER_INFO(name)
		else:
			break
	print("Exiting main! Goodbye!")

GET_COMMAND()