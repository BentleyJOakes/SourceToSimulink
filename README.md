
SourceToSimulink
===========

Python scripts to take C or C++ source code, extract an XML representation, and then transform that XML into a Simulink model representing the original source code.

parse_source.py
---------------

Usage: python2 parse_source.py filename.c(pp)

Walks through the AST produced by clang using the Python bindings of libclang.

Uses to_xml.py, which will break down the elements in the AST tree into XML nodes. Note that the tokenizing of clang is not perfect, and must be handled relatively manually.

build_model.py
--------------

Usage: python2 build_model.py filename.xml

Uses the XML representation of source code in order to create a Himesis graph, which will be transformed into a Simulink model.
