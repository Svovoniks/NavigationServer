import osmnx as ox


def get_base_graph(start, dest, k=0, incr=0.1, network_type='bike'):
    graph = None
    try:
        graph = ox.graph_from_bbox(
            max(dest[1], start[1]) + incr * k,
            min(dest[1], start[1]) - incr * k,
            max(dest[0], start[0]) + incr * k,
            min(dest[0], start[0]) - incr * k,
            network_type=network_type)
    except Exception as e:
        pass

    return graph


def get_graph(start, dest, k=0, incr=0.1, network_type='bike'):
    graph = get_base_graph(start, dest)

    while graph is None:
        graph = get_base_graph(start, dest, k=k, incr=0.1, network_type=network_type)
        k += 1

    return graph, k


def get_route(graph, start, dest, k=1):
    p1 = ox.nearest_nodes(graph, *start)
    p2 = ox.nearest_nodes(graph, *dest)

    return ox.shortest_path(graph, p1, p2)
