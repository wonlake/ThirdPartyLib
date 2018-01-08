import os
import codecs

solution_name = input("Solution Name:")
if len(solution_name) == 0:
    solution_name = 'ThirdPartyLib'

pipe = os.popen("dir /B /AD")

with codecs.open("CMakeLists.txt", "w", "utf-8") as f:
    f.write(r'cmake_minimum_required (VERSION 3.6)' + '\n\n')
    f.write(r'project(' + solution_name + ')' + '\n\n')
    for proj in pipe.readlines():
        proj_name = proj.strip()
        if os.path.exists(proj_name + "/CMakeLists.txt"):
            f.write(r'add_subdirectory(' + proj_name + ')' + '\n')
pipe.close()
