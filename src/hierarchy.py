"""Universal Hierarchy — the 21 organizational lenses as a data structure.

Each lens represents a way of seeing an organizational system, sourced from
the synthesis of substrate, living, and governance/economic/emergent systems
research. Lenses are organized into 7 strata (inspired by the Unix filesystem
hierarchy), forming a strange loop from chaos (/dev/) back to the noosphere.

The hierarchy is not a permanent analytical framework — lenses are summoned
per-task and released when done (Y7 principle). Holding all simultaneously
exceeds cognitive limits (neuroscience: 7±2 chunks).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class Stratum(Enum):
    """The 7 strata of the universal hierarchy.

    Named after Unix filesystem paths to emphasize that each level
    is a different 'mount point' for organizational reasoning.
    """

    BOOT = "/boot/"    # Foundation: formal structure, decidability
    SYS = "/sys/"      # Substrate: physics, entropy, measurement
    LIB = "/lib/"      # Composition: bonding, valence, reactions
    BIN = "/bin/"       # Architecture: organs, registry, governance
    USR = "/usr/"       # Emergent: coherence, brand, portfolio
    NET = "/net/"       # Environment: market, institutions, culture
    DEV = "/dev/"       # Entropy source: chaos, novelty, the strange loop origin


class LensCategory(Enum):
    """Functional categories for lens selection."""

    TOOLING = "tooling"           # Implementation details
    STRUCTURE = "structure"       # Architectural decisions
    AUTHORITY = "authority"       # Governance questions
    FOUNDATION = "foundation"    # Philosophical questions
    GENERATIVE = "generative"    # Creative questions


@dataclass(frozen=True)
class SystemHouse:
    """A single lens in the universal hierarchy.

    Each house (lens) defines:
    - What it reveals when summoned (adds)
    - What it strips away as noise (strips)
    - What it demands as irreducible (critique)
    - When to summon it (summon_conditions)
    - When to release it (release_conditions)
    """

    lens_id: str
    name: str
    stratum: Stratum
    category: LensCategory
    summon_when: str
    adds: str         # What this lens reveals
    strips: str       # What this lens removes as noise
    critique: str     # What this lens challenges
    release_when: str = "Insight absorbed into task output"
    metadata: dict[str, Any] = field(default_factory=dict)

    def matches_task(self, task_category: LensCategory) -> bool:
        """Check if this lens is appropriate for a task category."""
        return self.category == task_category

    def to_dict(self) -> dict[str, Any]:
        """Export as dictionary."""
        return {
            "lens_id": self.lens_id,
            "name": self.name,
            "stratum": self.stratum.value,
            "category": self.category.value,
            "summon_when": self.summon_when,
            "adds": self.adds,
            "strips": self.strips,
            "critique": self.critique,
            "release_when": self.release_when,
        }


# ---------------------------------------------------------------------------
# The Lens Catalog — all 21 lenses from the synthesis document
# ---------------------------------------------------------------------------

LENS_CATALOG: tuple[SystemHouse, ...] = (
    # /boot/ — Foundation
    SystemHouse(
        lens_id="mathematics",
        name="Mathematics",
        stratum=Stratum.BOOT,
        category=LensCategory.STRUCTURE,
        summon_when="Verifying state machine completeness, formal properties",
        adds="DFA/category theory reveals structural gaps",
        strips="Meaning — only structure remains",
        critique="Cannot capture meaning, only structure",
    ),
    SystemHouse(
        lens_id="information_theory",
        name="Information Theory",
        stratum=Stratum.BOOT,
        category=LensCategory.TOOLING,
        summon_when="Measuring complexity, diagnosing bottlenecks",
        adds="Entropy and compression ratios",
        strips="Value — only surprise remains",
        critique="Cannot capture value, only surprise",
    ),
    SystemHouse(
        lens_id="metaphysics",
        name="Metaphysics",
        stratum=Stratum.BOOT,
        category=LensCategory.FOUNDATION,
        summon_when="Ontological confusion (is this a tool or organism?)",
        adds="Permission for ontological polymorphism",
        strips="Premature classification",
        critique="Can paralyze with infinite alternatives",
    ),

    # /sys/ — Substrate
    SystemHouse(
        lens_id="thermodynamics",
        name="Thermodynamics",
        stratum=Stratum.SYS,
        category=LensCategory.TOOLING,
        summon_when="Diagnosing decay, energy budgets",
        adds="Entropy accumulation is measurable",
        strips="Optimism about maintenance-free systems",
        critique="Treats all disorder as equivalent",
    ),
    SystemHouse(
        lens_id="quantum_mechanics",
        name="Quantum Mechanics",
        stratum=Stratum.SYS,
        category=LensCategory.FOUNDATION,
        summon_when="Understanding measurement effects",
        adds="State is genuinely indefinite between observations",
        strips="False certainty about unobserved states",
        critique="Analogies can overextend to absurdity",
    ),

    # /lib/ — Composition
    SystemHouse(
        lens_id="chemistry",
        name="Chemistry",
        stratum=Stratum.LIB,
        category=LensCategory.TOOLING,
        summon_when="Planning repo composition, auditing bonds",
        adds="Valence rules constrain valid combinations",
        strips="Arbitrary groupings",
        critique="Not all organizational bonds are chemical",
    ),
    SystemHouse(
        lens_id="cosmology",
        name="Cosmology",
        stratum=Stratum.LIB,
        category=LensCategory.FOUNDATION,
        summon_when="Understanding temporal arc",
        adds="The system has epochs, not just states",
        strips="Short-term thinking",
        critique="Cosmological narratives can mythologize mundane history",
    ),

    # /bin/ — Architecture (organismal, cellular, infrastructure)
    SystemHouse(
        lens_id="organismal_biology",
        name="Organismal Biology",
        stratum=Stratum.BIN,
        category=LensCategory.STRUCTURE,
        summon_when="Health diagnostics, system architecture",
        adds="Homeostasis demands automatic response, not just monitoring",
        strips="Passive observation without correction",
        critique="The organism metaphor can anthropomorphize software",
    ),
    SystemHouse(
        lens_id="cellular_biology",
        name="Cellular Biology",
        stratum=Stratum.BIN,
        category=LensCategory.STRUCTURE,
        summon_when="Template design, context sync, repo creation",
        adds="DNA/expression/apoptosis map to seed.yaml/CLAUDE.md/ARCHIVED",
        strips="Treating all repos as permanent",
        critique="Cells don't have agency; repos are artifacts of choice",
    ),
    SystemHouse(
        lens_id="infrastructure",
        name="Infrastructure",
        stratum=Stratum.BIN,
        category=LensCategory.TOOLING,
        summon_when="Reliability, redundancy, failure analysis",
        adds="Critical path demands explicit triage ordering",
        strips="Equal treatment of all components",
        critique="Infrastructure thinking deprioritizes innovation",
    ),

    # /usr/ — Emergent properties
    SystemHouse(
        lens_id="neuroscience",
        name="Neuroscience",
        stratum=Stratum.USR,
        category=LensCategory.STRUCTURE,
        summon_when="Cognitive load, attention allocation, rest",
        adds="7±2 is a hard limit; forgetting is a feature",
        strips="Illusion of unlimited attention",
        critique="Reductive about meaning and purpose",
    ),
    SystemHouse(
        lens_id="ecology",
        name="Ecology",
        stratum=Stratum.USR,
        category=LensCategory.STRUCTURE,
        summon_when="Capacity planning, archival decisions, sprawl",
        adds="Carrying capacity is finite; decomposition is necessary",
        strips="Growth-is-always-good assumptions",
        critique="Ecological metaphors can naturalize what is designed",
    ),
    SystemHouse(
        lens_id="governance",
        name="Governance",
        stratum=Stratum.USR,
        category=LensCategory.AUTHORITY,
        summon_when="Authority questions, rule creation, enforcement",
        adds="Constitutional/statutory/case law hierarchy",
        strips="Informal/implicit authority",
        critique="Governance expands to fill available attention",
    ),
    SystemHouse(
        lens_id="economics",
        name="Economics",
        stratum=Stratum.USR,
        category=LensCategory.AUTHORITY,
        summon_when="Resource allocation, opportunity cost, trade-offs",
        adds="Attention is scarce; allocation has opportunity costs",
        strips="Abundance illusions",
        critique="Economic logic can commodify what shouldn't be commodified",
    ),

    # /net/ — Environment
    SystemHouse(
        lens_id="academia",
        name="Academia",
        stratum=Stratum.NET,
        category=LensCategory.AUTHORITY,
        summon_when="Promotion decisions, quality review, onboarding",
        adds="Tenure track maps to promotion pipeline",
        strips="Informal quality assessment",
        critique="Academic timescales are too slow for a startup",
    ),
    SystemHouse(
        lens_id="belief_systems",
        name="Belief Systems",
        stratum=Stratum.NET,
        category=LensCategory.FOUNDATION,
        summon_when="Doctrine maintenance, principle consistency",
        adds="Sacred texts need amendment processes",
        strips="Casual revision of core principles",
        critique="Sacralization can prevent needed changes",
    ),
    SystemHouse(
        lens_id="cultural_expression",
        name="Cultural Expression",
        stratum=Stratum.NET,
        category=LensCategory.GENERATIVE,
        summon_when="Aesthetic decisions, naming, identity",
        adds="House style requires space for variation",
        strips="Uniformity as a goal",
        critique="Culture can excuse poor engineering",
    ),
    SystemHouse(
        lens_id="sociology",
        name="Sociology",
        stratum=Stratum.NET,
        category=LensCategory.AUTHORITY,
        summon_when="Self-critique, signal vs. function analysis",
        adds="Identifies performative vs. functional governance",
        strips="Taking organizational artifacts at face value",
        critique="Sociology deconstructs but does not construct",
    ),
    SystemHouse(
        lens_id="the_technium",
        name="The Technium",
        stratum=Stratum.NET,
        category=LensCategory.GENERATIVE,
        summon_when="Technology adoption, tool evaluation",
        adds="Infrastructure has autonomous growth tendencies",
        strips="Neutrality assumptions about tools",
        critique="Technium analysis can excuse feature creep",
    ),

    # /dev/ — Entropy source / strange loop
    SystemHouse(
        lens_id="chaos",
        name="Chaos",
        stratum=Stratum.DEV,
        category=LensCategory.GENERATIVE,
        summon_when="Harvesting novelty, protecting creativity",
        adds="The boundary between order and disorder IS the creative engine",
        strips="Control illusions",
        critique="Can justify any disorder as 'productive'",
    ),
    SystemHouse(
        lens_id="the_noosphere",
        name="The Noosphere",
        stratum=Stratum.DEV,
        category=LensCategory.FOUNDATION,
        summon_when="External impact, contribution, publication",
        adds="Internal convergence without external transmission is solipsism",
        strips="Self-referential satisfaction",
        critique="Noospheric ambition can justify anything as 'contributing to collective intelligence'",
    ),
)


# Index for fast lookup
LENS_BY_ID: dict[str, SystemHouse] = {h.lens_id: h for h in LENS_CATALOG}
LENSES_BY_STRATUM: dict[Stratum, list[SystemHouse]] = {}
LENSES_BY_CATEGORY: dict[LensCategory, list[SystemHouse]] = {}

for _h in LENS_CATALOG:
    LENSES_BY_STRATUM.setdefault(_h.stratum, []).append(_h)
    LENSES_BY_CATEGORY.setdefault(_h.category, []).append(_h)


# The strange loop: /dev/ (chaos, entropy) feeds back into /boot/ (formal structure)
STRANGE_LOOP_EDGES: list[tuple[str, str]] = [
    ("the_noosphere", "mathematics"),   # Collective intelligence crystallizes into formal structure
    ("chaos", "information_theory"),    # Raw entropy is the source of all information
]

# Cross-stratum dependency edges (non-strange-loop)
CROSS_STRATUM_EDGES: list[tuple[str, str]] = [
    ("mathematics", "thermodynamics"),
    ("thermodynamics", "chemistry"),
    ("chemistry", "organismal_biology"),
    ("chemistry", "cellular_biology"),
    ("organismal_biology", "neuroscience"),
    ("organismal_biology", "ecology"),
    ("cellular_biology", "ecology"),
    ("infrastructure", "governance"),
    ("neuroscience", "economics"),
    ("ecology", "economics"),
    ("governance", "academia"),
    ("governance", "sociology"),
    ("economics", "the_technium"),
    ("academia", "belief_systems"),
    ("cultural_expression", "chaos"),
    ("the_technium", "the_noosphere"),
    ("sociology", "the_noosphere"),
]


def get_all_edges() -> list[tuple[str, str]]:
    """Return all edges including strange loop and cross-stratum."""
    return STRANGE_LOOP_EDGES + CROSS_STRATUM_EDGES
