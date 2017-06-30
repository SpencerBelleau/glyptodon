import os, sys, hashlib, random, time
from functions import *
from helpers import *

args = sys.argv
fileList, pathList = createFileList(args[1])
#print(fileList)
#print(pathList)
key = setupKey(args[2])
#checksum-----------------------------------------
csgen = hashlib.sha512()
t = time.time()
random.seed(t)
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
	package.write(applyXOR(checksum, key))
	#create directory
	directoryBytes = bytearray()
	for i in range(len(fileList)):
		file = fileList[i]
		path = pathList[i]
		entryBytes = bytearray()
		fnlength = len(file)
		if(not os.path.isfile(args[1])):
			size = os.path.getsize(os.path.join(args[1], path))
		else:
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
	for i in range(len(fileList)):
		file = pathList[i]
		if(not os.path.isfile(args[1])):
			data = bytearray(open(os.path.join(args[1], file), 'rb').read())
		else:
			data = bytearray(open(os.path.join(file), 'rb').read())
		data = applyXOR(data, key)
		package.write(data)
	print("Successfully wrote to: " + packageName)
except Exception as e:
	print(e)
	raise Exception("TEST")
	package.close()
	os.remove(packageName)