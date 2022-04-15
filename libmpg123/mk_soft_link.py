import os
import sys

path = 'mpg123.h.in'
if not os.path.exists("include/" + path):
	os.system("mklink include\\" + path + " ..\\src\\libmpg123\\" + path)