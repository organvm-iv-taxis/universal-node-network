"""Tests for HierarchyNetwork and LensDiscovery extensions."""

from src.discovery import LensDiscovery
from src.network import HierarchyNetwork


def test_hierarchy_network_populates_21_nodes():
    """HierarchyNetwork should contain all 21 lens nodes."""
    net = HierarchyNetwork()
    summary = net.topology_summary()
    assert summary["total_nodes"] == 21


def test_hierarchy_network_has_edges():
    """HierarchyNetwork should have cross-stratum + strange loop edges."""
    net = HierarchyNetwork()
    summary = net.topology_summary()
    assert summary["total_routes"] > 0
    assert summary["active_routes"] > 0


def test_hierarchy_network_all_nodes_online():
    """All hierarchy nodes should be online after construction."""
    net = HierarchyNetwork()
    summary = net.topology_summary()
    assert summary["status_distribution"]["online"] == 21


def test_hierarchy_network_get_stratum_nodes():
    """get_stratum_nodes should return nodes for a specific stratum."""
    net = HierarchyNetwork()
    boot_nodes = net.get_stratum_nodes("/boot/")
    assert len(boot_nodes) >= 1
    for n in boot_nodes:
        assert n.organ == "/boot/"


def test_hierarchy_network_get_strange_loop_nodes():
    """get_strange_loop_nodes should return nodes at both loop endpoints."""
    net = HierarchyNetwork()
    loop_nodes = net.get_strange_loop_nodes()
    assert len(loop_nodes) >= 2
    strata = {n.organ for n in loop_nodes}
    assert "/dev/" in strata
    assert "/boot/" in strata


def test_hierarchy_network_nodes_have_capabilities():
    """Each hierarchy node should have category and stratum capabilities."""
    net = HierarchyNetwork()
    node = net.get_node("mathematics")
    assert node.has_capability("structure")
    assert node.has_capability("stratum:/boot/")


def test_hierarchy_network_find_by_capability():
    """find_nodes_by_capability should work for hierarchy nodes."""
    net = HierarchyNetwork()
    generative = net.find_nodes_by_capability("generative")
    assert len(generative) >= 1
    ids = {n.node_id for n in generative}
    assert "chaos" in ids


def test_lens_discovery_finds_lenses():
    """LensDiscovery should return 2-3 lens IDs for a task."""
    discovery = LensDiscovery()
    lenses = discovery.discover_lenses("deploy the product")
    assert 2 <= len(lenses) <= 3
    assert all(isinstance(lid, str) for lid in lenses)


def test_lens_discovery_by_category():
    """discover_by_category should return lenses for the category."""
    discovery = LensDiscovery()
    lenses = discovery.discover_by_category("generative")
    assert len(lenses) >= 1
    assert "chaos" in lenses


def test_lens_discovery_by_category_invalid():
    """discover_by_category should return empty for invalid category."""
    discovery = LensDiscovery()
    lenses = discovery.discover_by_category("nonexistent")
    assert lenses == []


def test_lens_discovery_by_stratum():
    """discover_by_stratum should return lenses for the stratum."""
    discovery = LensDiscovery()
    lenses = discovery.discover_by_stratum("/boot/")
    assert len(lenses) >= 1
    assert "mathematics" in lenses


def test_lens_discovery_by_stratum_invalid():
    """discover_by_stratum should return empty for invalid stratum."""
    discovery = LensDiscovery()
    lenses = discovery.discover_by_stratum("/nonexistent/")
    assert lenses == []
