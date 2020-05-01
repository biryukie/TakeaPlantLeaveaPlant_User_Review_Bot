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