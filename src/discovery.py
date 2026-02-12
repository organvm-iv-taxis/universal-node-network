"""Discovery module for automatic node detection and registration.

Provides service discovery mechanisms that allow new nodes to announce
themselves and existing nodes to find peers by capability or organ affiliation.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Any

from .node import Node, NodeCapability, NodeStatus


@dataclass
class DiscoveryAnnouncement:
    """A broadcast announcement from a node seeking to join the network."""

    node_id: str
    organ: str
    endpoint: str
    capabilities: list[str]
    timestamp: datetime = field(default_factory=datetime.now)
    ttl_seconds: int = 300

    def is_expired(self) -> bool:
        """Check if this announcement has exceeded its time-to-live."""
        return datetime.now() > self.timestamp + timedelta(seconds=self.ttl_seconds)


class DiscoveryService:
    """Manages node discovery, announcement processing, and peer resolution.

    Nodes announce themselves through this service, which validates
    announcements and facilitates peer-to-peer discovery.
    """

    def __init__(self) -> None:
        self._announcements: dict[str, DiscoveryAnnouncement] = {}
        self._known_nodes: dict[str, Node] = {}

    def announce(self, announcement: DiscoveryAnnouncement) -> Node:
        """Process a node announcement and register the node.

        Args:
            announcement: The discovery announcement to process.

        Returns:
            The registered (or updated) Node object.
        """
        self._announcements[announcement.node_id] = announcement

        if announcement.node_id in self._known_nodes:
            node = self._known_nodes[announcement.node_id]
            node.heartbeat()
            return node

        node = Node(
            node_id=announcement.node_id,
            organ=announcement.organ,
            endpoint=announcement.endpoint,
        )
        for cap_name in announcement.capabilities:
            node.register_capability(NodeCapability(name=cap_name, version="1.0"))
        node.heartbeat()
        self._known_nodes[announcement.node_id] = node
        return node

    def find_peers(self, organ: str | None = None, capability: str | None = None) -> list[Node]:
        """Find nodes matching organ and/or capability criteria.

        Args:
            organ: Filter by organ affiliation (optional).
            capability: Filter by capability name (optional).

        Returns:
            List of matching online nodes.
        """
        results = list(self._known_nodes.values())

        if organ is not None:
            results = [n for n in results if n.organ == organ]
        if capability is not None:
            results = [n for n in results if n.has_capability(capability)]

        return [n for n in results if n.status == NodeStatus.ONLINE]

    def prune_expired(self) -> int:
        """Remove expired announcements and mark their nodes offline.

        Returns:
            Number of nodes marked offline.
        """
        pruned = 0
        expired_ids = [
            aid for aid, ann in self._announcements.items() if ann.is_expired()
        ]
        for node_id in expired_ids:
            del self._announcements[node_id]
            if node_id in self._known_nodes:
                self._known_nodes[node_id].go_offline()
                pruned += 1
        return pruned

    @property
    def active_count(self) -> int:
        """Number of currently online nodes."""
        return sum(1 for n in self._known_nodes.values() if n.status == NodeStatus.ONLINE)
