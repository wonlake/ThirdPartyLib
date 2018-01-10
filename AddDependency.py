import os
import codecs
import re

lines = []
if os.path.exists("CMakeLists.txt"):
	with codecs.open("CMakeLists.txt", "r", "utf-8") as f:
		for line in f.readlines():
			if not re.search("add_dependencies", line.strip(), re.I):
				lines.append(line)

	with codecs.open("CMakeLists.txt", "w", "utf-8") as f:
		lastline = ""
		for line in lines:
			f.write(line)
			lastline = line
		if lastline != "\n":
			f.write("\n")
		f.write("add_dependencies(libzzip libz)\n")
		f.write("add_dependencies(libfreeimage libjpeg libpng libtiff4 libz libopenexr libwebp libraw libjxr libopenjpeg)\n")
		f.write("add_dependencies(libil libz libpng libjpeg libtiff libmng liblcms libjasper)\n")
		f.write("add_dependencies(libilu libil)\n")
		f.write("add_dependencies(libilut libil libilu)\n")