#! /usr/bin/python3

import os
import codecs
import re

projectName = input("Project Name:\n")
projectType = input("Project Type: static | shared | exe\n")
#projectName = "ssss"
#projectType = "shared"

print(projectName, projectType)

root = projectName
if not os.path.exists(root):
	os.makedirs(root)

include_dir = root + "/include"
if not os.path.exists(include_dir):
	os.makedirs(include_dir)

src_dir = root + "/src"
if not os.path.exists(src_dir):
	os.makedirs(src_dir)
	
build_dir = root + "/build"
if not os.path.exists(build_dir):
	os.makedirs(build_dir)
	
dummy_file = root + "/src/dummy.cpp"
if not os.path.exists(dummy_file):
	dummy_fd = codecs.open(dummy_file, "w", "utf-8")
	dummy_fd.close()
	
cmakelists_file = root + "/CMakeLists.txt"
cmakelists_fd = codecs.open(cmakelists_file, "w", "utf-8")
cmakelists_fd.write(r'cmake_minimum_required (VERSION 3.6)' + "\n\n")

cmakelists_fd.write(r'# CMake命令行使用 -DCMAKE_BUILD_TYPE生成相应配置' + "\n")
cmakelists_fd.write(r'# 可取枚举值：Debug | Release | RelWithDebInfo | MinSizeRel' + "\n\n")

cmakelists_fd.write(r'set(ProjectName ' + projectName + r')' + "\n")
cmakelists_fd.write(r'project(${ProjectName})' + "\n\n")

cmakelists_fd.write(r'# 用于包含子项目' + "\n")
cmakelists_fd.write(r'# add_subdirectory(subfolder)' + "\n\n")

cmakelists_fd.write(r'include_directories(include)' + "\n\n")
cmakelists_fd.write(r'aux_source_directory(src SRC_LIST)' + "\n")

pipe = os.popen("chdir")
base_dir = pipe.readline().strip().replace("\\", "/") + "/" + root
pipe.close()
print(base_dir)

pipe = os.popen("dir /B /S /AD " + root + "\\src")

count = 0
dirs = []
for sub_dir in pipe.readlines():
    subdir_name = sub_dir.strip()
    pipe2 = os.popen("dir /B /A-D " + subdir_name)
    for file in pipe2.readlines():
        file_name = file.strip()
        if re.search("\.((cpp)|(c)|(cxx))$", file_name, re.I):
            count = count + 1
            subdir_name = subdir_name.replace("\\", "/")
            src_dir2 = re.sub(base_dir + "/", "", subdir_name)
            dirs.append(src_dir2)
            break
			
for i in range(count):
    cmakelists_fd.write("aux_source_directory(%s SRC_LIST%d)\n" % (dirs[i], i))

strList = "${SRC_LIST}"
for i in range(count):
    strList += " $SRC_LIST{%d}" % i 
cmakelists_fd.write("\nset(SRC_LIST %s)\n\n" % strList)
pipe.close()

cmakelists_fd.write(r'file(GLOB_RECURSE INC_LIST "*.h")' + "\n\n")

cmakelists_fd.write(r'# 编译选项' + "\n")
cmakelists_fd.write(r'# set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11")' + "\n\n")

cmakelists_fd.write(r'add_definitions(-D_CRT_SECURE_NO_DEPRECATE)' + "\n\n")

if re.match(r'^static$', projectType, re.I) != None:
	cmakelists_fd.write(r'add_library(${ProjectName} STATIC ${SRC_LIST} ${INC_LIST})' + "\n\n")
	cmakelists_fd.write(r'set_target_properties(${ProjectName} PROPERTIES ARCHIVE_OUTPUT_DIRECTORY ../lib) # 指定静态库输出路径' + "\n\n")
elif re.match(r'^shared$', projectType, re.I) != None:
	cmakelists_fd.write(r'add_library(${ProjectName} SHARED ${SRC_LIST} ${INC_LIST})' + "\n\n")
	cmakelists_fd.write(r'set_target_properties(${ProjectName} PROPERTIES ARCHIVE_OUTPUT_DIRECTORY ../lib) # 指定静态库输出路径' + "\n")
	cmakelists_fd.write(r'set_target_properties(${ProjectName} PROPERTIES LIBRARY_OUTPUT_DIRECTORY ../lib) # 指定动态库输出路径' + "\n")
	cmakelists_fd.write(r'set_target_properties(${ProjectName} PROPERTIES RUNTIME_OUTPUT_DIRECTORY ../lib) # 指定dll输出路径' + "\n\n")
	
	dllexport_fd = codecs.open(root + "/include/dllexport.h", "w", "utf-8")
	EXPORTS = projectName + "_EXPORTS"
	EXPORT_API = projectName + "_API"
	dllexport_fd.write(r'#pragma once' + "\n\n")
	
	dllexport_fd.write(r'#ifdef ' + EXPORTS + "\n")
	dllexport_fd.write(r'#define ' + EXPORT_API + r' __declspec(dllexport)' + "\n")
	dllexport_fd.write(r'#else' + "\n")
	dllexport_fd.write(r'#define ' + EXPORT_API + r' __declspec(dllimport)' + "\n")
	dllexport_fd.write(r'#endif' + "\n\n")
	
	dllexport_fd.close()
else:
	cmakelists_fd.write(r'add_executable(${ProjectName} ${SRC_LIST} ${INC_LIST})' + "\n\n")
	cmakelists_fd.write(r'set_target_properties(${ProjectName} PROPERTIES RUNTIME_OUTPUT_DIRECTORY ../bin) # 指定可执行程序输出路径' + "\n\n")

cmakelists_fd.write(r'function(group_by_dir src_dir)' + "\n")
cmakelists_fd.write("\t" + r'foreach(FILE ${ARGN})' + "\n")
cmakelists_fd.write("\t\t" + r'# 获取文件绝对路径' + "\n")
cmakelists_fd.write("\t\t" + r'get_filename_component(FULL_NAME "${FILE}" ABSOLUTE)' + "\n")
cmakelists_fd.write("\t\t" + r'# 获取文件父路径' + "\n")
cmakelists_fd.write("\t\t" + r'get_filename_component(PARENT_DIR "${FULL_NAME}" PATH)' + "\n")
cmakelists_fd.write("\t\t" + r'# 移除父路径中的源码根路径' + "\n")
cmakelists_fd.write("\t\t" + r'string(REPLACE "${ARGV0}" "" GROUP "${PARENT_DIR}")' + "\n")
cmakelists_fd.write("\t\t" + r'# 确保路径使用windows路径符号' + "\n")
cmakelists_fd.write("\t\t" + r'string(REPLACE "/" "\\\\" GROUP "${GROUP}")' + "\n\n")

cmakelists_fd.write("\t\t" + r'# 将文件归组到 "Source Files" 和 "Header Files"' + "\n")
cmakelists_fd.write("\t\t" + r'if("${FULL_NAME}" MATCHES "/include/" OR "${FILE}" MATCHES "\\.h")' + "\n")
cmakelists_fd.write("\t\t\t" + r'set(GROUP "Header Files${GROUP}")' + "\n")
cmakelists_fd.write("\t\t" + r'else()' + "\n")
cmakelists_fd.write("\t\t\t" + r'set(GROUP "Source Files${GROUP}")' + "\n")
cmakelists_fd.write("\t\t" + r'endif()' + "\n")
cmakelists_fd.write("\t\t" + r'source_group("${GROUP}" FILES "${FILE}")' + "\n")
cmakelists_fd.write("\t" + r'endforeach()' + "\n")
cmakelists_fd.write(r'endfunction(group_by_dir)' + "\n\n")

cmakelists_fd.write(r'# 调用方法如下：' + "\n")
cmakelists_fd.write(r'# group_by_dir("${CMAKE_CURRENT_SOURCE_DIR}/include" ${INC_LIST})' + "\n")
cmakelists_fd.write(r'# group_by_dir("${CMAKE_CURRENT_SOURCE_DIR}/src" ${SRC_LIST})' + "\n")

cmakelists_fd.write(r'# 生成后事件处理' + "\n")
cmakelists_fd.write(r'# add_custom_command(TARGET ${ProjectName}' + "\n")
cmakelists_fd.write(r'#	POST_BUILD' + "\n")
cmakelists_fd.write(r'#	#COMMAND echo "$<TARGET_FILE_DIR:${ProjectName}> $<TARGET_FILE:${ProjectName}>"' + "\n")
cmakelists_fd.write(r'#	COMMAND ${CMAKE_COMMAND} -E make_directory ../bin' + "\n")
cmakelists_fd.write(r'#	COMMAND ${CMAKE_COMMAND} -E copy $<TARGET_FILE:${ProjectName}> ../bin/' + "\n")
cmakelists_fd.write(r'# )' + "\n\n")

cmakelists_fd.write(r'# 设置安装路径, 默认/usr' + "\n")
cmakelists_fd.write(r'# set(CPACK_PACKAGING_INSTALL_PREFIX /opt)' + "\n\n")

cmakelists_fd.write(r'# install(PROGRAMS bin/Test DESTINATION bin)' + "\n")
cmakelists_fd.write(r'# install(FILES include/dllexport.h DESTINATION include)' + "\n\n")

cmakelists_fd.write(r'# set(CPACK_PACKAGE_NAME "' + projectName + '")' + "\n")
cmakelists_fd.write(r'# set(CPACK_PACKAGE_DESCRIPTION_SUMMARY "Simple CPack ' + projectName + '")' + "\n")
cmakelists_fd.write(r'# set(CPACK_PACKAGE_VENDOR "' + projectName + '")' + "\n")
cmakelists_fd.write(r'# set(CPACK_PACKAGE_VERSION "1.0.0")' + "\n")
cmakelists_fd.write(r'# set(CPACK_PACKAGE_VERSION_MAJOR "1")' + "\n")
cmakelists_fd.write(r'# set(CPACK_PACKAGE_VERSION_MINOR "0")' + "\n")
cmakelists_fd.write(r'# set(CPACK_PACKAGE_VERSION_PATCH "0")' + "\n")
cmakelists_fd.write(r'# set(CPACK_RPM_PACKAGE_GROUP "' + projectName + '")' + "\n")
cmakelists_fd.write(r'# set(CPACK_RPM_PACKAGE_URL "http://gogoigogo.info")' + "\n")
cmakelists_fd.write(r'# set(CPACK_RPM_PACKAGE_DESCRIPTION "' + projectName + ' Dependencies")' + "\n")
cmakelists_fd.write(r'# set(CPACK_PACKAGE_RELEASE 1)' + "\n")
cmakelists_fd.write(r'# set(CPACK_RPM_PACKAGE_LICENSE "' + projectName + ' Licence")' + "\n\n")

cmakelists_fd.write(r'# 设置默认生成器，RPM生成器会构建RPM安装包，其它还有TGZ/ZIP等' + "\n")
cmakelists_fd.write(r'# set(CPACK_GENERATOR "RPM")' + "\n\n")

cmakelists_fd.write(r'# include(CPack)' + "\n\n")

cmakelists_fd.close()
	

	

	
