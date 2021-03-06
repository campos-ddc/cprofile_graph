#!/usr/bin/env python
# -*- coding: utf-8 -*-
from cprofile_graph import (profile_code, profile_ctx, profile_decorator,
                            profile_file)


def test_profile_ctx(tmpdir):
    graph_file = tmpdir.join('profile_ctx.png')

    assert not graph_file.isfile()
    with profile_ctx(graph_filename=graph_file.strpath, view=False):
        for i in range(1000):
            1 + 1
    assert graph_file.isfile()


def test_profile_code(tmpdir):
    graph_file = tmpdir.join('profile_ctx.png')

    assert not graph_file.isfile()
    profile_code(
        code='for i in range(1000): 1 + 1',
        graph_filename=graph_file.strpath,
        view=False)
    assert graph_file.isfile()


def test_profile_decorator_args(tmpdir):
    graph_file = tmpdir.join('profile_ctx.png')
    assert not graph_file.isfile()

    @profile_decorator(graph_file.strpath, view=False)
    def foo():
        for i in range(1000):
            1 + 1

    assert not graph_file.isfile()
    foo()
    assert graph_file.isfile()


def test_profile_decorator_no_args(tmpdir, mocker):
    graph_file = tmpdir.join('profile_ctx.png')

    # Mock inner function to make default parameters what we need for test
    from cprofile_graph import _profile_decorator
    original = _profile_decorator

    def mock_profile_decorator(*args, **kwargs):
        kwargs['graph_filename'] = graph_file.strpath
        kwargs['view'] = False
        return original(*args, **kwargs)

    mocker.patch(
        'cprofile_graph._profile_decorator',
        mock_profile_decorator, )

    assert not graph_file.isfile()

    @profile_decorator
    def foo():
        for i in range(1000):
            1 + 1

    assert not graph_file.isfile()
    foo()
    assert graph_file.isfile()


def test_profile_file(tmpdir):
    script_file = tmpdir.join('script.py')
    script_file.write('for i in range(1000): 1 + 1')

    graph_file = tmpdir.join('profile_ctx.png')

    assert not graph_file.isfile()
    profile_file(
        filename=script_file.strpath,
        graph_filename=graph_file.strpath,
        view=False)
    assert graph_file.isfile()
