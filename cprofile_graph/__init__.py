# -*- coding: utf-8 -*-
from __future__ import absolute_import

import cProfile
import contextlib
import functools
import os
import subprocess
import sys
import tempfile

import gprof2dot
import pygraphviz

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

DEFAULT_GRAPH_FILENAME = 'cprofile_graph.png'
DEFAULT_NODE_THRESHOLD = 0.005  # 0.5%
DEFAULT_EDGE_THRESHOLD = 0.001  # 0.1%
DEFAULT_VIEW = True
DEFAULT_COLOUR_NODES_BY_SELFTIME = False


@contextlib.contextmanager
def profile_ctx(graph_filename=DEFAULT_GRAPH_FILENAME,
                node_threshold=DEFAULT_NODE_THRESHOLD,
                edge_threshold=DEFAULT_EDGE_THRESHOLD,
                view=DEFAULT_VIEW):
    '''
    Profile code within a context. Usage:
        with profile_ctx():
            foo()

    :param graph_filename: Graph image output filename.
    :type graph_filename: str

    :param node_threshold: Prune graph nodes below this threshold.
    :type node_threshold: float

    :param edge_threshold: Prune graph edges below this threshold.
    :type edge_threshold: float

    :param view: Automatically open output file after profiling.
    :type view: bool
    '''

    # Wrap profiling around context manager
    profile = cProfile.Profile()
    profile.enable()
    yield graph_filename
    profile.disable()

    # cProfile demands a real file to dump into, StringIO won't do
    with tempfile.NamedTemporaryFile() as pstats_file:
        profile.dump_stats(pstats_file.name)
        parser = gprof2dot.PstatsParser(pstats_file.name)

    _profile_from_parser(
        parser=parser,
        graph_filename=graph_filename,
        node_threshold=node_threshold,
        edge_threshold=edge_threshold,
        view=view, )


def profile_decorator(*args, **kwargs):
    '''
    Profile function using a decorator. Usage:

        @profile_decorator
        def foo():
            1 + 1

        @profile_decorator("myprofile.png")
        def foo():
            1 + 1

    All parameters are optional.

    :param graph_filename: Graph image output filename.
    :type graph_filename: str

    :param node_threshold: Prune graph nodes below this threshold.
    :type node_threshold: float

    :param edge_threshold: Prune graph edges below this threshold.
    :type edge_threshold: float

    :param view: Automatically open output file after profiling.
    :type view: bool
    '''
    if len(args) == 1 and callable(args[0]):
        return _profile_decorator()(args[0])
    else:
        return _profile_decorator(*args, **kwargs)


def _profile_decorator(graph_filename=DEFAULT_GRAPH_FILENAME,
                       node_threshold=DEFAULT_NODE_THRESHOLD,
                       edge_threshold=DEFAULT_EDGE_THRESHOLD,
                       view=DEFAULT_VIEW):
    '''
    Inner implementation of profile_decorator, this one must always be called
    as a function.

    .. seealso:: profile_decorator for args
    '''

    def _decorator(f):
        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            profile = cProfile.Profile()
            profile.enable()
            r = f(*args, **kwargs)
            profile.disable()
            # cProfile demands a real file to dump into, StringIO won't do
            with tempfile.NamedTemporaryFile() as pstats_file:
                profile.dump_stats(pstats_file.name)
                parser = gprof2dot.PstatsParser(pstats_file.name)

            _profile_from_parser(
                parser=parser,
                graph_filename=graph_filename,
                node_threshold=node_threshold,
                edge_threshold=edge_threshold,
                view=view, )
            return r

        return wrapper

    return _decorator


def profile_file(filename,
                 graph_filename=DEFAULT_GRAPH_FILENAME,
                 node_threshold=DEFAULT_NODE_THRESHOLD,
                 edge_threshold=DEFAULT_EDGE_THRESHOLD,
                 view=DEFAULT_VIEW,
                 colour_nodes_by_selftime=DEFAULT_COLOUR_NODES_BY_SELFTIME):
    '''
    Profile Python file execution. Usage:
        profile_file("my_script.py"):

    :param filename: Python script to be profiled.
    :type filename: str

    :param graph_filename: Graph image output filename.
    :type graph_filename: str

    :param node_threshold: Prune graph nodes below this threshold.
    :type node_threshold: float

    :param edge_threshold: Prune graph edges below this threshold.
    :type edge_threshold: float

    :param view: Automatically open output file after profiling.
    :type view: bool

    :param colour_nodes_by_selftime: Colour nodes by self time,
        rather than by total time (sum of self and descendants)
    :type colour_nodes_by_selftime: bool
    '''
    sys.path.insert(0, os.path.dirname(filename))
    with open(filename, 'rb') as fp:
        code = compile(fp.read(), filename, 'exec')
    profile_code(
        code=code,
        filename=filename,
        graph_filename=graph_filename,
        node_threshold=node_threshold,
        edge_threshold=edge_threshold,
        view=view,
        colour_nodes_by_selftime=colour_nodes_by_selftime, )


def profile_code(code,
                 filename=None,
                 graph_filename=DEFAULT_GRAPH_FILENAME,
                 node_threshold=DEFAULT_NODE_THRESHOLD,
                 edge_threshold=DEFAULT_EDGE_THRESHOLD,
                 view=DEFAULT_VIEW,
                 colour_nodes_by_selftime=DEFAULT_COLOUR_NODES_BY_SELFTIME):
    '''
    Profile code string. Usage:
        profile_code("import foo;foo.slow_function()"):

    :param code: Code (string) to be profiled.
    :type code: str

    :param filename: Optional filename set as __file__ when code is executed.
    :type filename: str

    :param graph_filename: Graph image output filename.
    :type graph_filename: str

    :param node_threshold: Prune graph nodes below this threshold.
    :type node_threshold: float

    :param edge_threshold: Prune graph edges below this threshold.
    :type edge_threshold: float

    :param view: Automatically open output file after profiling.
    :type view: bool

    :param colour_nodes_by_selftime: Colour nodes by self time,
        rather than by total time (sum of self and descendants)
    :type colour_nodes_by_selftime: bool
    '''
    globs = {
        '__name__': '__main__',
        '__package__': None,
    }
    if filename:
        globs['__file__'] = filename

    # cProfile demands a real file to dump into, StringIO won't do
    with tempfile.NamedTemporaryFile() as pstats_file:
        cProfile.runctx(
            code, globals=globs, locals=None, filename=pstats_file.name)
        parser = gprof2dot.PstatsParser(pstats_file.name)

    _profile_from_parser(
        parser=parser,
        graph_filename=graph_filename,
        node_threshold=node_threshold,
        edge_threshold=edge_threshold,
        view=view,
        colour_nodes_by_selftime=colour_nodes_by_selftime, )


def _profile_from_parser(
        parser,
        graph_filename=DEFAULT_GRAPH_FILENAME,
        node_threshold=DEFAULT_NODE_THRESHOLD,
        edge_threshold=DEFAULT_EDGE_THRESHOLD,
        view=DEFAULT_VIEW,
        colour_nodes_by_selftime=DEFAULT_COLOUR_NODES_BY_SELFTIME):

    # Parse pstats and prune graph based on thresholds
    profile = parser.parse()

    try:
        profile.prune(
            node_threshold,
            edge_threshold,
            paths=None,
            colour_nodes_by_selftime=colour_nodes_by_selftime)
    except TypeError:
        profile.prune(
            node_threshold,
            edge_threshold,
            colour_nodes_by_selftime=colour_nodes_by_selftime)

    # Convert graph to dot format
    dot_file = StringIO()
    dot = gprof2dot.DotWriter(dot_file)
    dot.graph(profile, theme=gprof2dot.themes['color'])

    # Convert dot to image
    graph = pygraphviz.AGraph(string=dot_file.getvalue())
    graph.draw(graph_filename, prog='dot')

    # Open image
    if view:
        _view_file(graph_filename)


def _view_file(path):
    '''
    Open a file using the default application.

    :param path: Path to be opened.
    :type path: str
    '''
    try:
        if sys.platform.startswith('darwin'):
            r = subprocess.call(('open', path))
            if r: raise RuntimeError('Subprocess failed to open')
        elif os.name == 'nt':
            os.startfile(path)
        elif os.name == 'posix':
            r = subprocess.call(('xdg-open', path))
            if r: raise RuntimeError('Subprocess failed to open')
    except:
        # If all fails, try to use webbrowser
        import webbrowser
        webbrowser.open(path)


#=============================================================================
# METADATA
#=============================================================================
__all__ = [
    'profile_code',
    'profile_ctx',
    'profile_decorator',
    'profile_file',
]

__author__ = 'Diogo de Campos'
__email__ = 'campos.ddc@gmail.com'
__version__ = '2.0.3'
