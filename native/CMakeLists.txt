cmake_minimum_required(VERSION 3.5)

project(wav2vec2_stt_lib)

find_package(Torch REQUIRED)
message("wav2vec2_stt_lib CMakeLists: ${TORCH_CXX_FLAGS}")
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} ${TORCH_CXX_FLAGS}")

add_subdirectory(simplectc)

add_library(wav2vec2_stt_lib SHARED
    wav2vec2_stt_lib.cpp
)
target_link_libraries(wav2vec2_stt_lib "${TORCH_LIBRARIES}" "${CTCDECODE_LIBRARY}")
set_property(TARGET wav2vec2_stt_lib PROPERTY CXX_STANDARD 14)
