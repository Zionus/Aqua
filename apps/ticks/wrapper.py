from functools import wraps
def wrap(func):
	@wraps(func)
	call(*args,**kwargs):
		return func(*args,**kwargs)
	return call
#eval(str[,globals [,locals]])	
#compile(str,filename,kind),for compiler str into code snippet
'''
showall = lambda x: list(map(sys.stdout.write, x))

map,#works like apply
filter 
reduce,takes an iterator for processing.
from functools import reduce

def  corroutine(func):
	def start(*args,**kwargs):
		g = func(*args,**kwargs)
		g.__next__()
		return g
	return  start
	
@corroutine
def receiver():
	print('Ready')
	try:
		n = yield s
	except GeneratorExit:
		print('info')

def gensquares(N):
	for i in range(N):
		yield i** 2

G =  (c * 4 for c  in 'SPYDER')
list(G)

#tick
import time

reps = 1000
repslist = range(reps)

def timer(func,*pargs,**kargs):
	start = time.clock()
	for i in repslist:
		ret = func(*pargs,**kargs)
	elapsed = time.clock() - start
	return (elapsed,ret)

#class decorator

class  tracer:
	def __init__ (self,func):
		self.calls = 0
		self.func = func
	
	def __call__ (self,*args):
		self.calls += 1
		print('cll %s  to %s ' % (self.call,self.func.__name__))
		

def decorator(C):
	class Wrapper(*args):
		def __init__ (self,*args):
			self.wrapped  = C (*args)
	return Wrapper
	
class Wrapper:
	def decorator(C):
		def onCall(	*args):
			return Wrapper(C(*args))
		return Wrapper
	return onCall
	

	
		
'''

