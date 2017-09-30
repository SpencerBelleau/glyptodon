import os, sys, subprocess

args = sys.argv

###HELP STRINGS###
usage = '''\nUsage:\n  ''' + args[0]
##----------------------------------------------------------------------
default = usage + ''' <mode> [arguments for mode]

Modes:
  -e,  --encrypt       Encrypt file or directory into package
  -d,  --decrypt       Decrypt package and unpack
  -s,  --scan          Scans a package to determine its contents
  
Entering a mode with no arguments will display help for that mode'''
##----------------------------------------------------------------------
encHelp = usage + ''' -e <file/directory> key [packagename]

Description:
  Encrypts file or directory into package

Arguments:
  <file/directory>     Path to a file or directory
  key                  String or path to key file
  packagename          Name of output package (optional, overrides default)'''
##----------------------------------------------------------------------
decHelp = usage + ''' -d packagename key [path]

Description:
  Decrypts package and unpacks it

Arguments:
  packagename          Package name to unpack
  key                  String or path to key file
  path                 Location to place unpacked file(s) (optional, overrides default)'''
##----------------------------------------------------------------------
scnHelp = usage + ''' -s packagename key

Description:
  Scans a package to determine its contents

Arguments:
  packagename          Package name to unpack
  key                  String or path to key file'''
##----------------------------------------------------------------------

#prepare to launch something using subprocess
command = [sys.executable]
for x in args[1:]:
	command.append(x)
###LOGIC###
if(len(args) == 1):
	print(default)
	os._exit(1)
if(command[1] == "-e" or command[1] == "--encrypt"):
	if(len(args) == 2):
		print(encHelp)
	elif(len(args) > 5 or len(args) == 3):
		print("Invalid number of arguments. Type 'py " + args[0] + " " + command[1] + "' for help")
	else:
		command[1] = 'modules\\encrypter.py'
		subprocess.call(command)
		pass
elif(command[1] == "-d" or command[1] == "--decrypt"):
	if(len(args) == 2):
		print(decHelp)
	elif(len(args) > 5 or len(args) == 3):
		print("Invalid number of arguments. Type 'py " + args[0] + " " + command[1] + "' for help")
	else:
		command[1] = 'modules\\decrypter.py'
		subprocess.call(command)
		pass
elif(command[1] == "-s" or command[1] == "--scan"):
	if(len(args) == 2):
		print(scnHelp)
	elif(len(args) > 4 or len(args) == 3):
		print("Invalid number of arguments. Type 'py " + args[0] + " " + command[1] + "' for help")
	else:
		command[1] = 'modules\\scanner.py'
		subprocess.call(command)
		pass
else:
	print("Invalid Mode.")
	print(default)