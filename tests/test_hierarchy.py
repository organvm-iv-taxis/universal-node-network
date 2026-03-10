"""Tests for the hierarchy module — the 21 organizational lenses."""

from src.hierarchy import (
    CROSS_STRATUM_EDGES,
    LENS_BY_ID,
    LENS_CATALOG,
    LENSES_BY_CATEGORY,
    LENSES_BY_STRATUM,
    STRANGE_LOOP_EDGES,
    LensCategory,
    Stratum,
    SystemHouse,
    get_all_edges,
)


def test_catalog_has_21_lenses():
    """The catalog should contain exactly 21 lenses from the synthesis."""
    assert len(LENS_CATALOG) == 21


def test_all_strata_populated():
    """Every stratum should have at least one lens."""
    for stratum in Stratum:
        lenses = LENSES_BY_STRATUM.get(stratum, [])
        assert len(lenses) >= 1, f"Stratum {stratum.value} has no lenses"


def test_all_categories_populated():
    """Every category should have at least one lens."""
    for cat in LensCategory:
        lenses = LENSES_BY_CATEGORY.get(cat, [])
        assert len(lenses) >= 1, f"Category {cat.value} has no lenses"


def test_lens_ids_unique():
    """Every lens ID should be unique."""
    ids = [h.lens_id for h in LENS_CATALOG]
    assert len(ids) == len(set(ids))


def test_lens_by_id_index():
    """LENS_BY_ID should map every lens correctly."""
    assert len(LENS_BY_ID) == len(LENS_CATALOG)
    for h in LENS_CATALOG:
        assert LENS_BY_ID[h.lens_id] is h


def test_strange_loop_edges_connect_dev_to_boot():
    """Strange loop edges should connect /dev/ lenses to /boot/ lenses."""
    for src, tgt in STRANGE_LOOP_EDGES:
        src_house = LENS_BY_ID[src]
        tgt_house = LENS_BY_ID[tgt]
        assert src_house.stratum == Stratum.DEV
        assert tgt_house.stratum == Stratum.BOOT


def test_cross_stratum_edges_valid():
    """All cross-stratum edges should reference valid lens IDs."""
    for src, tgt in CROSS_STRATUM_EDGES:
        assert src in LENS_BY_ID, f"Invalid source: {src}"
        assert tgt in LENS_BY_ID, f"Invalid target: {tgt}"


def test_get_all_edges_combines():
    """get_all_edges should return both strange loop and cross-stratum."""
    all_edges = get_all_edges()
    assert len(all_edges) == len(STRANGE_LOOP_EDGES) + len(CROSS_STRATUM_EDGES)


def test_system_house_frozen():
    """SystemHouse should be immutable (frozen dataclass)."""
    house = LENS_CATALOG[0]
    try:
        house.name = "changed"
        assert False, "Should have raised FrozenInstanceError"
    except AttributeError:
        pass


def test_system_house_to_dict():
    """to_dict should export all key fields."""
    house = LENS_BY_ID["mathematics"]
    d = house.to_dict()
    assert d["lens_id"] == "mathematics"
    assert d["stratum"] == "/boot/"
    assert d["category"] == "structure"
    assert "adds" in d
    assert "strips" in d
    assert "critique" in d


def test_matches_task():
    """matches_task should return True for matching category."""
    house = LENS_BY_ID["mathematics"]
    assert house.matches_task(LensCategory.STRUCTURE) is True
    assert house.matches_task(LensCategory.GENERATIVE) is False


def test_strata_values_are_unix_paths():
    """Strata values should follow the /path/ convention."""
    for s in Stratum:
        assert s.value.startswith("/")
        assert s.value.endswith("/")
