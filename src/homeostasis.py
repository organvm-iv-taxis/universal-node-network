"""Homeostatic Response System — vital signs with automatic corrective actions.

Convergence 2 from the synthesis: "Monitoring without automatic correction
is a thermometer without a thermostat." This module provides the autonomic
nervous system that the living-systems document demanded.

Each vital sign defines:
- A measurement function (how to observe the value)
- A normal range (homeostatic set point)
- Corrective responses when the value exits its range
- Severity levels (warning vs. critical)

The system acts, not just observes.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Protocol


class VitalStatus(Enum):
    """Status of a vital sign relative to its normal range."""

    NORMAL = "normal"
    WARNING_LOW = "warning_low"
    WARNING_HIGH = "warning_high"
    CRITICAL_LOW = "critical_low"
    CRITICAL_HIGH = "critical_high"


class Severity(Enum):
    """Severity of a homeostatic response."""

    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"


class ResponseType(Enum):
    """Types of automatic corrective responses."""

    DIM_CONTEXT = "dim_context"             # Remove from active context files
    AUTO_ARCHIVE_SUGGEST = "auto_archive"   # Suggest archival
    GENERATE_TASK = "generate_task"         # Create a corrective task
    REBALANCE = "rebalance"                 # Shift resource allocation
    ALERT = "alert"                         # Notify the conductor
    CIRCUIT_BREAK = "circuit_break"         # Halt operations on component


class VitalMeasurer(Protocol):
    """Protocol for functions that measure vital signs."""

    def __call__(self, context: dict[str, Any]) -> float: ...


@dataclass
class CorrectiveAction:
    """An automatic response triggered when a vital exits its range."""

    response_type: ResponseType
    description: str
    severity: Severity
    target: str = ""     # What to apply the action to (repo, organ, etc.)
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Export as dictionary."""
        return {
            "response_type": self.response_type.value,
            "description": self.description,
            "severity": self.severity.value,
            "target": self.target,
        }


@dataclass
class VitalSign:
    """A measurable indicator of system health with homeostatic response.

    Defines normal range, warning thresholds, and corrective actions.
    """

    vital_id: str
    name: str
    unit: str
    normal_low: float
    normal_high: float
    warning_low: float | None = None   # Below this = WARNING_LOW
    warning_high: float | None = None  # Above this = WARNING_HIGH
    critical_low: float | None = None  # Below this = CRITICAL_LOW
    critical_high: float | None = None  # Above this = CRITICAL_HIGH

    # Corrective actions for each status
    responses: dict[VitalStatus, list[CorrectiveAction]] = field(default_factory=dict)

    def evaluate(self, value: float) -> VitalStatus:
        """Evaluate a measured value against this vital sign's thresholds.

        Args:
            value: The measured value.

        Returns:
            The VitalStatus for this measurement.
        """
        if self.critical_low is not None and value <= self.critical_low:
            return VitalStatus.CRITICAL_LOW
        if self.critical_high is not None and value >= self.critical_high:
            return VitalStatus.CRITICAL_HIGH
        if self.warning_low is not None and value <= self.warning_low:
            return VitalStatus.WARNING_LOW
        if self.warning_high is not None and value >= self.warning_high:
            return VitalStatus.WARNING_HIGH
        if self.normal_low <= value <= self.normal_high:
            return VitalStatus.NORMAL
        # Between warning and normal boundaries
        if value < self.normal_low:
            return VitalStatus.WARNING_LOW
        return VitalStatus.WARNING_HIGH

    def get_responses(self, status: VitalStatus) -> list[CorrectiveAction]:
        """Get corrective actions for a given status.

        Args:
            status: The current VitalStatus.

        Returns:
            List of corrective actions to execute.
        """
        return self.responses.get(status, [])

    def to_dict(self) -> dict[str, Any]:
        """Export as dictionary."""
        return {
            "vital_id": self.vital_id,
            "name": self.name,
            "unit": self.unit,
            "normal_range": [self.normal_low, self.normal_high],
            "warning_range": [self.warning_low, self.warning_high],
            "critical_range": [self.critical_low, self.critical_high],
        }


@dataclass
class VitalReading:
    """A single measurement of a vital sign at a point in time."""

    vital_id: str
    value: float
    status: VitalStatus
    timestamp: datetime = field(default_factory=datetime.now)
    context: dict[str, Any] = field(default_factory=dict)
    triggered_actions: list[CorrectiveAction] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        """Export as dictionary."""
        return {
            "vital_id": self.vital_id,
            "value": self.value,
            "status": self.status.value,
            "timestamp": self.timestamp.isoformat(),
            "actions": [a.to_dict() for a in self.triggered_actions],
        }


class HomeostasisMonitor:
    """The autonomic nervous system — monitors vitals and triggers responses.

    Maintains a set of vital signs, takes periodic readings, and
    generates corrective actions when values exit normal ranges.
    """

    def __init__(self) -> None:
        self._vitals: dict[str, VitalSign] = {}
        self._readings: list[VitalReading] = []
        self._max_history: int = 500

    def register_vital(self, vital: VitalSign) -> None:
        """Register a new vital sign for monitoring.

        Args:
            vital: The VitalSign to monitor.

        Raises:
            ValueError: If a vital with this ID already exists.
        """
        if vital.vital_id in self._vitals:
            raise ValueError(f"Vital '{vital.vital_id}' already registered")
        self._vitals[vital.vital_id] = vital

    def measure(self, vital_id: str, value: float,
                context: dict[str, Any] | None = None) -> VitalReading:
        """Take a reading for a vital sign and determine response.

        Args:
            vital_id: ID of the vital sign to measure.
            value: The measured value.
            context: Optional context dict (e.g., which repo, organ).

        Returns:
            VitalReading with status and triggered actions.

        Raises:
            KeyError: If vital_id is not registered.
        """
        vital = self._vitals[vital_id]
        status = vital.evaluate(value)
        actions = vital.get_responses(status)

        reading = VitalReading(
            vital_id=vital_id,
            value=value,
            status=status,
            context=context or {},
            triggered_actions=actions,
        )

        self._readings.append(reading)
        if len(self._readings) > self._max_history:
            self._readings = self._readings[-self._max_history:]

        return reading

    def check_all(self, measurements: dict[str, float],
                  context: dict[str, Any] | None = None) -> list[VitalReading]:
        """Take readings for multiple vitals at once.

        Args:
            measurements: Dict mapping vital_id to measured value.
            context: Shared context for all readings.

        Returns:
            List of VitalReadings, one per measurement.
        """
        readings = []
        for vital_id, value in measurements.items():
            if vital_id in self._vitals:
                readings.append(self.measure(vital_id, value, context))
        return readings

    def get_abnormal_readings(self) -> list[VitalReading]:
        """Get all readings with non-NORMAL status from history.

        Returns:
            List of abnormal VitalReadings.
        """
        return [r for r in self._readings if r.status != VitalStatus.NORMAL]

    def get_latest_reading(self, vital_id: str) -> VitalReading | None:
        """Get the most recent reading for a vital sign.

        Args:
            vital_id: The vital sign ID.

        Returns:
            Most recent VitalReading, or None if never measured.
        """
        for reading in reversed(self._readings):
            if reading.vital_id == vital_id:
                return reading
        return None

    def system_status(self) -> dict[str, Any]:
        """Get overall system health status.

        Returns:
            Dict with per-vital latest status and overall health.
        """
        latest: dict[str, VitalReading] = {}
        for reading in self._readings:
            latest[reading.vital_id] = reading

        all_normal = all(r.status == VitalStatus.NORMAL for r in latest.values())
        any_critical = any(
            r.status in (VitalStatus.CRITICAL_LOW, VitalStatus.CRITICAL_HIGH)
            for r in latest.values()
        )

        return {
            "overall": "critical" if any_critical else ("healthy" if all_normal else "degraded"),
            "vitals": {vid: r.to_dict() for vid, r in latest.items()},
            "total_readings": len(self._readings),
            "abnormal_count": len(self.get_abnormal_readings()),
        }

    @property
    def vital_ids(self) -> list[str]:
        """List all registered vital sign IDs."""
        return list(self._vitals.keys())


# ---------------------------------------------------------------------------
# Pre-defined vital signs for the ORGANVM system
# ---------------------------------------------------------------------------

def create_organvm_vitals() -> list[VitalSign]:
    """Create the standard vital signs for ORGANVM health monitoring.

    Returns:
        List of VitalSign objects for the 7 core system vitals.
    """
    return [
        VitalSign(
            vital_id="active_repo_count",
            name="Active Repository Count",
            unit="repos",
            normal_low=5.0,
            normal_high=12.0,      # 7±2 + buffer
            warning_low=3.0,
            warning_high=15.0,
            critical_low=1.0,
            critical_high=20.0,
            responses={
                VitalStatus.WARNING_HIGH: [
                    CorrectiveAction(
                        response_type=ResponseType.DIM_CONTEXT,
                        description="Dim least-active repos from context files",
                        severity=Severity.WARNING,
                    ),
                ],
                VitalStatus.CRITICAL_HIGH: [
                    CorrectiveAction(
                        response_type=ResponseType.DIM_CONTEXT,
                        description="Aggressively dim repos — exceeding cognitive ceiling",
                        severity=Severity.CRITICAL,
                    ),
                    CorrectiveAction(
                        response_type=ResponseType.AUTO_ARCHIVE_SUGGEST,
                        description="Suggest archival for repos with no activity in 30+ days",
                        severity=Severity.CRITICAL,
                    ),
                ],
                VitalStatus.CRITICAL_LOW: [
                    CorrectiveAction(
                        response_type=ResponseType.ALERT,
                        description="System has too few active repos — check for blockage",
                        severity=Severity.CRITICAL,
                    ),
                ],
            },
        ),
        VitalSign(
            vital_id="stale_repo_ratio",
            name="Stale Repository Ratio",
            unit="ratio",
            normal_low=0.0,
            normal_high=0.3,
            warning_high=0.5,
            critical_high=0.7,
            responses={
                VitalStatus.WARNING_HIGH: [
                    CorrectiveAction(
                        response_type=ResponseType.GENERATE_TASK,
                        description="Generate tasks to triage stale repos: archive or reactivate",
                        severity=Severity.WARNING,
                    ),
                ],
                VitalStatus.CRITICAL_HIGH: [
                    CorrectiveAction(
                        response_type=ResponseType.CIRCUIT_BREAK,
                        description="Halt new repo creation until stale ratio drops below 50%",
                        severity=Severity.CRITICAL,
                    ),
                ],
            },
        ),
        VitalSign(
            vital_id="governance_to_product_ratio",
            name="Governance-to-Product Session Ratio",
            unit="ratio",
            normal_low=0.1,
            normal_high=0.4,      # 10-40% governance is healthy
            warning_high=0.6,
            critical_high=0.8,
            responses={
                VitalStatus.WARNING_HIGH: [
                    CorrectiveAction(
                        response_type=ResponseType.REBALANCE,
                        description="Shift next 3 sessions to product work",
                        severity=Severity.WARNING,
                    ),
                ],
                VitalStatus.CRITICAL_HIGH: [
                    CorrectiveAction(
                        response_type=ResponseType.ALERT,
                        description="System is producing itself, not products (sociology warning)",
                        severity=Severity.CRITICAL,
                    ),
                    CorrectiveAction(
                        response_type=ResponseType.REBALANCE,
                        description="Hard redirect: next 5 sessions must be product-facing",
                        severity=Severity.CRITICAL,
                    ),
                ],
            },
        ),
        VitalSign(
            vital_id="infra_wip_count",
            name="Infrastructure Work-in-Progress Count",
            unit="tasks",
            normal_low=0.0,
            normal_high=3.0,
            warning_high=5.0,
            critical_high=7.0,
            responses={
                VitalStatus.WARNING_HIGH: [
                    CorrectiveAction(
                        response_type=ResponseType.ALERT,
                        description="Infrastructure WIP approaching limit — finish before starting new",
                        severity=Severity.WARNING,
                    ),
                ],
                VitalStatus.CRITICAL_HIGH: [
                    CorrectiveAction(
                        response_type=ResponseType.CIRCUIT_BREAK,
                        description="Infrastructure WIP limit exceeded — no new infra until count drops",
                        severity=Severity.CRITICAL,
                    ),
                ],
            },
        ),
        VitalSign(
            vital_id="test_coverage_min",
            name="Minimum Test Coverage (Keystones)",
            unit="percent",
            normal_low=70.0,
            normal_high=100.0,
            warning_low=50.0,
            critical_low=30.0,
            responses={
                VitalStatus.WARNING_LOW: [
                    CorrectiveAction(
                        response_type=ResponseType.GENERATE_TASK,
                        description="Generate test-writing task for under-covered keystone repo",
                        severity=Severity.WARNING,
                    ),
                ],
                VitalStatus.CRITICAL_LOW: [
                    CorrectiveAction(
                        response_type=ResponseType.CIRCUIT_BREAK,
                        description="Block promotion for keystone repos below 30% coverage",
                        severity=Severity.CRITICAL,
                    ),
                ],
            },
        ),
        VitalSign(
            vital_id="omega_velocity",
            name="Omega Scorecard Velocity",
            unit="criteria/month",
            normal_low=0.5,
            normal_high=3.0,
            warning_low=0.1,
            critical_low=0.0,
            responses={
                VitalStatus.WARNING_LOW: [
                    CorrectiveAction(
                        response_type=ResponseType.REBALANCE,
                        description="Omega stalling — review blocking criteria and redirect sessions",
                        severity=Severity.WARNING,
                    ),
                ],
                VitalStatus.CRITICAL_LOW: [
                    CorrectiveAction(
                        response_type=ResponseType.ALERT,
                        description="Omega scorecard frozen — fundamental blocker exists",
                        severity=Severity.CRITICAL,
                    ),
                ],
            },
        ),
        VitalSign(
            vital_id="entropy_rate",
            name="System Entropy Rate",
            unit="events/day",
            normal_low=1.0,
            normal_high=10.0,
            warning_low=0.1,
            warning_high=20.0,
            critical_high=50.0,
            responses={
                VitalStatus.WARNING_LOW: [
                    CorrectiveAction(
                        response_type=ResponseType.ALERT,
                        description="System is stagnant — no commits, no activity",
                        severity=Severity.WARNING,
                    ),
                ],
                VitalStatus.WARNING_HIGH: [
                    CorrectiveAction(
                        response_type=ResponseType.ALERT,
                        description="Entropy rising — too many changes without consolidation",
                        severity=Severity.WARNING,
                    ),
                ],
                VitalStatus.CRITICAL_HIGH: [
                    CorrectiveAction(
                        response_type=ResponseType.CIRCUIT_BREAK,
                        description="System in chaos — pause and consolidate before continuing",
                        severity=Severity.CRITICAL,
                    ),
                ],
            },
        ),
    ]
