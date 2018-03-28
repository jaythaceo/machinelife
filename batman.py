# Fibonacci calculating 5 ways

# first using looping technique
def fib(n):
	a,b = 1,1
	for i in range(n-1):
		a,b = b, a + b
	return a
print fib(5)

## second using rescursion
def fibR(n):
	if n == 1 or n == 2:
		return 1
	return fibR(n-1) + fibR(n-2)
print fibR(5)

### third using generators
a,b = 0,1
def fib3():
	global a,b 
	while True:
		a,b = b, a+b
		yield a 
f=fib3()
f.next()
f.next()
f.next()
f.next()
print f.next()

#### using memoization
def memoize(fn, arg):
	memo = {}
	if arg not in memo:
		memo[arg] = fn(arg)
		return memo[arg]
