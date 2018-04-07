"""
def binarySearch(alist, item):
	first = 0
	last = len(alist) -1
	found = False

	while first <= last and not found:
		midpoint = (first + last)//2
		if alist[midpoint] == item:
			found = True
		else:
			if item < alist[midpoint]:
				last = midpoint - 1
			else:
				first = midpoint + 1
	return found

testList = [0,1,2,3,45,3,5,234]
print(binarySearch(testList, 3))
print(binarySearch(testList, 25))
"""
print(23 /2 )