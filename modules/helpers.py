class RC4(object):
	i = 0
	j = 0
	state = []
	stateLength = 0
	def __init__(self, data):
		self.state = data
		self.stateLength = len(data)
	def getByte(self):
		self.i = (self.i+1) % self.stateLength
		self.j = (self.j + self.state[self.i]) % self.stateLength
		
		self.state[self.i], self.state[self.j] = self.state[self.j], self.state[self.i]
		
		return self.state[(self.state[self.i]+self.state[self.j]) % self.stateLength]
	def setState(self, state):
		self.i = 0
		self.j = 0
		self.state = data
		self.stateLength = len(data)
	def __advance__(self):
		self.i = (self.i+1) % self.stateLength
		self.j = (self.j + self.state[self.i]) % self.stateLength
		
		self.state[self.i], self.state[self.j] = self.state[self.j], self.state[self.i]
	def advanceKey(self, cycles):
		for i in range(cycles):
			if(i%(1024*100)):
				print("Advancing key..." + str((i/cycles)*100) + "% \r", end="")
			self.__advance__()

#Split Hash Key, a method I made up that uses a lot of crypto hashing to create a relatively unpredictable key
## Start-->SHA512()----->1st half-->SHA512()-->Key(read until end)-->Append-->Send to start
##                 |                                                    ^
##                 ----->2nd half-->SHA512()-->Secret-------------------|
import hashlib
class SHK(object):
	K = 0
	S = 0
	i = 0
	def __init__(self, data): #data should be bytearray
		data = bytearray(data)
		h1 = data[:32]
		h2 = data[32:]
		sha512 = hashlib.sha512()
		sha512.update(bytes(h1))
		self.K = list(bytearray(sha512.digest()))
		sha512 = hashlib.sha512()
		sha512.update(bytes(h2))
		self.S = list(bytearray(sha512.digest()))
	def refreshKey(self):
		sha512 = hashlib.sha512()
		self.K.extend(self.S)
		data = bytearray(self.K)
		sha512.update(data)
		data = bytearray(sha512.digest())
		h1 = data[:32]
		h2 = data[32:]
		sha512 = hashlib.sha512()
		sha512.update(bytes(h1))
		self.K = list(bytearray(sha512.digest()))
		sha512 = hashlib.sha512()
		sha512.update(bytes(h2))
		self.S = list(bytearray(sha512.digest()))
	def getByte(self):
		ret = self.K[self.i]
		self.i = self.i+1
		if(self.i >= len(self.K)):
			self.refreshKey()
			self.i = 0
		return int(ret)