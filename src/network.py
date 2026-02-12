"""Network module for topology management and message routing.

Manages the mesh of nodes, tracks connections, and provides
routing logic for inter-organ communication.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .node import Node, NodeStatus


@dataclass
class Route:
    """A path between two nodes in the network."""

    source_id: str
    target_id: str
    latency_ms: float = 0.0
    active: bool = True


class Network:
    """The universal node network topology manager.

    Maintains a registry of nodes and their interconnections,
    supports capability-based routing and health monitoring.
    """

    def __init__(self) -> None:
        self._nodes: dict[str, Node] = {}
        self._routes: list[Route] = []

    def register_node(self, node: Node) -> None:
        """Add a node to the network.

        Args:
            node: The node to register.

        Raises:
            ValueError: If a node with the same ID already exists.
        """
        if node.node_id in self._nodes:
            raise ValueError(f"Node '{node.node_id}' already registered")
        self._nodes[node.node_id] = node

    def connect(self, source_id: str, target_id: str, latency_ms: float = 0.0) -> Route:
        """Establish a route between two nodes.

        Args:
            source_id: ID of the source node.
            target_id: ID of the target node.
            latency_ms: Expected latency in milliseconds.

        Raises:
            KeyError: If either node is not registered.
        """
        if source_id not in self._nodes:
            raise KeyError(f"Source node '{source_id}' not found")
        if target_id not in self._nodes:
            raise KeyError(f"Target node '{target_id}' not found")
        route = Route(source_id=source_id, target_id=target_id, latency_ms=latency_ms)
        self._routes.append(route)
        return route

    def find_nodes_by_capability(self, capability_name: str) -> list[Node]:
        """Find all online nodes that provide a given capability.

        Args:
            capability_name: The capability to search for.

        Returns:
            List of nodes providing the capability and currently online.
        """
        return [
            node for node in self._nodes.values()
            if node.has_capability(capability_name) and node.status == NodeStatus.ONLINE
        ]

    def get_node(self, node_id: str) -> Node:
        """Retrieve a node by ID.

        Raises:
            KeyError: If the node is not registered.
        """
        return self._nodes[node_id]

    def topology_summary(self) -> dict[str, Any]:
        """Generate a summary of the current network topology."""
        status_counts: dict[str, int] = {}
        for node in self._nodes.values():
            status_counts[node.status.value] = status_counts.get(node.status.value, 0) + 1

        return {
            "total_nodes": len(self._nodes),
            "total_routes": len(self._routes),
            "active_routes": sum(1 for r in self._routes if r.active),
            "status_distribution": status_counts,
        }

    @property
    def node_ids(self) -> list[str]:
        """Return all registered node IDs."""
        return list(self._nodes.keys())