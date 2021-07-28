cmake_minimum_required(VERSION 3.5)

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

add_custom_target(install_wav2vec2_stt_lib ALL
    COMMENT "Installing wav2vec2_stt_lib shared library file to python project directory"
    COMMAND cp ${PROJECT_BINARY_DIR}/libwav2vec2_stt_lib${CMAKE_SHARED_LIBRARY_SUFFIX} ${PROJECT_SOURCE_DIR}/wav2vec2_stt/
)
add_dependencies(install_wav2vec2_stt_lib wav2vec2_stt_lib)
