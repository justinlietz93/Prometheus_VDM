cmake_minimum_required(VERSION 3.23)
project(vdm_nexus LANGUAGES CXX)

# Build profile
set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_POSITION_INDEPENDENT_CODE ON)

# Qt automations
set(CMAKE_AUTOMOC ON)
set(CMAKE_AUTOUIC ON)
set(CMAKE_AUTORCC ON)

# Dependencies (CPU path; VTK-m/ROCm can be enabled later via VTK build)
find_package(Qt6 6.5 REQUIRED COMPONENTS Widgets)

# VTK components for a minimal viewport with Qt support
# Adjust components as needed (volume, streamlines, IOXML, etc.)
find_package(VTK 9.1 REQUIRED COMPONENTS
  CommonCore
  CommonColor
  CommonDataModel
  FiltersCore
  FiltersGeometry
  FiltersSources
  InteractionStyle
  InteractionWidgets
  RenderingCore
  RenderingOpenGL2
  RenderingAnnotation
  RenderingFreeType
  RenderingVolumeOpenGL2
  IOXML
  GUISupportQt
)

# Executable (sources will be added next)
add_executable(vdm_nexus
  src/main.cpp
  src/ViewportWindow.cpp
  src/ViewportWindow.h
)

target_include_directories(vdm_nexus PRIVATE src)

target_link_libraries(vdm_nexus PRIVATE
  Qt6::Widgets
  ${VTK_LIBRARIES}
)

# Required for VTK modules with CMake targets
vtk_module_autoinit(TARGETS vdm_nexus MODULES ${VTK_LIBRARIES})

# Notes:
# - This skeleton targets a cross-platform CPU build first.
# - For ROCm acceleration: build VTK with VTK-m enabled (Accelerators), then link VTK Accelerators modules.
# - QML integration can be added after initial QWidget-based QVTKOpenGLNativeWidget MVP compiles.