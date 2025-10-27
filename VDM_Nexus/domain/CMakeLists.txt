cmake_minimum_required(VERSION 3.24)

# Domain layer: plain data models (no Qt/DB/Python). Placeholder library to satisfy top-level wiring.
add_library(physics_nexus_domain INTERFACE)

target_include_directories(physics_nexus_domain INTERFACE
  ${CMAKE_CURRENT_SOURCE_DIR}
)

target_compile_features(physics_nexus_domain INTERFACE cxx_std_20)