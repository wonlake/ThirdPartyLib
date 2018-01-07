cmake_minimum_required (VERSION 3.6)

# CMake命令行使用 -DCMAKE_BUILD_TYPE生成相应配置
# 可取枚举值：Debug | Release | RelWithDebInfo | MinSizeRel

set(ProjectName libglew)
project(${ProjectName})

# 用于包含子项目
# add_subdirectory(subfolder)

include_directories(include)
aux_source_directory(src SRC_LIST)

file(GLOB_RECURSE INC_LIST "*.h")

# 编译选项
# set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11")

add_definitions(-D_CRT_SECURE_NO_DEPRECATE)
add_definitions(-DGLEW_STATIC)

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

# set(CPACK_PACKAGE_NAME "libglew")
# set(CPACK_PACKAGE_DESCRIPTION_SUMMARY "Simple CPack libglew")
# set(CPACK_PACKAGE_VENDOR "libglew")
# set(CPACK_PACKAGE_VERSION "1.0.0")
# set(CPACK_PACKAGE_VERSION_MAJOR "1")
# set(CPACK_PACKAGE_VERSION_MINOR "0")
# set(CPACK_PACKAGE_VERSION_PATCH "0")
# set(CPACK_RPM_PACKAGE_GROUP "libglew")
# set(CPACK_RPM_PACKAGE_URL "http://gogoigogo.info")
# set(CPACK_RPM_PACKAGE_DESCRIPTION "libglew Dependencies")
# set(CPACK_PACKAGE_RELEASE 1)
# set(CPACK_RPM_PACKAGE_LICENSE "libglew Licence")

# 设置默认生成器，RPM生成器会构建RPM安装包，其它还有TGZ/ZIP等
# set(CPACK_GENERATOR "RPM")

# include(CPack)

