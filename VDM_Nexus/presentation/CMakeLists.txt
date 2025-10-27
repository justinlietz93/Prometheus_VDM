cmake_minimum_required(VERSION 3.24)

# Presentation layer: QML/Qt UI wiring lives here later.
# Placeholder interface library to satisfy top-level linking from physics_nexus_app.
add_library(physics_nexus_presentation INTERFACE)

target_include_directories(physics_nexus_presentation INTERFACE
  ${CMAKE_CURRENT_SOURCE_DIR}
)

target_compile_features(physics_nexus_presentation INTERFACE cxx_std_20)