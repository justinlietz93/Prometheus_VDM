cmake_minimum_required(VERSION 3.24)

# Plugins layer: declarative descriptors for physics/viz; no code here yet.
# Placeholder interface target to satisfy top-level add_subdirectory(plugins).
add_library(physics_nexus_plugins INTERFACE)

target_include_directories(physics_nexus_plugins INTERFACE
  ${CMAKE_CURRENT_SOURCE_DIR}
)

target_compile_features(physics_nexus_plugins INTERFACE cxx_std_20)