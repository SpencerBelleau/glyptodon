import os, sys, hashlib, random, time
from functions import *
from helpers import *

args = sys.argv
t = time.time()
random.seed(t)

fileList, pathList = createFileList(args[1])
IVGen = hashlib.sha512()
IVGen.update(str(random.getrandbits(1024)).encode('utf-8'))
IV = IVGen.digest()
debuglog("IV is " + str(IV))
key = setupKey(args[2], IV)
#checksum-----------------------------------------
csgen = hashlib.sha512()
csgen.update(str(random.getrandbits(1024)).encode('utf-8'))
checksumP1 = csgen.digest()
csgen = hashlib.sha512()
csgen.update(checksumP1)
checksumP2 = csgen.digest()
checksum = bytearray(checksumP1)
for i in checksumP2:
	checksum.append(int(i))
#--------------------------------------------------
if(len(args) == 4):
	packageName = args[3]
else:
	packageName = list(str(time.time())[:10])
	random.shuffle(packageName)
	packageName = "gly" + ''.join(packageName)
try:
	package = open(packageName, 'wb')
	package.write(IV)
	package.write(applyXOR(checksum, key))
	#create directory
	directoryBytes = bytearray()
	for i in range(len(fileList)):
		file = fileList[i]
		path = pathList[i]
		entryBytes = bytearray()
		fnlength = len(file)
		size = os.path.getsize(path)
		size = breakDownSize(size)
		nameList = list(file)
		for i in range(len(nameList)):
			nameList[i] = ord(nameList[i])
		entryBytes.append(fnlength)
		byteArrayAppend(entryBytes, bytearray(nameList))
		byteArrayAppend(entryBytes,bytearray(size))
		byteArrayAppend(directoryBytes, entryBytes)
	dirSize = breakDownSize(len(directoryBytes))
	package.write(applyXOR(bytearray(dirSize), key))
	package.write(applyXOR(directoryBytes, key))
	#----------------
	#Append file content
	for i in range(len(pathList)):
		file = pathList[i]
		data = bytearray(open(os.path.join(file), 'rb').read())
		data = applyXOR(data, key)
		package.write(data)
	print("Successfully wrote to: " + packageName)
except Exception as e:
	print(e)
	raise Exception("TEST")
	package.close()
	os.remove(packageName)