
file(GLOB_RECURSE SOURCES "*.cpp" "*.hpp")

add_library (wikiparser SHARED ${SOURCES})

target_include_directories(wikiparser PRIVATE ${SC_MEMORY_SRC})
target_link_libraries(wikiparser sc-memory)

add_dependencies(wikiparser sc-memory)

sc_codegen(wikiparser ${CMAKE_CURRENT_LIST_DIR})
