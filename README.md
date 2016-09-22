[![Travis Build Status](https://img.shields.io/travis/campos-ddc/cprofile_graph.svg)](https://travis-ci.org/campos-ddc/cprofile_graph)
[![PyPI version](https://img.shields.io/pypi/v/cprofile_graph.svg)](https://pypi.python.org/pypi/cprofile_graph)

# About _cprofile_graph_

cprofile_graph is used to generate visual graphs for Python profiling.

## Usage

* As a context manager:

```python
from cprofile_graph import profile_ctx
with profile_ctx("myprofile.png"):
    foo()
```

* As a function:

```python
from cprofile_graph import profile_code
profile_code("foo()", "myprofile.png")
```

* As a script:

```bash
cprofile_graph myscript.py -o myprofile.png
cprofile_graph -c "foo()" -o myprofile.png
```

# Example

This is the kind of output you will get from cprofile_graph, hot colors indicate most used functions:

![Sample](sample.png)

# Requirements

  * [gprof2dot](https://github.com/jrfonseca/gprof2dot): Convert cProfile stats into dot files
  * [Graphviz](http://www.graphviz.org/Download.php): Convert dot files into visual graphs
  * [pygraphviz](http://pygraphviz.github.io/): Call Graphviz from within Python
