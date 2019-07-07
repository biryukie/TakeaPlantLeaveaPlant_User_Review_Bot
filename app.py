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

def APPEND_DATA():
	f = open("test.txt", "r")
	contents = f.readlines()
	f.close()

	#contents.insert(index, value)
	contents.insert(1, "peach\n")

	f = open("test.txt", "w")
	contents = "".join(contents)
	f.write(contents)
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

	f = open("test.txt", "w")
	contents = "".join(contents)
	f.write(contents)
	f.close()

def main():
	print("Starting main!")
	#FILE_READING()
	INSERT_AFTER("banana", "peach")
	print("GOODBYE!")

if __name__ == "__main__":
    main()