"""Tests for the dynamic lens assembly protocol."""

from src.assembly import (
    AssemblyResult,
    ConflictResolution,
    LensCategory,
    assemble,
    detect_conflicts,
    identify_category,
    identify_stratum,
    interrogate,
    select_lenses,
)
from src.hierarchy import LENS_BY_ID, Stratum


def test_identify_category_tooling():
    """Tooling keywords should map to TOOLING."""
    assert identify_category("fix the CI pipeline build failure") == LensCategory.TOOLING


def test_identify_category_structure():
    """Architecture keywords should map to STRUCTURE."""
    assert identify_category("redesign the module dependency graph") == LensCategory.STRUCTURE


def test_identify_category_authority():
    """Governance keywords should map to AUTHORITY."""
    assert identify_category("set promotion policy for new repos") == LensCategory.AUTHORITY


def test_identify_category_foundation():
    """Philosophy keywords should map to FOUNDATION."""
    assert identify_category("clarify the ontological identity of the system") == LensCategory.FOUNDATION


def test_identify_category_generative():
    """Creative keywords should map to GENERATIVE."""
    assert identify_category("generate new art pieces and explore aesthetics") == LensCategory.GENERATIVE


def test_identify_category_default():
    """Unknown keywords should default to STRUCTURE."""
    assert identify_category("zzzzz nothing matches here") == LensCategory.STRUCTURE


def test_identify_stratum_mapping():
    """Each category should map to a specific stratum."""
    assert identify_stratum(LensCategory.TOOLING) == Stratum.SYS
    assert identify_stratum(LensCategory.STRUCTURE) == Stratum.BIN
    assert identify_stratum(LensCategory.AUTHORITY) == Stratum.USR
    assert identify_stratum(LensCategory.FOUNDATION) == Stratum.BOOT
    assert identify_stratum(LensCategory.GENERATIVE) == Stratum.DEV


def test_select_lenses_returns_2_to_3():
    """select_lenses should return 2-3 lenses."""
    lenses = select_lenses(LensCategory.STRUCTURE)
    assert 2 <= len(lenses) <= 3


def test_select_lenses_hard_cap_at_3():
    """Even if max_lenses > 3, should never exceed 3."""
    lenses = select_lenses(LensCategory.STRUCTURE, max_lenses=10)
    assert len(lenses) <= 3


def test_select_lenses_includes_critic():
    """When require_critic=True, at least one lens should be from a different category."""
    lenses = select_lenses(LensCategory.TOOLING, require_critic=True)
    categories = {l.category for l in lenses}
    assert len(categories) > 1, "Should include a critic from a different category"


def test_select_lenses_respects_exclude():
    """Excluded lens IDs should not appear in results."""
    lenses = select_lenses(LensCategory.STRUCTURE, exclude=["mathematics", "organismal_biology"])
    ids = {l.lens_id for l in lenses}
    assert "mathematics" not in ids
    assert "organismal_biology" not in ids


def test_interrogate_produces_insight():
    """interrogate should produce a structured LensInsight."""
    lens = LENS_BY_ID["ecology"]
    insight = interrogate(lens, "should we archive old repos?")
    assert insight.lens_id == "ecology"
    assert insight.adds == lens.adds
    assert insight.strips == lens.strips
    assert insight.critique == lens.critique


def test_detect_conflicts_reduce_vs_preserve():
    """Should detect the reduce-vs-preserve conflict pattern."""
    neurosci = interrogate(LENS_BY_ID["neuroscience"], "test")
    ecology = interrogate(LENS_BY_ID["ecology"], "test")
    conflicts = detect_conflicts([neurosci, ecology])
    # Neuroscience is reduction, ecology is diversity — but both are in the same set here
    # Let's use a clear pair:
    neurosci2 = interrogate(LENS_BY_ID["neuroscience"], "test")
    cultural = interrogate(LENS_BY_ID["cultural_expression"], "test")
    conflicts = detect_conflicts([neurosci2, cultural])
    assert len(conflicts) >= 1
    assert conflicts[0].resolution == ConflictResolution.DYNAMIC_SCOPING


def test_detect_conflicts_governance_vs_shipping():
    """Should detect the governance-vs-shipping conflict pattern."""
    gov = interrogate(LENS_BY_ID["governance"], "test")
    econ = interrogate(LENS_BY_ID["economics"], "test")
    conflicts = detect_conflicts([gov, econ])
    assert len(conflicts) >= 1
    assert conflicts[0].resolution == ConflictResolution.PHASE_DIAGNOSIS


def test_detect_conflicts_internal_vs_external():
    """Should detect the internal-vs-external conflict pattern."""
    belief = interrogate(LENS_BY_ID["belief_systems"], "test")
    noosphere = interrogate(LENS_BY_ID["the_noosphere"], "test")
    conflicts = detect_conflicts([belief, noosphere])
    assert len(conflicts) >= 1
    assert conflicts[0].resolution == ConflictResolution.STRATUM_SEPARATION


def test_detect_conflicts_no_false_positives():
    """Non-conflicting lenses should produce no conflicts."""
    math = interrogate(LENS_BY_ID["mathematics"], "test")
    thermo = interrogate(LENS_BY_ID["thermodynamics"], "test")
    conflicts = detect_conflicts([math, thermo])
    assert len(conflicts) == 0


def test_assemble_full_protocol():
    """assemble should execute the full 5-step protocol."""
    result = assemble("redesign the system architecture for better health monitoring")
    assert isinstance(result, AssemblyResult)
    assert result.identified_category == LensCategory.STRUCTURE
    assert result.identified_stratum == Stratum.BIN
    assert 2 <= len(result.summoned_lenses) <= 3
    assert len(result.insights) == len(result.summoned_lenses)
    assert result.synthesis != ""
    assert result.released is False


def test_assemble_release():
    """After release, the assembly should be marked released."""
    result = assemble("test task")
    result.release()
    assert result.released is True


def test_assemble_to_dict():
    """to_dict should export all assembly data."""
    result = assemble("deploy new product feature")
    d = result.to_dict()
    assert "task" in d
    assert "stratum" in d
    assert "lenses" in d
    assert "insights" in d
    assert "conflicts" in d
    assert "synthesis" in d
    assert "released" in d


def test_assemble_with_exclude():
    """assemble should respect exclude list."""
    result = assemble("deploy code", exclude=["chemistry", "thermodynamics", "infrastructure"])
    ids = {l.lens_id for l in result.summoned_lenses}
    assert "chemistry" not in ids
    assert "thermodynamics" not in ids
    assert "infrastructure" not in ids
