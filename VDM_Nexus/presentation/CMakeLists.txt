cmake_minimum_required(VERSION 3.24)

# Presentation layer: QML/Qt UI wiring lives here later.
# Provide a concrete target for controllers (QtCore-only for now).
add_library(physics_nexus_presentation STATIC
  DashboardController.cpp
)

target_include_directories(physics_nexus_presentation
  PUBLIC
    ${CMAKE_CURRENT_SOURCE_DIR}
)

target_link_libraries(physics_nexus_presentation
  PUBLIC
    Qt6::Core
)

target_compile_features(physics_nexus_presentation PUBLIC cxx_std_20)
