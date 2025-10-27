cmake_minimum_required(VERSION 3.24)

# Resources layer: qrc/assets and static files (read-only).
# Placeholder interface target to satisfy top-level add_subdirectory(resources).
add_library(physics_nexus_resources INTERFACE)

target_include_directories(physics_nexus_resources INTERFACE
  ${CMAKE_CURRENT_SOURCE_DIR}
)

target_compile_features(physics_nexus_resources INTERFACE cxx_std_20)