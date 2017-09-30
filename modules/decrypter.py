import os, sys, hashlib, random, time
from functions import *
from helpers import *

working_dir = os.getcwd()
args = sys.argv

package = 0

if(os.path.isfile(args[1])):
	package = open(args[1], 'rb')
else:
	sys.exit(-1)
IV = package.read(64)
debuglog("IV is " + str(IV))
key = setupKey(args[2], IV)
checksum = list(applyXOR(bytearray(package.read(128)), key))
csgen = hashlib.sha512()
csgen.update(bytearray(checksum[:64]))
check = csgen.digest()
if(compareBytes(check, bytes(checksum[64:]))):
	print("Checksum validated")
else:
	debuglog("Checksum not valid, check your key")
	sys.exit(-1)
#Create Directory
dirLength = readSizeBytes(list(applyXOR(bytearray(package.read(4)), key)))
directory = list(applyXOR(bytearray(package.read(dirLength)), key))
dirIndex = 0
while(dirIndex < len(directory)):
	fnLength = directory[dirIndex]
	dirIndex = dirIndex+1
	name = ""
	for i in range(fnLength):
		name = name + chr(directory[dirIndex])
		dirIndex = dirIndex+1
	if(len(args) == 4):
		name = os.path.join(args[3], name)
	size = []
	for i in range(4):
		size.append(directory[dirIndex])
		dirIndex = dirIndex+1
	size = readSizeBytes(size)
	if(not os.path.dirname(name) == ''):
		os.makedirs(os.path.dirname(name), exist_ok=True)
	print("Writing to: " + name)
	output = open(name, 'wb')
	MAX_BUFFER_SIZE = 65535
	readCounter = 0
	while(readCounter < size):
		if(readCounter + MAX_BUFFER_SIZE > size):
			toWrite = applyXOR(bytearray(package.read(size-readCounter)), key)
			output.write(toWrite)
			readCounter = readCounter + size-readCounter
		else:
			toWrite = applyXOR(bytearray(package.read(MAX_BUFFER_SIZE)), key)
			output.write(toWrite)
			readCounter = readCounter + MAX_BUFFER_SIZE
	output.close()
#----------------