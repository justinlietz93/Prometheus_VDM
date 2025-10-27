cmake_minimum_required(VERSION 3.24)

add_library(physics_nexus_application INTERFACE)

target_include_directories(physics_nexus_application INTERFACE
  ${CMAKE_CURRENT_SOURCE_DIR}
  ${CMAKE_CURRENT_SOURCE_DIR}/ports
)

target_compile_features(physics_nexus_application INTERFACE cxx_std_20)