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

	if userFound is False:
		print("USER [" + username + "] NOT FOUND")
		return
	
	rating = contents[i + 1].rstrip()
	rating = rating.replace("#", "")

	print("USER [" + username + "] HAS RATING [" + rating + "]")

	# get the first review column
	firstReviewIndex = i + 4
	firstReview = contents[firstReviewIndex].strip()
	firstReview = firstReview.replace(" ", "")
	#print(firstReview)
	ratingNum = list(filter(None, firstReview.split("|")))[0]
	#print("Rating is [" + ratingNum + "]")

	# find the last review, get how many reviews total
	reviews = list()
	numOfReviews = 0
	while contents[firstReviewIndex + numOfReviews].find("|") != -1:
		#print(contents[firstReviewIndex + numOfReviews])
		reviews.append(((contents[firstReviewIndex + numOfReviews].strip()).replace(" ", "")).split("|")[1])
		#print("{" + ((contents[firstReviewIndex + numOfReviews].strip()).replace(" ", "")).split("|")[1] + "}")
		numOfReviews += 1

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

def GET_COMMAND():
	while True:
		userInput = input("Enter USER, RATING, URL: ")
		if userInput != "":
			userInput = userInput.split()
			GET_USER_INFO(userInput[0])
		else:
			break
	pass

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