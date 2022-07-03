"""Test core objects/concepts
"""
# pylint: disable=C0103
import warnings

with warnings.catch_warnings():
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    from geopandas import GeoDataFrame

from pandas.testing import assert_frame_equal
from pytest import fixture, mark
from shapely.geometry import Point, LineString, MultiPoint

try:
    import networkx as nx
    from networkx.utils.misc import graphs_equal

    USE_NX = True
except ImportError:
    USE_NX = False

import snkit
import snkit.network


def assert_frame_not_equal(*args, **kwargs):
    try:
        assert_frame_equal(*args, **kwargs)
    except AssertionError:
        pass
    else:
        raise AssertionError


@fixture
def edge_only():
    """Single edge:
    |
    |
    |
    """
    edge = LineString([(0, 0), (0, 2)])
    edges = GeoDataFrame([{"geometry": edge}])
    return snkit.Network(edges=edges)


@fixture
def nodes_only():
    """Two nodes:
    x

    x
    """
    a = Point((0, 0))
    b = Point((0, 2))
    nodes = GeoDataFrame([{"geometry": a}, {"geometry": b}])
    return snkit.Network(nodes=nodes)


@fixture
def connected():
    """Edge with nodes:
    b
    |
    a
    """
    a = Point((0, 0))
    b = Point((0, 2))
    edge = LineString([a, b])
    edges = GeoDataFrame([{"geometry": edge}])
    nodes = GeoDataFrame([{"geometry": a}, {"geometry": b}])
    return snkit.Network(edges=edges, nodes=nodes)


@fixture
def misaligned():
    """Edge with nodes offset:
    b |
      |
      | a
    """
    edge = LineString([(0, 0), (0, 2)])
    a = Point((0.5, 0))
    b = Point((-0.5, 2))
    edges = GeoDataFrame([{"geometry": edge}])
    nodes = GeoDataFrame([{"geometry": a}, {"geometry": b}])
    return snkit.Network(edges=edges, nodes=nodes)


@fixture
def unsplit():
    """T-junction with nodes, long edge not split:
    b
    |
    |c--d
    |
    a
    """
    a = Point((0, 0))
    b = Point((0, 2))
    c = Point((0, 1))
    d = Point((1, 1))
    ab = LineString([a, b])
    cd = LineString([c, d])
    edges = GeoDataFrame([ab, cd], columns=["geometry"])
    nodes = GeoDataFrame([a, b, c, d], columns=["geometry"])
    return snkit.Network(edges=edges, nodes=nodes)


@fixture
def split():
    """T-junction with nodes, long edge split:
    b
    |
    c--d
    |
    a
    """
    a = Point((0, 0))
    b = Point((0, 2))
    c = Point((0, 1))
    d = Point((1, 1))
    nodes = GeoDataFrame([a, b, c, d], columns=["geometry"])
    ac = LineString([a, c])
    cb = LineString([c, b])
    cd = LineString([c, d])
    edges = GeoDataFrame([ac, cb, cd], columns=["geometry"])
    return snkit.Network(edges=edges, nodes=nodes)


@fixture
def split_with_ids():
    """T-junction with nodes, long edge split, and node and edge ids:
     b
    2| 3
     c---d
    1|
     a
    """
    a = Point((0, 0))
    b = Point((0, 2))
    c = Point((0, 1))
    d = Point((1, 1))
    nodes = GeoDataFrame(data={"geometry": [a, b, c, d], "id": ["a", "b", "c", "d"]})
    ac = LineString([a, c])
    cb = LineString([c, b])
    cd = LineString([c, d])
    edges = GeoDataFrame(data={"geometry": [ac, cb, cd], "id": [1, 2, 3]})
    return snkit.Network(edges=edges, nodes=nodes)


@fixture
def unsplit_intersection():
    """Edges intersection, both edges not split
       b
       |
    c--|--d
       |
       a
    """
    a = Point((1, 0))
    b = Point((1, 2))
    c = Point((0, 1))
    d = Point((2, 1))
    nodes = GeoDataFrame(data={"geometry": [a, b, c, d]})
    ab = LineString([a, b])
    cd = LineString([c, d])
    edges = GeoDataFrame(data={"geometry": [ab, cd]})
    return snkit.Network(edges=edges, nodes=nodes)


@fixture
def split_intersection():
    """Edges intersection, both edges split
       b
       |
    c--x--d
       |
       a
    """
    a = Point((1, 0))
    b = Point((1, 2))
    c = Point((0, 1))
    d = Point((2, 1))
    x = Point((1, 1))
    nodes = GeoDataFrame(data={"geometry": [a, b, c, d, x]})
    ax = LineString([a, x])
    xb = LineString([x, b])
    cx = LineString([c, x])
    xd = LineString([x, d])
    edges = GeoDataFrame(data={"geometry": [ax, xb, cx, xd]})
    return snkit.Network(edges=edges, nodes=nodes)


@fixture
def unsplit_multiple_intersections():
    """Multiple edges intersections, all edges unsplit
       b   f
       |   |
    c--|---|--d
       |   |
       a   e
    """
    a = Point((1, 0))
    b = Point((1, 2))
    c = Point((0, 1))
    d = Point((3, 1))
    e = Point((2, 0))
    f = Point((2, 2))
    nodes = GeoDataFrame(data={"geometry": [a, b, c, d, e, f]})
    ab = LineString([a, b])
    cd = LineString([c, d])
    ef = LineString([e, f])
    edges = GeoDataFrame(data={"geometry": [ab, cd, ef]})
    return snkit.Network(edges=edges, nodes=nodes)


@fixture
def split_multiple_intersections():
    """Multiple edges intersections, all edges split
       b   f
       |   |
    c--x---y--d
       |   |
       a   e
    """
    a = Point((1, 0))
    b = Point((1, 2))
    c = Point((0, 1))
    d = Point((3, 1))
    e = Point((2, 0))
    f = Point((2, 2))
    x = Point((1, 1))
    y = Point((2, 1))
    nodes = GeoDataFrame(data={"geometry": [a, b, c, d, e, f, x, y]})
    ax = LineString([a, x])
    xb = LineString([x, b])
    cx = LineString([c, x])
    xy = LineString([x, y])
    yd = LineString([y, d])
    ey = LineString([e, y])
    yf = LineString([y, f])
    edges = GeoDataFrame(data={"geometry": [ax, xb, cx, xy, yd, ey, yf]})
    return snkit.Network(edges=edges, nodes=nodes)


@fixture
def unsplit_overlapping_lines():
    """Overlapping lines for a section
       c--d
       ||
    b--|
       |
       a
    """
    a = Point((1, 0))
    b = Point((0, 1))
    c = Point((1, 2))
    d = Point((2, 2))
    # x is just a construction point
    x = Point((1, 1))
    nodes = GeoDataFrame(data={"geometry": [a, b, c, d]})
    ac = LineString([a, c])
    bd = LineString([b, x, c, d])
    edges = GeoDataFrame(data={"geometry": [ac, bd]})
    return snkit.Network(edges=edges, nodes=nodes)


@fixture
def split_overlapping_lines():
    """Split of overlapping lines for a section
       c--d
       ||
    b--x
       |
       a
    """
    a = Point((1, 0))
    b = Point((0, 1))
    c = Point((1, 2))
    d = Point((2, 2))
    x = Point((1, 1))
    nodes = GeoDataFrame(data={"geometry": [a, b, c, d, x]})
    ax = LineString([a, x])
    bx = LineString([b, x])
    xc = LineString([x, c])
    cd = LineString([c, d])
    # note that there are two edges 'xc'
    edges = GeoDataFrame(data={"geometry": [ax, xc, bx, xc, cd]})
    return snkit.Network(edges=edges, nodes=nodes)


@fixture
def gap():
    """T-junction with nodes, edges not quite intersecting:
    b
    |
    | c--d
    |
    a
    """
    a = Point((0, 0))
    b = Point((0, 2))
    c = Point((0.1, 1))
    d = Point((1, 1))
    nodes = GeoDataFrame([a, b, c, d], columns=["geometry"])
    ab = LineString([a, b])
    cd = LineString([c, d])
    edges = GeoDataFrame([ab, cd], columns=["geometry"])
    return snkit.Network(edges=edges, nodes=nodes)


@fixture
def bridged():
    """T-junction with nodes, bridged by short edge:
    b
    |
    e-c--d
    |
    a
    """
    a = Point((0, 0))
    b = Point((0, 2))
    c = Point((0.1, 1))
    d = Point((1, 1))
    e = Point((0, 1))
    nodes = GeoDataFrame([a, b, c, d, e], columns=["geometry"])
    ae = LineString([a, e])
    eb = LineString([e, b])
    cd = LineString([c, d])
    ce = LineString([c, e])
    edges = GeoDataFrame([ae, eb, cd, ce], columns=["geometry"])
    return snkit.Network(edges=edges, nodes=nodes)


def test_init():
    """Should create an empty network"""
    net = snkit.Network()
    assert len(net.nodes) == 0
    assert len(net.edges) == 0


def test_round_geometries(misaligned, connected):
    """Should round coordinates to some tolerance"""
    rounded = snkit.network.round_geometries(misaligned, precision=0)
    assert_frame_equal(rounded.nodes, connected.nodes)


def test_add_ids(edge_only, connected):
    """Should add ids to network nodes and columns"""
    edge_with_ids = snkit.network.add_ids(edge_only)
    assert list(edge_with_ids.edges.id) == ["edge_0"]
    assert list(edge_with_ids.nodes.id) == []

    net_with_ids = snkit.network.add_ids(connected)
    assert list(net_with_ids.edges.id) == ["edge_0"]
    assert list(net_with_ids.nodes.id) == ["node_0", "node_1"]


def test_add_endpoints(edge_only, connected):
    """Should add nodes at edge endpoints"""
    with_endpoints = snkit.network.add_endpoints(edge_only)
    assert_frame_equal(with_endpoints.nodes, connected.nodes)


def test_snap_nodes(misaligned, connected):
    """Should snap nodes to edges"""
    snapped = snkit.network.snap_nodes(misaligned)
    assert_frame_equal(snapped.nodes, connected.nodes)

    # don't move if under threshold
    snapped = snkit.network.snap_nodes(misaligned, threshold=0.1)
    assert_frame_equal(snapped.nodes, misaligned.nodes)


def test_split_at_nodes(unsplit, split):
    """Should split edges at nodes, duplicating attributes if any"""
    actual = snkit.network.split_edges_at_nodes(unsplit)
    assert_frame_equal(split.edges, actual.edges)


def test_split_at_intersections(unsplit_intersection, split_intersection):
    """Should split edges at edges intersections"""
    actual = snkit.network.split_edges_at_intersections(unsplit_intersection)
    assert_frame_equal(split_intersection.edges, actual.edges)
    assert_frame_equal(split_intersection.nodes, actual.nodes)


def test_split_at_intersection_already_split(split_intersection):
    """Shouldn't do anything"""
    actual = snkit.network.split_edges_at_intersections(split_intersection)
    assert_frame_equal(split_intersection.edges, actual.edges)
    assert_frame_equal(split_intersection.nodes, actual.nodes)


def test_split_at_intersection_endnode(unsplit, split):
    """Should split the edge at the endnode intersection
    There shouldn't be any duplicate (no additional node).
    """
    actual = snkit.network.split_edges_at_intersections(unsplit)
    assert_frame_not_equal(split.edges, actual.edges)
    assert_frame_equal(split.nodes, actual.nodes)


def test_split_at_intersection_multiple(
    unsplit_multiple_intersections, split_multiple_intersections
):
    """Should split the edges at each intersection"""
    actual = snkit.network.split_edges_at_intersections(unsplit_multiple_intersections)
    assert_frame_equal(split_multiple_intersections.edges, actual.edges)
    assert_frame_equal(split_multiple_intersections.nodes, actual.nodes)


def test_split_intersection_overlapping_edges(
    unsplit_overlapping_lines, split_overlapping_lines
):
    """Should split at the start and end of the intersecting sector
    The intersecting sector should be duplicated.
    """
    actual = snkit.network.split_edges_at_intersections(unsplit_overlapping_lines)
    assert_frame_equal(split_overlapping_lines.edges, actual.edges)
    assert_frame_equal(split_overlapping_lines.nodes, actual.nodes)


def test_split_line():
    """Definitively split line at a point"""
    line = LineString(
        [
            (273157.33178339572623372, 5789362.55751010309904814),
            (273134.25517477234825492, 5789314.91026492696255445),
        ]
    )
    point = Point(273151.75418011785950512, 5789351.04119784012436867)
    segments = snkit.network.split_line(line, point)
    assert point.distance(line) < 1e-9
    assert len(segments) == 2

    line = LineString(
        [
            (1038390.701003063, 6945982.90058485),
            (1037867.399055927, 6943088.583528072),
        ]
    )
    points = MultiPoint(
        [
            (1037867.399055927, 6943088.583528072),
            (1037867.399081285, 6943088.583668322),
            (1037867.400031154, 6943088.583835071),
            (1038390.701003063, 6945982.90058485),
            (1038390.701021349, 6945982.900686138),
            (1038390.701061018, 6945982.900786115),
        ]
    )
    segments = snkit.network.split_line(line, points, tolerance=1e-3)
    for point in points.geoms:
        assert point.distance(line) < 1e-3
    assert len(segments) == 5

    line = LineString(
        [
            (1111849.810325465, 6791469.122112891),  # 1
            (1111935.678092212, 6791104.869596513),  # 2
            (1112151.958236065, 6790264.085704206),  # 3
            (1112606.312094527, 6789678.939913818),  # 4
            (1112725.292801428, 6789178.128700008),  # 5
            (1112796.932870851, 6789012.113559419),  # 6
            (1112886.754280969, 6788371.470671637),  # 7
            (1112942.209796557, 6787971.608098711),  # 8
        ]
    )
    points = MultiPoint(
        [
            (1111849.810325465, 6791469.122112891),  # 1
            (1112942.209819941, 6787971.607780417),  # a
            (1112942.210585088, 6787971.609669216),  # b
            (1111849.810544952, 6791469.121181826),  # c
            (1112942.209796557, 6787971.608098711),  # 8
        ]
    )

    segments = snkit.network.split_line(line, points, tolerance=1e-3)
    for point in points.geoms:
        assert point.distance(line) < 1e-3
    for segment in segments:
        print(segment)
    assert len(segments) == len(points.geoms) - 1

    # consider duplicate points in linestring or in multipoint
    # consider points which will be considered duplicate within tolerance


def test_link_nodes_to_edges_within(gap, bridged):
    """Nodes should link to edges within a distance, splitting the node at a new point if
    necessary.
    """
    actual = snkit.network.link_nodes_to_edges_within(gap, distance=0.1)
    assert_frame_equal(actual.nodes, bridged.nodes)
    assert_frame_equal(actual.edges, bridged.edges)


def test_assign_topology(split_with_ids):
    """Given network
     b
    2| 3
     c---d
    1|
     a
    """
    topo = snkit.network.add_topology(split_with_ids)
    assert list(topo.nodes.id) == ["a", "b", "c", "d"]
    expected = [
        # edge id, alpha-sorted node ids
        (1, ("a", "c")),
        (2, ("b", "c")),
        (3, ("c", "d")),
    ]
    actual = []
    for edge in topo.edges.itertuples():
        edge_id = edge.id
        from_id = edge.from_id
        to_id = edge.to_id
        if from_id < to_id:
            edge_tuple = (edge_id, (from_id, to_id))
        else:
            edge_tuple = (edge_id, (to_id, from_id))
        actual.append(edge_tuple)

    # sort by edge_id
    actual = sorted(actual, key=lambda edge_tuple: edge_tuple[0])
    assert actual == expected


def test_passing_slice():
    """Passing a partial dataframe through add_ids should work fine, resetting index"""
    a = Point((0, 0))
    b = Point((0, 2))
    c = Point((0, 1))
    d = Point((1, 1))
    ac = LineString([a, c])
    cb = LineString([c, b])
    cd = LineString([c, d])
    edges = GeoDataFrame([ac, cb, cd], columns=["geometry"])
    network = snkit.Network(edges=edges[1:])
    with_endpoints = snkit.network.add_endpoints(network)
    with_ids = snkit.network.add_ids(with_endpoints)

    actual = with_ids.edges
    expected = GeoDataFrame(
        [(cb, "edge_0"), (cd, "edge_1")], columns=["geometry", "id"]
    )

    print(actual)
    assert_frame_equal(actual, expected)


@mark.skipif(not USE_NX, reason="networkx not available")
def test_to_networkx(connected):
    """Test conversion to networkx"""
    connected.nodes["id"] = ["n" + str(i) for i in connected.nodes.index]
    connected = snkit.network.add_topology(connected)
    G = snkit.network.to_networkx(connected)

    G_true = nx.Graph()
    G_true.add_node("n0", pos=(0, 0))
    G_true.add_node("n1", pos=(0, 2))
    G_true.add_edge("n0", "n1", weight=2)

    assert graphs_equal(G, G_true)
