[![ORGAN-IV: Taxis](https://img.shields.io/badge/ORGAN--IV-Taxis-e65100?style=flat-square)](https://github.com/organvm-iv-taxis)
[![License: Unlicense](https://img.shields.io/badge/License-Unlicense-blue?style=flat-square)](LICENSE)
[![Status: In Development](https://img.shields.io/badge/Status-In_Development-yellow?style=flat-square)](#roadmap)

# Universal Node Network

[![CI](https://github.com/organvm-iv-taxis/universal-node-network/actions/workflows/ci.yml/badge.svg)](https://github.com/organvm-iv-taxis/universal-node-network/actions/workflows/ci.yml)
[![Coverage](https://img.shields.io/badge/coverage-pending-lightgrey)](https://github.com/organvm-iv-taxis/universal-node-network)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://github.com/organvm-iv-taxis/universal-node-network/blob/main/LICENSE)
[![Organ IV](https://img.shields.io/badge/Organ-IV%20Taxis-10B981)](https://github.com/organvm-iv-taxis)
[![Status](https://img.shields.io/badge/status-active-brightgreen)](https://github.com/organvm-iv-taxis/universal-node-network)
[![Shell](https://img.shields.io/badge/lang-Shell-informational)](https://github.com/organvm-iv-taxis/universal-node-network)


**Distributed node network infrastructure for decentralized cross-organ communication.**

Universal Node Network (UNN) provides the communication backbone for the [ORGAN system](https://github.com/meta-organvm) — a topology-aware message routing layer that enables autonomous nodes across all eight organs to discover each other, negotiate capabilities, and exchange structured messages without centralized brokers. Where [agentic-titan](https://github.com/organvm-iv-taxis/agentic-titan) orchestrates *agent intelligence* and [petasum-super-petasum](https://github.com/organvm-iv-taxis/petasum-super-petasum) manages *layered abstraction*, UNN handles the raw plumbing: node identity, network topology, message serialization, and reliable delivery across organizational boundaries.

---

## Table of Contents

- [Product Overview](#product-overview)
- [Why a Custom Node Network](#why-a-custom-node-network)
- [Orchestration Philosophy](#orchestration-philosophy)
- [Planned Architecture](#planned-architecture)
  - [Network Topology](#network-topology)
  - [Node Registration and Identity](#node-registration-and-identity)
  - [Message Routing](#message-routing)
  - [Cross-Organ Communication Protocol](#cross-organ-communication-protocol)
- [Relationship to ORGAN-IV Siblings](#relationship-to-organ-iv-siblings)
- [Cross-Organ References](#cross-organ-references)
- [Related Work and Prior Art](#related-work-and-prior-art)
- [Roadmap](#roadmap)
- [Contributing](#contributing)
- [License](#license)
- [Author](#author)

---

## Product Overview

The ORGAN system spans eight GitHub organizations, each governing a distinct domain — from theoretical research (ORGAN-I: Theoria) through art (ORGAN-II: Poiesis), commerce (ORGAN-III: Ergon), orchestration (ORGAN-IV: Taxis), public process (ORGAN-V: Logos), community (ORGAN-VI: Koinonia), marketing (ORGAN-VII: Kerygma), and meta-governance (ORGAN-VIII: Meta). Each organ contains multiple repositories, each repository potentially running autonomous agents, CI/CD pipelines, and event-driven workflows. The question that Universal Node Network answers is straightforward: **how do all of these moving parts find and talk to each other?**

UNN is not a general-purpose message queue or a Kubernetes service mesh. It is a purpose-built communication layer designed for a specific organizational topology — one where nodes are identified by their organ membership, where message routing respects the directional dependency constraints of the system (ORGAN-I feeds ORGAN-II feeds ORGAN-III; never the reverse), and where every node must be discoverable without a central registry server running 24/7.

### Core Capabilities (Planned)

| Capability | Description |
|-----------|-------------|
| **Node Discovery** | Decentralized peer-finding via organ-scoped manifests and DNS-like resolution |
| **Topology Awareness** | Routing decisions informed by organ hierarchy and dependency direction |
| **Message Serialization** | Structured envelope format with schema versioning and backward compatibility |
| **Reliable Delivery** | At-least-once delivery semantics with idempotent message processing |
| **Cross-Org Bridging** | Secure message relay between GitHub organizations without shared infrastructure |
| **Health Propagation** | Liveness and readiness signals that flow through the network topology |
| **Capability Negotiation** | Nodes advertise what they can do; senders route to capable receivers |

### What UNN Is Not

- **Not a job queue.** It does not schedule or execute tasks. That is [agentic-titan](https://github.com/organvm-iv-taxis/agentic-titan)'s domain.
- **Not an abstraction layer.** It does not wrap APIs or normalize interfaces. That is [petasum-super-petasum](https://github.com/organvm-iv-taxis/petasum-super-petasum)'s role.
- **Not a database.** It does not persist state beyond what is needed for reliable delivery. State lives in each organ's own repositories.
- **Not a monitoring system.** It carries health signals but does not aggregate or visualize them.

---

## Why a Custom Node Network

A reasonable question: why not just use RabbitMQ, NATS, or a service mesh like Istio? The answer has three parts.

**1. Organizational topology is the routing topology.** In most distributed systems, the network topology is determined by infrastructure — which servers exist, which subnets they occupy, which load balancers front them. In the ORGAN system, topology is determined by *organizational structure*. A message from ORGAN-I to ORGAN-III must conceptually pass through ORGAN-II (or at minimum, respect the dependency direction). Off-the-shelf message brokers have no concept of organizational hierarchy; they route by topic, queue name, or IP address. UNN routes by organ identity.

**2. The system is intermittent, not always-on.** The ORGAN system is not a cloud-deployed microservice architecture running on Kubernetes. It is a constellation of GitHub repositories, GitHub Actions workflows, local development environments, and periodic agent runs. Nodes come and go. A broker-based architecture assumes the broker is always running. UNN assumes nothing is always running and uses a gossip-inspired protocol to reconstruct topology from whatever nodes happen to be alive at any given moment.

**3. Cross-organization security boundaries matter.** Each of the eight GitHub organizations is a distinct security boundary. Messages crossing org boundaries carry different trust levels than messages within an org. UNN's envelope format includes provenance metadata — which org sent the message, which node within that org, and what capability was invoked — enabling fine-grained access control at the organ level without requiring a centralized identity provider.

---

## Orchestration Philosophy

UNN follows three guiding design principles that align with ORGAN-IV's broader orchestration mandate:

### Principle 1: No Single Point of Failure

There is no central broker, no master node, no coordination server. Every node in the network can operate independently. When two nodes can see each other, they communicate directly. When they cannot, messages are queued locally and forwarded when connectivity is restored. This is not eventual consistency in the database sense — it is eventual *reachability* in the network sense.

### Principle 2: Topology Encodes Governance

The dependency graph of the eight-organ system (`I → II → III`; `IV` orchestrates; `V–VII` distribute; `VIII` governs) is not just a planning document — it is encoded directly into UNN's routing tables. A message from ORGAN-III to ORGAN-I is not just unusual; it is *structurally invalid* and will be rejected at the routing layer. This enforcement is not a policy bolt-on; it is intrinsic to how the network operates. The network *is* the governance model, made executable.

### Principle 3: Capability Over Identity

Nodes do not address messages to specific nodes by name. They address messages to *capabilities*. A node that needs "text generation" sends a capability request; UNN resolves it to the nearest capable node (likely in ORGAN-I or ORGAN-II). A node that needs "revenue projection" addresses the capability; UNN routes to ORGAN-III. This decouples senders from receivers and allows the network to evolve — nodes can be added, removed, or replaced without updating every sender's configuration.

---

## Planned Architecture

### Network Topology

UNN uses a **hierarchical mesh** topology. Within each organ, nodes form a fully connected mesh (every node can reach every other node in the same organ). Between organs, designated **bridge nodes** handle cross-organ traffic. Bridge nodes are the only nodes that maintain connections outside their own organ.

```
ORGAN-I (Theoria)              ORGAN-II (Poiesis)
┌──────────────────┐           ┌──────────────────┐
│  Node A ←→ Node B│           │  Node E ←→ Node F│
│    ↕         ↕   │           │    ↕         ↕   │
│  Node C ←→ Node D│           │  Node G ←→ Node H│
│         ↕        │           │         ↕        │
│    [Bridge-I]────┼───────────┼───→[Bridge-II]   │
└──────────────────┘           └──────────────────┘
                                        │
                                        ↓
                               ORGAN-III (Ergon)
                               ┌──────────────────┐
                               │  [Bridge-III]     │
                               │    ↕         ↕    │
                               │  Node J ←→ Node K │
                               └──────────────────┘
```

The bridge node pattern ensures that cross-organ traffic is auditable (all inter-organ messages pass through a known point), governable (bridge nodes enforce dependency-direction rules), and isolatable (if an organ needs to be taken offline, only its bridge node needs to be disconnected).

### Node Registration and Identity

Every node in UNN has a **Fully Qualified Node Identifier (FQNI)** that encodes its position in the organizational hierarchy:

```
<organ-number>.<repo-name>.<node-role>.<instance-id>
```

Examples:
- `iv.agentic-titan.orchestrator.01` — the primary orchestrator node in agentic-titan
- `i.recursive-engine.generator.03` — the third generator instance in recursive-engine
- `iii.public-record-data-scrapper.ingester.01` — the ingestion node for the data scraper

Node registration is **manifest-based**. Each repository that participates in UNN maintains a `unn-manifest.yaml` file at its root that declares the node's identity, capabilities, and communication preferences:

```yaml
# unn-manifest.yaml
unn_version: "0.1"
organ: iv
repo: universal-node-network
nodes:
  - role: bridge
    instance: "01"
    capabilities:
      - cross-organ-relay
      - topology-sync
      - health-aggregation
    protocols:
      - unn-envelope/v1
    endpoints:
      webhook: "https://example.com/unn/webhook"
      github_dispatch: true
```

There is no central registration server. Topology is reconstructed by scanning manifests across repositories — either via GitHub API traversal or via cached topology snapshots distributed through the network itself.

### Message Routing

Messages in UNN are wrapped in a **UNN Envelope** — a structured JSON format that carries routing metadata, provenance information, and the payload:

```json
{
  "unn_version": "0.1",
  "envelope_id": "e-20260210-iv-001",
  "source": {
    "fqni": "iv.universal-node-network.bridge.01",
    "organ": "iv",
    "timestamp": "2026-02-10T12:00:00Z"
  },
  "destination": {
    "capability": "text-generation",
    "organ_hint": "i",
    "priority": "normal"
  },
  "routing": {
    "hops": [],
    "max_hops": 4,
    "direction_constraint": "downstream"
  },
  "payload": {
    "type": "capability-request",
    "schema": "unn-capability-request/v1",
    "data": { }
  },
  "signatures": {
    "source_org": "sha256:..."
  }
}
```

Routing follows a deterministic algorithm:

1. **Local resolution:** If the destination capability exists within the same organ, route locally (zero bridge hops).
2. **Directional resolution:** If the capability requires a different organ, check the dependency graph. If the target organ is reachable in the allowed direction, forward to the local bridge node.
3. **Bridge relay:** The bridge node forwards to the target organ's bridge node, which performs local resolution within the target organ.
4. **Failure handling:** If no capable node is found, the envelope is returned to the sender with an `unroutable` status. If the bridge node is unreachable, the message is queued locally with exponential backoff.

### Cross-Organ Communication Protocol

Cross-organ communication uses one of two transport mechanisms, selected based on context:

**GitHub Actions Dispatch (primary):** For asynchronous, event-driven communication, UNN uses GitHub's `repository_dispatch` API. A bridge node in ORGAN-I can trigger a workflow in an ORGAN-II repository by dispatching a custom event carrying the UNN envelope as the payload. This requires no infrastructure beyond GitHub itself and respects org-level permissions.

**Webhook Relay (secondary):** For lower-latency communication when nodes are running as persistent processes (e.g., during local development or in a deployed environment), UNN supports direct webhook delivery. The envelope is POSTed to the destination node's registered endpoint. Webhook endpoints are optional — nodes that only participate via GitHub Actions do not need them.

Both transports carry the same UNN envelope format, ensuring that message handling logic is transport-agnostic.

---

## Relationship to ORGAN-IV Siblings

ORGAN-IV (Taxis) contains three core infrastructure repositories that form a layered orchestration stack:

| Layer | Repository | Role |
|-------|-----------|------|
| **Intelligence** | [agentic-titan](https://github.com/organvm-iv-taxis/agentic-titan) | Agent swarm orchestration — decides *what* to do and *who* does it |
| **Abstraction** | [petasum-super-petasum](https://github.com/organvm-iv-taxis/petasum-super-petasum) | Layered abstraction framework — normalizes interfaces between heterogeneous systems |
| **Communication** | **universal-node-network** (this repo) | Node discovery and message routing — handles *how* nodes find and talk to each other |

The three repositories have distinct responsibilities but tight integration points:

- **agentic-titan → UNN:** When agentic-titan dispatches an agent to perform a task in a remote organ, it uses UNN to locate capable nodes and deliver task envelopes. Titan decides *what* needs to happen; UNN figures out *where* to send the request.
- **petasum-super-petasum → UNN:** Petasum's abstraction layers present a uniform interface to consumers. When that interface needs to reach a concrete implementation in a specific organ, it hands off to UNN for routing. Petasum decides *how* to represent the request; UNN decides *how to deliver* it.
- **UNN → both:** UNN provides topology information back to both siblings. Titan uses topology data to make intelligent scheduling decisions (don't assign a task to an organ whose bridge is down). Petasum uses topology data to select the appropriate abstraction layer for the current network state.

This separation of concerns — intelligence, abstraction, communication — mirrors the classic distributed systems decomposition of *policy*, *mechanism*, and *transport*.

---

## Cross-Organ References

UNN is a horizontal infrastructure layer that touches every organ. Here is how it relates to each:

| Organ | Relationship |
|-------|-------------|
| **I — Theoria** | Hosts theory-generating nodes (recursive-engine, epistemic frameworks). UNN routes capability requests for generative and analytical tasks to ORGAN-I nodes. |
| **II — Poiesis** | Hosts creative production nodes (metasystem-master, generative art). UNN enables ORGAN-I outputs to flow downstream into ORGAN-II creative pipelines. |
| **III — Ergon** | Hosts commercial product nodes (data scrapers, SaaS tools). UNN routes productized outputs from ORGAN-II into ORGAN-III delivery pipelines. |
| **IV — Taxis** | Home organ. UNN is one of three core orchestration tools alongside agentic-titan and petasum-super-petasum. |
| **V — Logos** | Hosts public process documentation. UNN carries publication events (essay published, build log updated) as broadcast messages. |
| **VI — Koinonia** | Hosts community coordination. UNN delivers event notifications (salon scheduled, reading group formed) across organs. |
| **VII — Kerygma** | Hosts marketing distribution. UNN triggers POSSE distribution workflows when content is published in other organs. |
| **VIII — Meta** | Governs all organs. UNN topology data feeds into meta-level health dashboards and governance reports. |

---

## Related Work and Prior Art

UNN draws inspiration from several established approaches to distributed communication, while adapting them to the specific constraints of an organization-as-network model.

### Service Meshes (Istio, Linkerd, Consul Connect)

Service meshes solve a similar routing-and-discovery problem for microservice architectures. They use sidecar proxies (like Envoy) to intercept traffic and apply routing rules, retries, and observability. UNN borrows the concept of transparent routing and capability-based discovery but does not use sidecar proxies — nodes in UNN are not long-running containers but intermittent processes triggered by events. The mesh metaphor applies at the organizational level, not the infrastructure level.

### Message Brokers (RabbitMQ, Apache Kafka, NATS)

Broker-based systems provide reliable message delivery through a central intermediary. UNN's bridge nodes serve a similar relay function but are not centralized — each organ has its own bridge, and no single bridge handles all traffic. UNN's at-least-once delivery semantics are inspired by Kafka's consumer group model, but without the persistent log (messages are ephemeral once acknowledged).

### Pub/Sub Systems (Google Pub/Sub, AWS SNS/SQS)

Cloud pub/sub systems provide topic-based fanout — publish to a topic, all subscribers receive. UNN supports a similar broadcast pattern for organ-wide announcements but prefers capability-addressed unicast for most traffic. The key difference is that UNN topics are not arbitrary strings but organ-scoped capabilities with governance constraints.

### Gossip Protocols (SWIM, Serf, Memberlist)

Gossip protocols propagate cluster membership and health information through randomized peer-to-peer communication. UNN's topology reconstruction mechanism is gossip-inspired — nodes that discover each other share what they know about the broader network, gradually building a complete picture. However, UNN's gossip is structured by organ hierarchy rather than random, which accelerates convergence.

### ActivityPub / Fediverse

The federated social web protocol ActivityPub shares UNN's assumption that the network is composed of autonomous servers (instances) that communicate via standardized message formats. UNN's envelope format is conceptually similar to ActivityPub's Activity objects, and UNN's bridge nodes serve a role analogous to ActivityPub's inbox/outbox forwarding. The key difference is that UNN's federation model is hierarchical (organ-structured) rather than flat (instance-to-instance).

---

## Roadmap

Universal Node Network is currently in the **design and specification phase**. The implementation roadmap follows ORGAN-IV's broader sprint schedule.

### Phase 1 — Specification (Current)

- [ ] Define UNN Envelope schema (JSON Schema + protobuf)
- [ ] Define `unn-manifest.yaml` schema
- [ ] Document FQNI naming convention
- [ ] Specify bridge node protocol
- [ ] Write architectural decision records (ADRs) for key design choices
- [ ] Validate routing algorithm against organ dependency graph

### Phase 2 — Proof of Concept

- [ ] Implement manifest scanning via GitHub API
- [ ] Build envelope serialization/deserialization library
- [ ] Implement local (intra-organ) message routing
- [ ] Build bridge node prototype using GitHub Actions dispatch
- [ ] Test cross-organ communication between ORGAN-I and ORGAN-II

### Phase 3 — Integration

- [ ] Integrate with agentic-titan's task dispatch system
- [ ] Integrate with petasum-super-petasum's abstraction layers
- [ ] Deploy bridge nodes to all eight organs
- [ ] Implement health propagation and topology sync
- [ ] Build capability registry and resolution logic

### Phase 4 — Hardening

- [ ] Add envelope signing and provenance verification
- [ ] Implement dead-letter handling for unroutable messages
- [ ] Add observability (message tracing, latency metrics)
- [ ] Load test cross-organ routing under realistic traffic patterns
- [ ] Document operational runbooks for bridge node maintenance

---

## Contributing

Universal Node Network is part of the ORGAN system's orchestration layer. Contributions are welcome, particularly in:

- **Protocol design** — refining the UNN Envelope schema and routing algorithm
- **Transport implementations** — adding new transport mechanisms beyond GitHub Dispatch and webhooks
- **Testing** — building integration tests that validate cross-organ communication
- **Documentation** — improving architectural decision records and operational guides

To contribute:

1. Fork this repository
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Commit your changes with clear, descriptive messages
4. Open a pull request against `main`

Please read the [ORGAN-IV contribution guidelines](https://github.com/organvm-iv-taxis/.github/blob/main/CONTRIBUTING.md) before submitting.

---

## License

This project is released into the public domain under the [Unlicense](LICENSE). You are free to copy, modify, publish, use, compile, sell, or distribute this software for any purpose, commercial or non-commercial, and by any means.

---

## Author

**[@4444j99](https://github.com/4444j99)** — architect of the ORGAN system and its orchestration infrastructure.

Universal Node Network is part of [ORGAN-IV: Taxis](https://github.com/organvm-iv-taxis), the orchestration organ of the [ORGAN system](https://github.com/meta-organvm). For the broader system context, see the [meta-organvm](https://github.com/meta-organvm) umbrella organization.
