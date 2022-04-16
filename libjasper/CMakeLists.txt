cmake_minimum_required (VERSION 3.6)

# CMake命令行使用 -DCMAKE_BUILD_TYPE生成相应配置
# 可取枚举值：Debug | Release | RelWithDebInfo | MinSizeRel

set(ProjectName libjasper)
project(${ProjectName})

# 用于包含子项目
# add_subdirectory(subfolder)

include_directories(include)
aux_source_directory(src SRC_LIST)
aux_source_directory(src/base SRC_LIST1)
aux_source_directory(src/bmp SRC_LIST2)
aux_source_directory(src/jp2 SRC_LIST3)
aux_source_directory(src/jpc SRC_LIST4)
aux_source_directory(src/jpg SRC_LIST5)
aux_source_directory(src/mif SRC_LIST6)
aux_source_directory(src/pgx SRC_LIST7)
aux_source_directory(src/pnm SRC_LIST8)
aux_source_directory(src/ras SRC_LIST9)

set(SRC_LIST ${SRC_LIST1} ${SRC_LIST2} ${SRC_LIST3} ${SRC_LIST4} ${SRC_LIST5} ${SRC_LIST6} ${SRC_LIST7} ${SRC_LIST8} ${SRC_LIST9})

file(GLOB_RECURSE INC_LIST "*.h")

# 编译选项
# set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11")

add_compile_options( 
	$<$<CONFIG:>:/MT>
	$<$<CONFIG:Debug>:/MTd>
	$<$<CONFIG:Release>:/MD>
)

add_definitions(-D_CRT_SECURE_NO_DEPRECATE)
add_definitions(-DJAS_WIN_MSVC_BUILD)

list(FILTER SRC_LIST EXCLUDE REGEX "jpg_dec.c")
list(FILTER SRC_LIST EXCLUDE REGEX "jpg_enc.c")
list(FILTER SRC_LIST EXCLUDE REGEX "ras_cod.c")

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
		if("${FILE}" MATCHES ".*\\\\.h")
			set(GROUP "Header Files${GROUP}")
		else()
			set(GROUP "Source Files${GROUP}")
		endif()
		source_group("${GROUP}" FILES "${FILE}")
	endforeach()
endfunction(group_by_dir)

# 调用方法如下：
# group_by_dir("${CMAKE_CURRENT_SOURCE_DIR}" ${INC_LIST})
# group_by_dir("${CMAKE_CURRENT_SOURCE_DIR}" ${SRC_LIST})
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

# set(CPACK_PACKAGE_NAME "libjasper")
# set(CPACK_PACKAGE_DESCRIPTION_SUMMARY "Simple CPack libjasper")
# set(CPACK_PACKAGE_VENDOR "libjasper")
# set(CPACK_PACKAGE_VERSION "1.0.0")
# set(CPACK_PACKAGE_VERSION_MAJOR "1")
# set(CPACK_PACKAGE_VERSION_MINOR "0")
# set(CPACK_PACKAGE_VERSION_PATCH "0")
# set(CPACK_RPM_PACKAGE_GROUP "libjasper")
# set(CPACK_RPM_PACKAGE_URL "http://gogoigogo.info")
# set(CPACK_RPM_PACKAGE_DESCRIPTION "libjasper Dependencies")
# set(CPACK_PACKAGE_RELEASE 1)
# set(CPACK_RPM_PACKAGE_LICENSE "libjasper Licence")

# 设置默认生成器，RPM生成器会构建RPM安装包，其它还有TGZ/ZIP等
# set(CPACK_GENERATOR "RPM")

# include(CPack)

