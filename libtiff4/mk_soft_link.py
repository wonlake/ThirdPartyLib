import os
	
path = 'ZLib'
if not os.path.exists(path):
	os.system("mklink /D " + path + " ..\\" + "libz" + "\\include")

path = 'LibJPEG'
if not os.path.exists(path):
	os.system("mklink /D " + path + " ..\\" + path.lower() + "\\include")	