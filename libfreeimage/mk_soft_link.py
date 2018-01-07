import os
import sys

path = 'LibJPEG'
if not os.path.exists("src/" + path):
	os.system("mklink /D src\\" + path + " ..\\..\\" + path.lower() + "\\include")

path = 'LibOpenJPEG'
if not os.path.exists("src/" + path):
	os.system("mklink /D src\\" + path + " ..\\..\\" + path.lower() + "\\include")
	
path = 'LibJXR'
if not os.path.exists("src/" + path):
	os.system("mklink /D src\\" + path + " ..\\..\\" + path.lower() + "\\include")
	
path = 'ZLib'
if not os.path.exists("src/" + path):
	os.system("mklink /D src\\" + path + " ..\\..\\" + "libz" + "\\include")
	
path = 'LibTIFF4'
if not os.path.exists("src/" + path):
	os.system("mklink /D src\\" + path + " ..\\..\\" + "libtiff4" + "\\include")
	
path = 'LibWebP'
if not os.path.exists("src/" + path):
	os.system("mklink /D src\\" + path + " ..\\..\\" + path.lower())
	
path = 'LibRawLite'
if not os.path.exists("src/" + path):
	os.system("mklink /D src\\" + path + " ..\\..\\" + "libraw" + "\\include")
	
path = 'OpenEXR'
if not os.path.exists("src/" + path):
	os.system("mklink /D src\\" + path + " ..\\..\\" + "libopenexr" + "\\src")
	
path = 'LibPNG'
if not os.path.exists("src/" + path):
	os.system("mklink /D src\\" + path + " ..\\..\\" + path.lower() + "\\include")