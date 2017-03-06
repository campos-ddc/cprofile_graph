# -*- coding: utf-8 -*-

import click
from cprofile_graph import (DEFAULT_COLOUR_NODES_BY_SELFTIME,
                            DEFAULT_EDGE_THRESHOLD, DEFAULT_GRAPH_FILENAME,
                            DEFAULT_NODE_THRESHOLD, DEFAULT_VIEW, profile_code,
                            profile_file)


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
@click.option(
    '--colour-nodes-by-selftime',
    default=DEFAULT_COLOUR_NODES_BY_SELFTIME,
    help='Colour nodes by self time, rather than by total time '
    '(sum of self and descendants)')
def main(filename, code, graph_filename, node_threshold, edge_threshold, view,
         colour_nodes_by_selftime):

    if filename:
        profile_file(
            filename=filename,
            graph_filename=graph_filename,
            node_threshold=node_threshold,
            edge_threshold=edge_threshold,
            view=view,
            colour_nodes_by_selftime=colour_nodes_by_selftime)

    elif code:
        profile_code(
            code=code,
            graph_filename=graph_filename,
            node_threshold=node_threshold,
            edge_threshold=edge_threshold,
            view=view,
            colour_nodes_by_selftime=colour_nodes_by_selftime)


if __name__ == "__main__":
    main()
