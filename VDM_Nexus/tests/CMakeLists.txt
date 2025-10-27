cmake_minimum_required(VERSION 3.24)

# Generate a tiny compile-only test that includes the application ports
file(WRITE ${CMAKE_CURRENT_BINARY_DIR}/test_ports_compile.cpp "
#include "${CMAKE_CURRENT_SOURCE_DIR}/../application/ports/ports.hpp"
int main() {
  using namespace vdm_nexus::app;
  IRunnerService* runner = nullptr;
  IArtifactStore* store = nullptr;
  IMarkdownReader* reader = nullptr;
  ISchemaCatalog* catalog = nullptr;
  IApprovalRepo* approvals = nullptr;
  (void)runner; (void)store; (void)reader; (void)catalog; (void)approvals;
  return 0;
}
")

add_executable(ports_compile_test ${CMAKE_CURRENT_BINARY_DIR}/test_ports_compile.cpp)
target_link_libraries(ports_compile_test PRIVATE physics_nexus_application)
target_compile_features(ports_compile_test PRIVATE cxx_std_20)