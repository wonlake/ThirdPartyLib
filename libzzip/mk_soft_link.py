import os
	
path = 'zzip'
if not os.path.exists(path):
	os.system("mklink /D src\\" + path + " ..\\include")	