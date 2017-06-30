import os, sys, hashlib
from helpers import *

debug = False

def debuglog(s):
	if(debug):
		print(s)

def getKeyBytes(argument):
	if(os.path.isfile(argument)):
		debuglog("It's a file")
		f = open(argument, 'rb')
		fileBytes = f.read()
		debuglog(str(fileBytes))
		return fileBytes
	else:
		debuglog("It's not a file")
		debuglog(argument.encode('utf-8'))
		return argument.encode('utf-8')

def createFileList(fileArg):
	fileList = []
	pathList = []
	#sanity checks
	if(os.path.isfile(fileArg)):
		pathList.append(fileArg)
		fileList.append(os.path.split(fileArg)[1])
	elif(os.path.isdir(fileArg)):
		for path, _, files in os.walk(fileArg):
			for i in files:
				if(os.path.isfile(os.path.join(path, i))):
					#print(os.path.join(path, i).replace(fileArg+os.sep, ""))
					pathList.append(os.path.join(path, i))
					fileList.append(os.path.join(path, i).replace(fileArg+os.sep, ""))
	else:
		sys.exit(-1)
	return fileList, pathList

def setupKey(keyArg):
	kb = getKeyBytes(keyArg)
	sha512 = hashlib.sha512()
	sha512.update(kb)
	kb = sha512.digest()
	l = []
	for i in kb:
		l.append(int(i))
	key = SHK(l)
	return key

def applyXOR(s, k):#bytearray, RC4/SHK
	for i in range(len(s)):
		s[i] = s[i]^k.getByte()
	return s
	
def XORbyte(b, k):
	return b^k.getByte()
	
def byteArrayAppend(a, b):
	for i in b:
		a.append(i)
	return a

def breakDownSize(l):
	m = 0
	h = 0
	rh = 0
	while l > 255:
		l = l - 256
		m = m + 1
		if(m > 255):
			m = 0
			h = h + 1
			if(h > 255):
				h = 0
				rh = rh + 1
	return [l, m, h, rh]

def readSizeBytes(l):
	return (l[0]) + (l[1]*256) + (l[2]*256*256) + (l[3]*256*256*256)

def compareBytes(b1, b2):
	for i in range(len(b1)):
		if(not b1[i] == b2[i]):	
			return False
	return True