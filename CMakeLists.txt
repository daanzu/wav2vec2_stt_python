cmake_minimum_required(VERSION 3.15)

cmake_policy(SET CMP0091 NEW)
set(CMAKE_MSVC_RUNTIME_LIBRARY "MultiThreaded$<$<CONFIG:Debug>:Debug>")

project(wav2vec2_stt)

find_package(Torch REQUIRED)
message("wav2vec2_stt CMakeLists: ${TORCH_CXX_FLAGS}")
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} ${TORCH_CXX_FLAGS}")

add_subdirectory(native/simplectc)

add_library(wav2vec2_stt_lib SHARED
    native/wav2vec2_stt_lib.cpp
)
target_link_libraries(wav2vec2_stt_lib "${TORCH_LIBRARIES}" "${CTCDECODE_LIBRARY}")
set_property(TARGET wav2vec2_stt_lib PROPERTY CXX_STANDARD 14)

add_custom_command(
    TARGET wav2vec2_stt_lib POST_BUILD
    COMMAND ${CMAKE_COMMAND} -E copy
        $<TARGET_FILE:wav2vec2_stt_lib>
        ${PROJECT_SOURCE_DIR}/wav2vec2_stt/
    COMMENT "Installing wav2vec2_stt_lib shared library file to python project directory"
)

