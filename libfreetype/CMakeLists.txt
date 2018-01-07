cmake_minimum_required (VERSION 3.6)

# CMake命令行使用 -DCMAKE_BUILD_TYPE生成相应配置
# 可取枚举值：Debug | Release | RelWithDebInfo | MinSizeRel

set(ProjectName libfreetype)
project(${ProjectName})

# 用于包含子项目
# add_subdirectory(subfolder)

include_directories(include)
aux_source_directory(src SRC_LIST)
set(SRC_LIST1 src/autofit/autofit.c)

aux_source_directory(src/base SRC_LIST2)
list(FILTER SRC_LIST2 EXCLUDE REGEX "basepic.c")
list(FILTER SRC_LIST2 EXCLUDE REGEX "ftadvanc.c")
list(FILTER SRC_LIST2 EXCLUDE REGEX "ftapi.c")
list(FILTER SRC_LIST2 EXCLUDE REGEX "ftbdf.c")
list(FILTER SRC_LIST2 EXCLUDE REGEX "ftcalc.c")
list(FILTER SRC_LIST2 EXCLUDE REGEX "ftcid.c")
list(FILTER SRC_LIST2 EXCLUDE REGEX "ftdbgmem.c")
list(FILTER SRC_LIST2 EXCLUDE REGEX "ftgloadr.c")
list(FILTER SRC_LIST2 EXCLUDE REGEX "ftgxval.c")
list(FILTER SRC_LIST2 EXCLUDE REGEX "ftlcdfil.c")
list(FILTER SRC_LIST2 EXCLUDE REGEX "ftmac.c")
list(FILTER SRC_LIST2 EXCLUDE REGEX "ftobjs.c")
list(FILTER SRC_LIST2 EXCLUDE REGEX "ftotval.c")
list(FILTER SRC_LIST2 EXCLUDE REGEX "ftoutln.c")
list(FILTER SRC_LIST2 EXCLUDE REGEX "ftpatent.c")
list(FILTER SRC_LIST2 EXCLUDE REGEX "ftparent.c")
list(FILTER SRC_LIST2 EXCLUDE REGEX "ftpic.c")
list(FILTER SRC_LIST2 EXCLUDE REGEX "ftrfork.c")
list(FILTER SRC_LIST2 EXCLUDE REGEX "ftsnames.c")
list(FILTER SRC_LIST2 EXCLUDE REGEX "ftstream.c")
list(FILTER SRC_LIST2 EXCLUDE REGEX "fttrigon.c")
list(FILTER SRC_LIST2 EXCLUDE REGEX "ftutil.c")
list(FILTER SRC_LIST2 EXCLUDE REGEX "ftxf86.c")

set(SRC_LIST3 src/bdf/bdf.c)
set(SRC_LIST4 src/cache/ftcache.c)

set(SRC_LIST5 src/cff/cff.c)
set(SRC_LIST6 src/cid/type1cid.c)
set(SRC_LIST9 src/gzip/ftgzip.c)
set(SRC_LIST10 src/lzw/ftlzw.c)

set(SRC_LIST12 src/pcf/pcf.c)
set(SRC_LIST13 src/pfr/pfr.c)
set(SRC_LIST14 src/psaux/psaux.c)
set(SRC_LIST15 src/pshinter/pshinter.c)
set(SRC_LIST16 src/psnames/psmodule.c)
set(SRC_LIST17 src/raster/raster.c)
set(SRC_LIST18 src/sfnt/sfnt.c)
set(SRC_LIST19 src/smooth/smooth.c)
set(SRC_LIST21 src/truetype/truetype.c)
set(SRC_LIST22 src/type1/type1.c)
set(SRC_LIST23 src/type42/type42.c)
set(SRC_LIST24 src/winfonts/winfnt.c)

set(SRC_LIST ${SRC_LIST1} ${SRC_LIST2} ${SRC_LIST3} ${SRC_LIST4} ${SRC_LIST5} ${SRC_LIST6}
	${SRC_LIST9} ${SRC_LIST10} ${SRC_LIST12} ${SRC_LIST13} ${SRC_LIST14} ${SRC_LIST15} ${SRC_LIST16}
	${SRC_LIST17} ${SRC_LIST18} ${SRC_LIST19} ${SRC_LIST21} ${SRC_LIST22} ${SRC_LIST23} ${SRC_LIST24})

file(GLOB_RECURSE INC_LIST "*.h")

# 编译选项
# set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11")

add_definitions(-D_CRT_SECURE_NO_DEPRECATE)
add_definitions(-DFT_DEBUG_LEVEL_ERROR)
add_definitions(-DFT_DEBUG_LEVEL_TRACE)
add_definitions(-DFT2_BUILD_LIBRARY)

add_library(${ProjectName} STATIC ${SRC_LIST} ${INC_LIST})

set_target_properties(${ProjectName} PROPERTIES ARCHIVE_OUTPUT_DIRECTORY ../lib) # 指定静态库输出路径

function(group_by_dir src_dir)
	foreach(FILE ${ARGN})
		# 获取文件绝对路径
		get_filename_component(FULL_NAME "${FILE}" ABSOLUTE)
		# 获取文件父路径
		get_filename_component(PARENT_DIR "${FULL_NAME}" PATH)
		# 移除父路径中的源码根路径
		string(REPLACE "${ARGV0}" "" GROUP "${PARENT_DIR}")
		# 确保路径使用windows路径符号
		string(REPLACE "/" "\\\\" GROUP "${GROUP}")

		# 将文件归组到 "Source Files" 和 "Header Files"
		if("${FULL_NAME}" MATCHES "/include/" OR "${FILE}" MATCHES "\\.h")
			set(GROUP "Header Files${GROUP}")
		else()
			set(GROUP "Source Files${GROUP}")
		endif()
		source_group("${GROUP}" FILES "${FILE}")
	endforeach()
endfunction(group_by_dir)

# 调用方法如下：
# group_by_dir("${CMAKE_CURRENT_SOURCE_DIR}/include" ${INC_LIST})
# group_by_dir("${CMAKE_CURRENT_SOURCE_DIR}/src" ${SRC_LIST})
# 生成后事件处理
# add_custom_command(TARGET ${ProjectName}
#	POST_BUILD
#	#COMMAND echo "$<TARGET_FILE_DIR:${ProjectName}> $<TARGET_FILE:${ProjectName}>"
#	COMMAND ${CMAKE_COMMAND} -E make_directory ../bin
#	COMMAND ${CMAKE_COMMAND} -E copy $<TARGET_FILE:${ProjectName}> ../bin/
# )

# 设置安装路径, 默认/usr
# set(CPACK_PACKAGING_INSTALL_PREFIX /opt)

# install(PROGRAMS bin/Test DESTINATION bin)
# install(FILES include/dllexport.h DESTINATION include)

# set(CPACK_PACKAGE_NAME "libfreetype")
# set(CPACK_PACKAGE_DESCRIPTION_SUMMARY "Simple CPack libfreetype")
# set(CPACK_PACKAGE_VENDOR "libfreetype")
# set(CPACK_PACKAGE_VERSION "1.0.0")
# set(CPACK_PACKAGE_VERSION_MAJOR "1")
# set(CPACK_PACKAGE_VERSION_MINOR "0")
# set(CPACK_PACKAGE_VERSION_PATCH "0")
# set(CPACK_RPM_PACKAGE_GROUP "libfreetype")
# set(CPACK_RPM_PACKAGE_URL "http://gogoigogo.info")
# set(CPACK_RPM_PACKAGE_DESCRIPTION "libfreetype Dependencies")
# set(CPACK_PACKAGE_RELEASE 1)
# set(CPACK_RPM_PACKAGE_LICENSE "libfreetype Licence")

# 设置默认生成器，RPM生成器会构建RPM安装包，其它还有TGZ/ZIP等
# set(CPACK_GENERATOR "RPM")

# include(CPack)

