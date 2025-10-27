cmake_minimum_required(VERSION 3.24)

# VDM Nexus — compile-only sanity test for application ports
# Scope: strictly Nexus. No memory graph, no MCP, no tokens.

# Generate a tiny source that includes the Clean Architecture ports header
file(WRITE ${CMAKE_CURRENT_BINARY_DIR}/test_ports_compile.cpp "
#include \"${CMAKE_CURRENT_LIST_DIR}/../application/ports/ports.hpp\"
int main() {
  using namespace vdm_nexus::app;
  IRunnerService* runner = nullptr;
  IArtifactStore* store = nullptr;
  IMarkdownReader* reader = nullptr;
  ISchemaCatalog* schema = nullptr;
  (void)runner; (void)store; (void)reader; (void)schema;
  return 0;
}
")

add_executable(nexus_ports_compile ${CMAKE_CURRENT_BINARY_DIR}/test_ports_compile.cpp)

# Header-only compile; expose the application/ports includes
target_include_directories(nexus_ports_compile PRIVATE
  ${CMAKE_CURRENT_LIST_DIR}/../application
  ${CMAKE_CURRENT_LIST_DIR}/../application/ports
)

# No linking required; this test just verifies Nexus ports compile in isolation.
