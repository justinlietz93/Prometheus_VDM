cmake_minimum_required(VERSION 3.24)

# Infrastructure layer: adapters will be added here (SQLite approvals, filesystem, runners, schema catalog).
# Placeholder interface library to satisfy top-level add_subdirectory while ports/adapters are implemented.
add_library(physics_nexus_infrastructure INTERFACE)

target_include_directories(physics_nexus_infrastructure INTERFACE
  ${CMAKE_CURRENT_SOURCE_DIR}
)

target_compile_features(physics_nexus_infrastructure INTERFACE cxx_std_20)