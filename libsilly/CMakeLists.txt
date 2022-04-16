cmake_minimum_required (VERSION 3.6)

# CMake命令行使用 -DCMAKE_BUILD_TYPE生成相应配置
# 可取枚举值：Debug | Release | RelWithDebInfo | MinSizeRel

set(ProjectName libsilly)
project(${ProjectName})

# 用于包含子项目
# add_subdirectory(subfolder)

include_directories(include)
include_directories(../libjpeg/include)
include_directories(../libpng/include)
include_directories(../libz/include)

aux_source_directory(src SRC_LIST)
aux_source_directory(src/loaders SRC_LIST1)

set(SRC_LIST ${SRC_LIST} ${SRC_LIST1})

file(GLOB_RECURSE INC_LIST "*.h")

# 编译选项
# set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11")

set(CMAKE_DEBUG_POSTFIX "_d")

add_compile_options( 
	$<$<CONFIG:>:/MT>
	$<$<CONFIG:Debug>:/MTd>
	$<$<CONFIG:Release>:/MD>
)

add_definitions(-D_WIN32)
add_definitions(-D__WIN32__)
add_definitions(-D_CRT_SECURE_NO_DEPRECATE)
add_definitions(-DSILLY_EXPORTS)
add_definitions(-DSILLY_HAVE_JPG)
add_definitions(-DSILLY_HAVE_PNG)

link_directories("${CMAKE_CURRENT_SOURCE_DIR}/../build/lib")

add_library(${ProjectName} SHARED ${SRC_LIST} ${INC_LIST})

set(LINK_LIB libz.lib libpng.lib libjpeg.lib)
target_link_libraries(${ProjectName} "${LINK_LIB}")

set_target_properties(${ProjectName} PROPERTIES ARCHIVE_OUTPUT_DIRECTORY ../lib) # 指定静态库输出路径
set_target_properties(${ProjectName} PROPERTIES LIBRARY_OUTPUT_DIRECTORY ../lib) # 指定动态库输出路径
set_target_properties(${ProjectName} PROPERTIES RUNTIME_OUTPUT_DIRECTORY ../lib) # 指定dll输出路径

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
		if("${FULL_NAME}" MATCHES "/include/")
			set(GROUP "Header Files${GROUP}")
		else()
			set(GROUP "Source Files${GROUP}")
		endif()
		source_group("${GROUP}" FILES "${FILE}")
	endforeach()
endfunction(group_by_dir)

# 调用方法如下：
group_by_dir("${CMAKE_CURRENT_SOURCE_DIR}/include" ${INC_LIST})
group_by_dir("${CMAKE_CURRENT_SOURCE_DIR}/src" ${SRC_LIST})

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

# set(CPACK_PACKAGE_NAME "libsilly")
# set(CPACK_PACKAGE_DESCRIPTION_SUMMARY "Simple CPack libsilly")
# set(CPACK_PACKAGE_VENDOR "libsilly")
# set(CPACK_PACKAGE_VERSION "1.0.0")
# set(CPACK_PACKAGE_VERSION_MAJOR "1")
# set(CPACK_PACKAGE_VERSION_MINOR "0")
# set(CPACK_PACKAGE_VERSION_PATCH "0")
# set(CPACK_RPM_PACKAGE_GROUP "libsilly")
# set(CPACK_RPM_PACKAGE_URL "http://gogoigogo.info")
# set(CPACK_RPM_PACKAGE_DESCRIPTION "libsilly Dependencies")
# set(CPACK_PACKAGE_RELEASE 1)
# set(CPACK_RPM_PACKAGE_LICENSE "libsilly Licence")

# 设置默认生成器，RPM生成器会构建RPM安装包，其它还有TGZ/ZIP等
# set(CPACK_GENERATOR "RPM")

# include(CPack)

