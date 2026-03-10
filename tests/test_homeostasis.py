"""Tests for the homeostatic response system."""

from src.homeostasis import (
    CorrectiveAction,
    HomeostasisMonitor,
    ResponseType,
    Severity,
    VitalReading,
    VitalSign,
    VitalStatus,
    create_organvm_vitals,
)


def _make_vital() -> VitalSign:
    """Create a test vital sign."""
    return VitalSign(
        vital_id="test_vital",
        name="Test Vital",
        unit="count",
        normal_low=5.0,
        normal_high=10.0,
        warning_low=3.0,
        warning_high=12.0,
        critical_low=1.0,
        critical_high=15.0,
        responses={
            VitalStatus.WARNING_HIGH: [
                CorrectiveAction(
                    response_type=ResponseType.ALERT,
                    description="Value too high",
                    severity=Severity.WARNING,
                ),
            ],
            VitalStatus.CRITICAL_HIGH: [
                CorrectiveAction(
                    response_type=ResponseType.CIRCUIT_BREAK,
                    description="Value critically high",
                    severity=Severity.CRITICAL,
                ),
            ],
        },
    )


def test_vital_evaluate_normal():
    """Values within normal range should be NORMAL."""
    vital = _make_vital()
    assert vital.evaluate(7.0) == VitalStatus.NORMAL


def test_vital_evaluate_warning_high():
    """Values above normal but below critical should be WARNING_HIGH."""
    vital = _make_vital()
    assert vital.evaluate(12.0) == VitalStatus.WARNING_HIGH


def test_vital_evaluate_critical_high():
    """Values at or above critical should be CRITICAL_HIGH."""
    vital = _make_vital()
    assert vital.evaluate(15.0) == VitalStatus.CRITICAL_HIGH


def test_vital_evaluate_warning_low():
    """Values below normal but above critical should be WARNING_LOW."""
    vital = _make_vital()
    assert vital.evaluate(3.0) == VitalStatus.WARNING_LOW


def test_vital_evaluate_critical_low():
    """Values at or below critical low should be CRITICAL_LOW."""
    vital = _make_vital()
    assert vital.evaluate(1.0) == VitalStatus.CRITICAL_LOW


def test_vital_get_responses():
    """get_responses should return the corrective actions for a status."""
    vital = _make_vital()
    actions = vital.get_responses(VitalStatus.WARNING_HIGH)
    assert len(actions) == 1
    assert actions[0].response_type == ResponseType.ALERT


def test_vital_get_responses_empty():
    """get_responses should return empty list for status with no responses."""
    vital = _make_vital()
    actions = vital.get_responses(VitalStatus.NORMAL)
    assert actions == []


def test_vital_to_dict():
    """to_dict should export vital configuration."""
    vital = _make_vital()
    d = vital.to_dict()
    assert d["vital_id"] == "test_vital"
    assert d["normal_range"] == [5.0, 10.0]


def test_monitor_register_and_measure():
    """Monitor should register vitals and take measurements."""
    monitor = HomeostasisMonitor()
    monitor.register_vital(_make_vital())
    reading = monitor.measure("test_vital", 7.0)
    assert reading.status == VitalStatus.NORMAL
    assert reading.triggered_actions == []


def test_monitor_measure_triggers_actions():
    """Measurements outside normal range should trigger corrective actions."""
    monitor = HomeostasisMonitor()
    monitor.register_vital(_make_vital())
    reading = monitor.measure("test_vital", 13.0)
    assert reading.status == VitalStatus.WARNING_HIGH
    assert len(reading.triggered_actions) == 1
    assert reading.triggered_actions[0].response_type == ResponseType.ALERT


def test_monitor_rejects_duplicate_vital():
    """Registering a duplicate vital ID should raise ValueError."""
    monitor = HomeostasisMonitor()
    monitor.register_vital(_make_vital())
    try:
        monitor.register_vital(_make_vital())
        assert False, "Should have raised ValueError"
    except ValueError:
        pass


def test_monitor_measure_unknown_vital():
    """Measuring an unregistered vital should raise KeyError."""
    monitor = HomeostasisMonitor()
    try:
        monitor.measure("nonexistent", 5.0)
        assert False, "Should have raised KeyError"
    except KeyError:
        pass


def test_monitor_check_all():
    """check_all should measure multiple vitals at once."""
    monitor = HomeostasisMonitor()
    v1 = VitalSign(vital_id="v1", name="V1", unit="x", normal_low=0, normal_high=10)
    v2 = VitalSign(vital_id="v2", name="V2", unit="x", normal_low=0, normal_high=10)
    monitor.register_vital(v1)
    monitor.register_vital(v2)
    readings = monitor.check_all({"v1": 5.0, "v2": 5.0})
    assert len(readings) == 2
    assert all(r.status == VitalStatus.NORMAL for r in readings)


def test_monitor_get_abnormal_readings():
    """get_abnormal_readings should return only non-NORMAL readings."""
    monitor = HomeostasisMonitor()
    monitor.register_vital(_make_vital())
    monitor.measure("test_vital", 7.0)   # normal
    monitor.measure("test_vital", 14.0)  # warning high
    abnormal = monitor.get_abnormal_readings()
    assert len(abnormal) == 1
    assert abnormal[0].value == 14.0


def test_monitor_get_latest_reading():
    """get_latest_reading should return the most recent reading for a vital."""
    monitor = HomeostasisMonitor()
    monitor.register_vital(_make_vital())
    monitor.measure("test_vital", 7.0)
    monitor.measure("test_vital", 8.0)
    latest = monitor.get_latest_reading("test_vital")
    assert latest is not None
    assert latest.value == 8.0


def test_monitor_get_latest_reading_none():
    """get_latest_reading should return None for never-measured vital."""
    monitor = HomeostasisMonitor()
    monitor.register_vital(_make_vital())
    assert monitor.get_latest_reading("test_vital") is None


def test_monitor_system_status():
    """system_status should summarize overall system health."""
    monitor = HomeostasisMonitor()
    monitor.register_vital(_make_vital())
    monitor.measure("test_vital", 7.0)
    status = monitor.system_status()
    assert status["overall"] == "healthy"
    assert "test_vital" in status["vitals"]


def test_monitor_system_status_degraded():
    """system_status should report degraded when any vital is in warning."""
    monitor = HomeostasisMonitor()
    monitor.register_vital(_make_vital())
    monitor.measure("test_vital", 13.0)
    status = monitor.system_status()
    assert status["overall"] == "degraded"


def test_monitor_system_status_critical():
    """system_status should report critical when any vital is critical."""
    monitor = HomeostasisMonitor()
    monitor.register_vital(_make_vital())
    monitor.measure("test_vital", 16.0)
    status = monitor.system_status()
    assert status["overall"] == "critical"


def test_monitor_vital_ids():
    """vital_ids should list all registered vital signs."""
    monitor = HomeostasisMonitor()
    monitor.register_vital(_make_vital())
    assert monitor.vital_ids == ["test_vital"]


def test_vital_reading_to_dict():
    """VitalReading.to_dict should include all fields."""
    reading = VitalReading(
        vital_id="test", value=7.0, status=VitalStatus.NORMAL,
    )
    d = reading.to_dict()
    assert d["vital_id"] == "test"
    assert d["value"] == 7.0
    assert d["status"] == "normal"


def test_corrective_action_to_dict():
    """CorrectiveAction.to_dict should export all fields."""
    action = CorrectiveAction(
        response_type=ResponseType.ALERT,
        description="test",
        severity=Severity.WARNING,
        target="repo-x",
    )
    d = action.to_dict()
    assert d["response_type"] == "alert"
    assert d["target"] == "repo-x"


def test_create_organvm_vitals():
    """create_organvm_vitals should return the 7 core vital signs."""
    vitals = create_organvm_vitals()
    assert len(vitals) == 7
    ids = {v.vital_id for v in vitals}
    assert "active_repo_count" in ids
    assert "stale_repo_ratio" in ids
    assert "governance_to_product_ratio" in ids
    assert "infra_wip_count" in ids
    assert "test_coverage_min" in ids
    assert "omega_velocity" in ids
    assert "entropy_rate" in ids


def test_organvm_vitals_have_responses():
    """All organvm vitals should have at least one response defined."""
    vitals = create_organvm_vitals()
    for v in vitals:
        assert len(v.responses) > 0, f"Vital '{v.vital_id}' has no responses"


def test_monitor_history_limit():
    """Monitor should trim history to max_history."""
    monitor = HomeostasisMonitor()
    monitor._max_history = 5
    monitor.register_vital(_make_vital())
    for i in range(10):
        monitor.measure("test_vital", float(i))
    assert len(monitor._readings) == 5
