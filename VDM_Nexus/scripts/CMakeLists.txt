cmake_minimum_required(VERSION 3.24)

# Scripts layer: helper CLIs/utilities (read-only canon sync, approval wrappers, report packagers).
# Placeholder interface target to satisfy top-level add_subdirectory(scripts).
add_library(physics_nexus_scripts INTERFACE)

target_include_directories(physics_nexus_scripts INTERFACE
  ${CMAKE_CURRENT_SOURCE_DIR}
)

target_compile_features(physics_nexus_scripts INTERFACE cxx_std_20)