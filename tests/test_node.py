"""Tests for the node module."""

from src.node import Node, NodeCapability, NodeStatus


def test_node_heartbeat_transitions_to_online():
    """A node in INITIALIZING state should transition to ONLINE on heartbeat."""
    node = Node(node_id="N1", organ="taxis", endpoint="http://localhost:8000")
    assert node.status == NodeStatus.INITIALIZING
    node.heartbeat()
    assert node.status == NodeStatus.ONLINE
    assert node.last_heartbeat is not None


def test_node_register_capability():
    """Registering a capability should make it discoverable."""
    node = Node(node_id="N1", organ="taxis", endpoint="http://localhost:8000")
    cap = NodeCapability(name="routing", version="1.0")
    node.register_capability(cap)
    assert node.has_capability("routing") is True
    assert node.has_capability("unknown") is False


def test_node_rejects_duplicate_capability():
    """Registering a duplicate capability name should raise ValueError."""
    node = Node(node_id="N1", organ="taxis", endpoint="http://localhost:8000")
    cap = NodeCapability(name="routing", version="1.0")
    node.register_capability(cap)
    try:
        node.register_capability(cap)
        assert False, "Should have raised ValueError"
    except ValueError:
        pass


def test_node_to_registry_entry():
    """Registry entry should contain all essential fields."""
    node = Node(node_id="N1", organ="taxis", endpoint="http://localhost:8000")
    node.heartbeat()
    entry = node.to_registry_entry()
    assert entry["node_id"] == "N1"
    assert entry["status"] == "online"
    assert entry["last_heartbeat"] is not None
