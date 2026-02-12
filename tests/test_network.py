"""Tests for the network module."""

from src.node import Node, NodeCapability
from src.network import Network


def test_network_register_and_connect():
    """Registering nodes and connecting them should create a route."""
    net = Network()
    n1 = Node(node_id="N1", organ="taxis", endpoint="http://n1")
    n2 = Node(node_id="N2", organ="theoria", endpoint="http://n2")
    net.register_node(n1)
    net.register_node(n2)
    route = net.connect("N1", "N2", latency_ms=5.0)
    assert route.active is True
    assert route.latency_ms == 5.0


def test_network_rejects_duplicate_node():
    """Registering a node with duplicate ID should raise ValueError."""
    net = Network()
    n1 = Node(node_id="N1", organ="taxis", endpoint="http://n1")
    net.register_node(n1)
    try:
        net.register_node(n1)
        assert False, "Should have raised ValueError"
    except ValueError:
        pass


def test_network_find_by_capability():
    """find_nodes_by_capability should return only online matching nodes."""
    net = Network()
    n1 = Node(node_id="N1", organ="taxis", endpoint="http://n1")
    n1.register_capability(NodeCapability(name="routing", version="1.0"))
    n1.heartbeat()
    n2 = Node(node_id="N2", organ="theoria", endpoint="http://n2")
    n2.heartbeat()
    net.register_node(n1)
    net.register_node(n2)
    results = net.find_nodes_by_capability("routing")
    assert len(results) == 1
    assert results[0].node_id == "N1"


def test_network_topology_summary():
    """Topology summary should reflect current network state."""
    net = Network()
    n1 = Node(node_id="N1", organ="taxis", endpoint="http://n1")
    n1.heartbeat()
    net.register_node(n1)
    summary = net.topology_summary()
    assert summary["total_nodes"] == 1
    assert summary["status_distribution"]["online"] == 1
