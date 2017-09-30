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
key = setupKey(args[2], IV)
checksum = list(applyXOR(bytearray(package.read(128)), key))
csgen = hashlib.sha512()
csgen.update(bytearray(checksum[:64]))
check = csgen.digest()
if(compareBytes(check, bytes(checksum[64:]))):
	print("Checksum validated")
else:
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
	size = []
	for i in range(4):
		size.append(directory[dirIndex])
		dirIndex = dirIndex+1
	size = readSizeBytes(size)
	print("> " + name)