cmake_minimum_required(VERSION 3.24)
project(nexus_compile_tests)

# Standalone mode: include interface targets if not brought by a parent project
if(NOT TARGET physics_nexus_application)
  add_subdirectory(${CMAKE_CURRENT_SOURCE_DIR}/../application application)
endif()
if(NOT TARGET physics_nexus_domain)
  add_subdirectory(${CMAKE_CURRENT_SOURCE_DIR}/../domain domain)
endif()

# Generate a tiny compile-only test that includes the application ports
file(WRITE ${CMAKE_CURRENT_BINARY_DIR}/test_ports_compile.cpp "
#include \"${CMAKE_CURRENT_SOURCE_DIR}/../application/ports/ports.hpp\"
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

# Generate a domain compile-only test that includes the domain models (KG-Lite)
file(WRITE ${CMAKE_CURRENT_BINARY_DIR}/test_domain_compile.cpp "
#include \"${CMAKE_CURRENT_SOURCE_DIR}/../domain/models.hpp\"
#include <string>
#include <vector>
int main() {
  using namespace vdm_nexus::domain;
  Relation r = Relation::References;
  Node n{.id=\"n1\", .label=\"Label\", .kind=\"axis\"};
  Edge e{.source=\"n1\", .target=\"n2\", .relation=r, .weight{}};
  ChunkType ct = ChunkType::Signals;
  ChunkCounts cc{};
  IndexPayload ip{};
  ip.schema_version = \"2025-09-25\";
  ChunkRef cr{};
  cr.chunk_id = \"justin@1.0:signals\";
  cr.sha256 = \"0000000000000000000000000000000000000000000000000000000000000000\";
  cr.kind = ct;
  ip.chunks.push_back(cr);
  ip.counts = cc;
  ChunkEnvelope env{};
  env.set_id = \"justin\";
  env.set_version = \"1.0\";
  env.chunk_type = ct;
  env.chunk_id = \"justin@1.0:signals\";
  env.updated = \"2025-10-27T00:00:00Z\";
  env.source = \"memory-bank/MEMORY_GRAPH_CONTEXT/justin-graph.json\";
  env.content_sha256 = cr.sha256;
  env.part = 1; env.total_parts = 1;
  env.payload_canonical_json = \"{}\";
  return (n.id==\"n1\" && e.source==\"n1\" && env.part==1) ? 0 : 1;
}
")

add_executable(domain_compile_test ${CMAKE_CURRENT_BINARY_DIR}/test_domain_compile.cpp)
target_link_libraries(domain_compile_test PRIVATE physics_nexus_domain)
target_compile_features(domain_compile_test PRIVATE cxx_std_20)
