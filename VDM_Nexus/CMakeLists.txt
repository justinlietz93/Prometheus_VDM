cmake_minimum_required(VERSION 3.24)

project(physics_nexus
  VERSION 0.1.0
  DESCRIPTION "VDM Nexus desktop application"
  LANGUAGES CXX
)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

set(CMAKE_AUTOMOC ON)
set(CMAKE_AUTORCC ON)
set(CMAKE_AUTOUIC ON)

find_package(Qt6 6.5 REQUIRED COMPONENTS Core Gui Qml Quick Widgets)

add_subdirectory(domain)
add_subdirectory(application)
add_subdirectory(infrastructure)
add_subdirectory(presentation)
add_subdirectory(resources)
add_subdirectory(plugins)
add_subdirectory(scripts)
add_subdirectory(tests)

# Build tests by default (compile-only sanity target)
option(NEXUS_BUILD_TESTS "Build Nexus compile-only tests" ON)
if(NEXUS_BUILD_TESTS)
  # Ensure the compile-only test target is built with 'all'
  add_custom_target(nexus_build_tests ALL DEPENDS nexus_ports_compile)
endif()

add_executable(physics_nexus_app)
target_sources(physics_nexus_app
  PRIVATE
    src/main.cpp
)
target_link_libraries(physics_nexus_app
  PRIVATE
    Qt6::Core
    Qt6::Gui
    Qt6::Qml
    Qt6::Quick
    Qt6::Widgets
    physics_nexus_application
    physics_nexus_presentation
)

install(TARGETS physics_nexus_app
  RUNTIME DESTINATION bin
)

include(GNUInstallDirs)
install(DIRECTORY resources/
  DESTINATION ${CMAKE_INSTALL_DATAROOT_DIR}/physics_nexus/resources
  FILES_MATCHING PATTERN "*"
)