# -*- coding: utf-8 -*-

import click

from cprofile_graph import DEFAULT_NODE_THRESHOLD, DEFAULT_EDGE_THRESHOLD, \
    DEFAULT_GRAPH_FILENAME, DEFAULT_VIEW, profile_file, profile_code


@click.command()
@click.argument('filename', type=click.Path(exists=True), required=False)
@click.option('-c', 'code', help='Program passed in as string.')
@click.option(
    '--node-threshold',
    default=DEFAULT_NODE_THRESHOLD,
    help='Prune graph nodes below this threshold.')
@click.option(
    '--edge-threshold',
    default=DEFAULT_EDGE_THRESHOLD,
    help='Prune graph edges below this threshold.')
@click.option(
    '--output',
    '-o',
    'graph_filename',
    default=DEFAULT_GRAPH_FILENAME,
    help='Graph image output filename.')
@click.option(
    '--view/--no-view',
    default=DEFAULT_VIEW,
    help='Automatically open output file after profiling.')
def main(filename, code, graph_filename, node_threshold, edge_threshold, view):
    if filename:
        profile_file(
            filename=filename,
            graph_filename=graph_filename,
            node_threshold=node_threshold,
            edge_threshold=edge_threshold,
            view=view)
    elif code:
        profile_code(
            code=code,
            graph_filename=graph_filename,
            node_threshold=node_threshold,
            edge_threshold=edge_threshold,
            view=view)


if __name__ == "__main__":
    main()
