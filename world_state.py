"""
INTELLECT MEDIA — WORLD STATE
Layer 06 of the canonical 40-layer Project Brain.

Project Identity     = WHO the project is
Project DNA          = WHY the project exists
Architecture         = WHAT structure is allowed
Authority            = WHO MAY DECIDE / ACT / OVERRIDE
Invariant / Law      = WHAT MUST NEVER BE BROKEN
World State          = WHAT IS TRUE RIGHT NOW

World State is the canonical reality-observation layer.

Its purpose is to:
- represent the project's current known reality,
- separate facts from assumptions and unknowns,
- preserve evidence provenance,
- track freshness and confidence,
- detect contradictory observations,
- prevent stale information from silently becoming current truth,
- produce deterministic state fingerprints,
- support future context compilation, planning, verification,
  autonomous execution, recovery, and decision-making.

IMPORTANT:
World State does not decide what the project SHOULD do.
It records what is currently believed to be TRUE,
WHY it is believed, HOW reliable it is, and WHEN it was observed.

This module intentionally remains dependency-light and deterministic.
No external service is contacted by this file.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum
from hashlib import sha256
import json
from typing import Final, Iterable, Mapping


# ============================================================================
# CANONICAL PROJECT CONSTANTS
# ============================================================================

PROJECT_ID: Final[str] = "intellect-media"
CANONICAL_NAME: Final[str] = "Intellect Media"

WORLD_STATE_VERSION: Final[str] = "1.0.0"
BRAIN_ARCHITECTURE_VERSION: Final[str] = "40.0.0"

LAYER_NUMBER: Final[int] = 6
LAYER_NAME: Final[str] = "World State"

SCHEMA_VERSION: Final[int] = 1


# ============================================================================
# ENUMERATIONS
# ============================================================================

class StateValueType(str, Enum):
    """Canonical semantic type of an observed state value."""

    BOOLEAN = "boolean"
    INTEGER = "integer"
    NUMBER = "number"
    STRING = "string"
    OBJECT = "object"
    ARRAY = "array"
    NULL = "null"


class EvidenceQuality(str, Enum):
    """Quality of evidence supporting a world-state observation."""

    UNKNOWN = "unknown"
    WEAK = "weak"
    MODERATE = "moderate"
    STRONG = "strong"
    VERIFIED = "verified"


EVIDENCE_RANK: Final[dict[EvidenceQuality, int]] = {
    EvidenceQuality.UNKNOWN: 0,
    EvidenceQuality.WEAK: 1,
    EvidenceQuality.MODERATE: 2,
    EvidenceQuality.STRONG: 3,
    EvidenceQuality.VERIFIED: 4,
}


class StateStatus(str, Enum):
    """Lifecycle status of a world-state observation."""

    UNKNOWN = "unknown"
    ACTIVE = "active"
    STALE = "stale"
    EXPIRED = "expired"
    SUPERSEDED = "superseded"
    CONFLICTED = "conflicted"


class StateSourceType(str, Enum):
    """Origin category of state evidence."""

    HUMAN = "human"
    REPOSITORY = "repository"
    GIT = "git"
    TOOL = "tool"
    EXTERNAL_SOURCE = "external_source"
    SYSTEM = "system"
    AGENT = "agent"
    MODEL = "model"


class StateCriticality(str, Enum):
    """Importance of a state fact to system integrity."""

    LOW = "low"
    MODERATE = "moderate"
    HIGH = "high"
    CRITICAL = "critical"


CRITICALITY_RANK: Final[dict[StateCriticality, int]] = {
    StateCriticality.LOW: 0,
    StateCriticality.MODERATE: 1,
    StateCriticality.HIGH: 2,
    StateCriticality.CRITICAL: 3,
}


class StateTruth(str, Enum):
    """
    Epistemic status of an observation.

    TRUE means sufficiently supported for active use.
    ASSUMED means intentionally provisional.
    UNKNOWN means insufficient evidence.
    FALSE means evidence supports the opposite.
    """

    TRUE = "true"
    FALSE = "false"
    ASSUMED = "assumed"
    UNKNOWN = "unknown"


# ============================================================================
# CORE DATA STRUCTURES
# ============================================================================

@dataclass(frozen=True, slots=True)
class StateSource:
    """
    Provenance of a world-state observation.

    source_id should identify the concrete source when possible:
    commit SHA, tool execution ID, file path, human actor, etc.
    """

    source_type: StateSourceType
    source_id: str
    observed_at: str
    evidence_quality: EvidenceQuality = EvidenceQuality.UNKNOWN
    locator: str = ""


@dataclass(frozen=True, slots=True)
class StateObservation:
    """
    One canonical observation about the current world.

    key:
        Stable semantic identifier such as:
        "repository.main.branch"

    value:
        JSON-compatible observed value.

    observed_at:
        UTC ISO-8601 timestamp.

    expires_at:
        Optional UTC ISO-8601 timestamp after which the observation
        must not be treated as fresh truth.

    truth:
        Current epistemic interpretation.

    confidence:
        Numeric confidence between 0.0 and 1.0.

    criticality:
        Importance of this fact.

    source:
        Evidence provenance.

    supersedes:
        Optional observation ID previously replaced by this observation.
    """

    observation_id: str
    key: str
    value: object
    value_type: StateValueType

    observed_at: str
    expires_at: str | None

    truth: StateTruth
    confidence: float
    criticality: StateCriticality

    source: StateSource

    status: StateStatus = StateStatus.ACTIVE
    supersedes: str | None = None

    note: str = ""


@dataclass(frozen=True, slots=True)
class StateConflict:
    """Represents materially inconsistent observations for one state key."""

    key: str
    observation_ids: tuple[str, ...]
    reason: str
    critical: bool


@dataclass(frozen=True, slots=True)
class WorldStateEvaluation:
    """Deterministic evaluation of a World State snapshot."""

    valid: bool
    usable: bool
    stale_observation_count: int
    expired_observation_count: int
    conflicted_key_count: int
    critical_conflict_count: int
    errors: tuple[str, ...]
    warnings: tuple[str, ...]
    fingerprint: str


# ============================================================================
# VALUE-TYPE UTILITIES
# ============================================================================

def infer_value_type(value: object) -> StateValueType:
    """Infer the canonical StateValueType for a JSON-compatible value."""

    if value is None:
        return StateValueType.NULL

    if isinstance(value, bool):
        return StateValueType.BOOLEAN

    if isinstance(value, int) and not isinstance(value, bool):
        return StateValueType.INTEGER

    if isinstance(value, float):
        return StateValueType.NUMBER

    if isinstance(value, str):
        return StateValueType.STRING

    if isinstance(value, dict):
        return StateValueType.OBJECT

    if isinstance(value, (list, tuple)):
        return StateValueType.ARRAY

    raise TypeError(
        "World State values must be JSON-compatible. "
        f"Unsupported type: {type(value).__name__}"
    )


def _ensure_utc_iso(timestamp: str, field_name: str) -> datetime:
    """
    Parse a timestamp and normalize the semantic expectation to UTC.

    Accepts:
        2026-09-14T10:30:00+00:00
        2026-09-14T16:00:00+05:30
        2026-09-14T10:30:00Z
    """

    if not isinstance(timestamp, str) or not timestamp.strip():
        raise ValueError(f"{field_name} must be a non-empty ISO-8601 string.")

    normalized = timestamp.strip()

    if normalized.endswith("Z"):
        normalized = normalized[:-1] + "+00:00"

    try:
        parsed = datetime.fromisoformat(normalized)
    except ValueError as exc:
        raise ValueError(
            f"{field_name} is not a valid ISO-8601 timestamp: {timestamp!r}"
        ) from exc

    if parsed.tzinfo is None:
        raise ValueError(
            f"{field_name} must contain explicit timezone information."
        )

    return parsed.astimezone(timezone.utc)


def now_utc_iso() -> str:
    """Return the current UTC timestamp in deterministic ISO-8601 form."""

    return (
        datetime.now(timezone.utc)
        .replace(microsecond=0)
        .isoformat()
        .replace("+00:00", "Z")
    )


def _safe_json_value(value: object) -> object:
    """Return a normalized JSON-compatible representation."""

    if isinstance(value, tuple):
        return [_safe_json_value(item) for item in value]

    if isinstance(value, list):
        return [_safe_json_value(item) for item in value]

    if isinstance(value, dict):
        return {
            str(key): _safe_json_value(item)
            for key, item in sorted(value.items(), key=lambda item: str(item[0]))
        }

    if value is None or isinstance(value, (bool, int, float, str)):
        return value

    raise TypeError(
        "Non-JSON-compatible state value encountered: "
        f"{type(value).__name__}"
    )


# ============================================================================
# OBSERVATION VALIDATION
# ============================================================================

def validate_observation(
    observation: StateObservation,
    *,
    reference_time: str | None = None,
) -> tuple[str, ...]:
    """
    Validate a single observation.

    Returns deterministic error strings.
    """

    errors: list[str] = []

    if not observation.observation_id.strip():
        errors.append("Observation ID cannot be empty.")

    if not observation.key.strip():
        errors.append("Observation key cannot be empty.")

    try:
        inferred = infer_value_type(observation.value)
        if inferred != observation.value_type:
            errors.append(
                f"{observation.observation_id}: value_type mismatch "
                f"(declared={observation.value_type.value}, "
                f"inferred={inferred.value})."
            )
    except TypeError as exc:
        errors.append(
            f"{observation.observation_id}: {exc}"
        )

    try:
        observed_at = _ensure_utc_iso(
            observation.observed_at,
            "observed_at",
        )
    except ValueError as exc:
        errors.append(str(exc))
        observed_at = None

    expires_at = None

    if observation.expires_at is not None:
        try:
            expires_at = _ensure_utc_iso(
                observation.expires_at,
                "expires_at",
            )
        except ValueError as exc:
            errors.append(str(exc))

    if observed_at is not None and expires_at is not None:
        if expires_at <= observed_at:
            errors.append(
                f"{observation.observation_id}: expires_at must be after "
                "observed_at."
            )

    if not 0.0 <= observation.confidence <= 1.0:
        errors.append(
            f"{observation.observation_id}: confidence must be "
            "between 0.0 and 1.0."
        )

    if not observation.source.source_id.strip():
        errors.append(
            f"{observation.observation_id}: source_id cannot be empty."
        )

    if not observation.source.observed_at.strip():
        errors.append(
            f"{observation.observation_id}: source observed_at cannot "
            "be empty."
        )

    if observation.supersedes == observation.observation_id:
        errors.append(
            f"{observation.observation_id}: observation cannot supersede "
            "itself."
        )

    if reference_time is not None:
        try:
            reference = _ensure_utc_iso(
                reference_time,
                "reference_time",
            )
        except ValueError as exc:
            errors.append(str(exc))
            reference = None

        if (
            reference is not None
            and observed_at is not None
            and observed_at > reference
        ):
            errors.append(
                f"{observation.observation_id}: observed_at cannot be "
                "in the future relative to reference_time."
            )

    return tuple(errors)


# ============================================================================
# FRESHNESS / STATUS
# ============================================================================

def calculate_observation_status(
    observation: StateObservation,
    *,
    reference_time: str | None = None,
) -> StateStatus:
    """
    Calculate lifecycle freshness status.

    Existing SUPERSEDED / CONFLICTED states are preserved.
    """

    if observation.status in {
        StateStatus.SUPERSEDED,
        StateStatus.CONFLICTED,
    }:
        return observation.status

    reference = (
        _ensure_utc_iso(reference_time, "reference_time")
        if reference_time
        else datetime.now(timezone.utc)
    )

    observed = _ensure_utc_iso(
        observation.observed_at,
        "observed_at",
    )

    if observation.expires_at is not None:
        expires = _ensure_utc_iso(
            observation.expires_at,
            "expires_at",
        )

        if reference >= expires:
            return StateStatus.EXPIRED

    if observed > reference:
        return StateStatus.UNKNOWN

    return StateStatus.ACTIVE


def refresh_statuses(
    observations: Iterable[StateObservation],
    *,
    reference_time: str | None = None,
) -> tuple[StateObservation, ...]:
    """Return observations with recalculated freshness status."""

    refreshed: list[StateObservation] = []

    for observation in observations:
        refreshed.append(
            StateObservation(
                observation_id=observation.observation_id,
                key=observation.key,
                value=observation.value,
                value_type=observation.value_type,
                observed_at=observation.observed_at,
                expires_at=observation.expires_at,
                truth=observation.truth,
                confidence=observation.confidence,
                criticality=observation.criticality,
                source=observation.source,
                status=calculate_observation_status(
                    observation,
                    reference_time=reference_time,
                ),
                supersedes=observation.supersedes,
                note=observation.note,
            )
        )

    return tuple(refreshed)


# ============================================================================
# CONFLICT DETECTION
# ============================================================================

def _semantic_value(value: object) -> str:
    """Create deterministic comparable representation of a state value."""

    return json.dumps(
        _safe_json_value(value),
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
    )


def detect_conflicts(
    observations: Iterable[StateObservation],
) -> tuple[StateConflict, ...]:
    """
    Detect conflicts among currently active/usable observations.

    A conflict exists when two observations for the same key have:
    - different semantic values,
    - and neither one clearly supersedes the other.
    """

    grouped: dict[str, list[StateObservation]] = {}

    for observation in observations:
        if observation.status in {
            StateStatus.EXPIRED,
            StateStatus.SUPERSEDED,
        }:
            continue

        grouped.setdefault(observation.key, []).append(observation)

    conflicts: list[StateConflict] = []

    for key, items in sorted(grouped.items()):
        if len(items) < 2:
            continue

        semantic_values = {
            _semantic_value(item.value)
            for item in items
        }

        if len(semantic_values) <= 1:
            continue

        ids = tuple(
            sorted(item.observation_id for item in items)
        )

        critical = any(
            item.criticality == StateCriticality.CRITICAL
            for item in items
        )

        conflicts.append(
            StateConflict(
                key=key,
                observation_ids=ids,
                reason=(
                    "Multiple non-superseded observations report "
                    "different values for the same world-state key."
                ),
                critical=critical,
            )
        )

    return tuple(conflicts)


# ============================================================================
# OBSERVATION INDEX / SNAPSHOT CONSTRUCTION
# ============================================================================

def observation_index(
    observations: Iterable[StateObservation],
) -> dict[str, StateObservation]:
    """Build an observation-ID index and reject duplicate IDs."""

    index: dict[str, StateObservation] = {}

    for observation in observations:
        if observation.observation_id in index:
            raise ValueError(
                "Duplicate observation ID: "
                f"{observation.observation_id}"
            )

        index[observation.observation_id] = observation

    return index


def create_observation(
    *,
    observation_id: str,
    key: str,
    value: object,
    observed_at: str,
    source_type: StateSourceType,
    source_id: str,
    evidence_quality: EvidenceQuality,
    confidence: float,
    criticality: StateCriticality = StateCriticality.MODERATE,
    expires_at: str | None = None,
    truth: StateTruth = StateTruth.TRUE,
    status: StateStatus = StateStatus.ACTIVE,
    supersedes: str | None = None,
    note: str = "",
    locator: str = "",
) -> StateObservation:
    """Create a typed StateObservation with automatic value-type inference."""

    return StateObservation(
        observation_id=observation_id,
        key=key,
        value=value,
        value_type=infer_value_type(value),
        observed_at=observed_at,
        expires_at=expires_at,
        truth=truth,
        confidence=confidence,
        criticality=criticality,
        source=StateSource(
            source_type=source_type,
            source_id=source_id,
            observed_at=observed_at,
            evidence_quality=evidence_quality,
            locator=locator,
        ),
        status=status,
        supersedes=supersedes,
        note=note,
    )


# ============================================================================
# DETERMINISTIC SERIALIZATION
# ============================================================================

def _source_material(source: StateSource) -> dict[str, object]:
    """Serialize StateSource deterministically."""

    return {
        "source_type": source.source_type.value,
        "source_id": source.source_id,
        "observed_at": source.observed_at,
        "evidence_quality": source.evidence_quality.value,
        "locator": source.locator,
    }


def _observation_material(
    observation: StateObservation,
) -> dict[str, object]:
    """Serialize StateObservation deterministically."""

    return {
        "observation_id": observation.observation_id,
        "key": observation.key,
        "value": _safe_json_value(observation.value),
        "value_type": observation.value_type.value,
        "observed_at": observation.observed_at,
        "expires_at": observation.expires_at,
        "truth": observation.truth.value,
        "confidence": observation.confidence,
        "criticality": observation.criticality.value,
        "source": _source_material(observation.source),
        "status": observation.status.value,
        "supersedes": observation.supersedes,
        "note": observation.note,
    }


def _conflict_material(
    conflict: StateConflict,
) -> dict[str, object]:
    """Serialize StateConflict deterministically."""

    return {
        "key": conflict.key,
        "observation_ids": list(conflict.observation_ids),
        "reason": conflict.reason,
        "critical": conflict.critical,
    }


def world_state_material(
    observations: Iterable[StateObservation],
) -> dict[str, object]:
    """Return canonical material for a World State snapshot."""

    normalized = tuple(
        sorted(
            observations,
            key=lambda item: item.observation_id,
        )
    )

    conflicts = detect_conflicts(normalized)

    return {
        "project_id": PROJECT_ID,
        "canonical_name": CANONICAL_NAME,
        "world_state_version": WORLD_STATE_VERSION,
        "brain_architecture_version": BRAIN_ARCHITECTURE_VERSION,
        "schema_version": SCHEMA_VERSION,
        "layer_number": LAYER_NUMBER,
        "layer_name": LAYER_NAME,
        "observations": [
            _observation_material(item)
            for item in normalized
        ],
        "conflicts": [
            _conflict_material(item)
            for item in conflicts
        ],
    }


def calculate_fingerprint(
    observations: Iterable[StateObservation],
) -> str:
    """Calculate deterministic SHA-256 fingerprint for a World State."""

    payload = json.dumps(
        world_state_material(observations),
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
    )

    return sha256(payload.encode("utf-8")).hexdigest()


# ============================================================================
# WORLD STATE EVALUATION
# ============================================================================

def evaluate_world_state(
    observations: Iterable[StateObservation],
    *,
    reference_time: str | None = None,
) -> WorldStateEvaluation:
    """
    Evaluate an entire World State snapshot.

    The snapshot is not usable when:
    - structural validation fails,
    - a critical observation is expired,
    - a critical conflict exists,
    - or observation identity is ambiguous.
    """

    snapshot = tuple(observations)

    errors: list[str] = []
    warnings: list[str] = []

    # Duplicate identity checks.
    try:
        observation_index(snapshot)
    except ValueError as exc:
        errors.append(str(exc))

    # Per-observation structural validation.
    for observation in snapshot:
        errors.extend(
            validate_observation(
                observation,
                reference_time=reference_time,
            )
        )

    refreshed = refresh_statuses(
        snapshot,
        reference_time=reference_time,
    )

    stale_count = sum(
        1
        for observation in refreshed
        if observation.status == StateStatus.STALE
    )

    expired_count = sum(
        1
        for observation in refreshed
        if observation.status == StateStatus.EXPIRED
    )

    conflicts = detect_conflicts(refreshed)

    for conflict in conflicts:
        if conflict.critical:
            errors.append(
                f"Critical World State conflict on key "
                f"{conflict.key}: {conflict.reason}"
            )
        else:
            warnings.append(
                f"World State conflict on key "
                f"{conflict.key}: {conflict.reason}"
            )

    for observation in refreshed:
        if observation.status == StateStatus.EXPIRED:
            message = (
                f"Observation {observation.observation_id} "
                f"is expired."
            )

            if observation.criticality in {
                StateCriticality.HIGH,
                StateCriticality.CRITICAL,
            }:
                errors.append(message)
            else:
                warnings.append(message)

        elif observation.status == StateStatus.STALE:
            warnings.append(
                f"Observation {observation.observation_id} is stale."
            )

    # Unknown truth for critical observations is not usable.
    for observation in refreshed:
        if (
            observation.criticality == StateCriticality.CRITICAL
            and observation.truth == StateTruth.UNKNOWN
        ):
            errors.append(
                f"Critical observation {observation.observation_id} "
                "has UNKNOWN truth state."
            )

    valid = not errors

    usable = (
        valid
        and not any(
            observation.status == StateStatus.EXPIRED
            and observation.criticality
            in {
                StateCriticality.HIGH,
                StateCriticality.CRITICAL,
            }
            for observation in refreshed
        )
    )

    snapshot_fingerprint = calculate_fingerprint(refreshed)

    return WorldStateEvaluation(
        valid=valid,
        usable=usable,
        stale_observation_count=stale_count,
        expired_observation_count=expired_count,
        conflicted_key_count=len(conflicts),
        critical_conflict_count=sum(
            1 for conflict in conflicts if conflict.critical
        ),
        errors=tuple(sorted(set(errors))),
        warnings=tuple(sorted(set(warnings))),
        fingerprint=snapshot_fingerprint,
    )


# ============================================================================
# FAIL-CLOSED WORLD STATE GATE
# ============================================================================

def assert_world_state_usable(
    observations: Iterable[StateObservation],
    *,
    reference_time: str | None = None,
) -> WorldStateEvaluation:
    """
    Fail closed when World State is not valid and usable.
    """

    evaluation = evaluate_world_state(
        observations,
        reference_time=reference_time,
    )

    if not evaluation.usable:
        reason = (
            evaluation.errors[0]
            if evaluation.errors
            else "World State is not usable."
        )

        raise RuntimeError(
            "World State gate failed closed: "
            f"{reason}"
        )

    return evaluation


# ============================================================================
# STATE QUERIES
# ============================================================================

def get_latest_for_key(
    observations: Iterable[StateObservation],
    key: str,
) -> StateObservation | None:
    """
    Return the newest active observation for a key.

    Expired and superseded observations are ignored.
    """

    candidates = [
        observation
        for observation in observations
        if (
            observation.key == key
            and observation.status
            not in {
                StateStatus.EXPIRED,
                StateStatus.SUPERSEDED,
            }
        )
    ]

    if not candidates:
        return None

    return max(
        candidates,
        key=lambda item: (
            _ensure_utc_iso(
                item.observed_at,
                "observed_at",
            ),
            item.confidence,
            EVIDENCE_RANK[item.source.evidence_quality],
        ),
    )


def query_state(
    observations: Iterable[StateObservation],
    *,
    prefix: str | None = None,
    criticality: StateCriticality | None = None,
    truth: StateTruth | None = None,
) -> tuple[StateObservation, ...]:
    """Query observations without mutating the canonical state."""

    result = tuple(observations)

    if prefix is not None:
        result = tuple(
            observation
            for observation in result
            if observation.key.startswith(prefix)
        )

    if criticality is not None:
        result = tuple(
            observation
            for observation in result
            if observation.criticality == criticality
        )

    if truth is not None:
        result = tuple(
            observation
            for observation in result
            if observation.truth == truth
        )

    return tuple(
        sorted(
            result,
            key=lambda item: item.observation_id,
        )
    )


# ============================================================================
# CHANGE / SNAPSHOT DIFFERENCING
# ============================================================================

def diff_world_state(
    before: Iterable[StateObservation],
    after: Iterable[StateObservation],
) -> dict[str, object]:
    """
    Compare two World State snapshots.

    Returns added, removed, changed, and unchanged observation IDs.
    """

    before_index = observation_index(tuple(before))
    after_index = observation_index(tuple(after))

    before_ids = set(before_index)
    after_ids = set(after_index)

    added = sorted(after_ids - before_ids)
    removed = sorted(before_ids - after_ids)

    common = sorted(before_ids & after_ids)

    changed: list[str] = []
    unchanged: list[str] = []

    for observation_id in common:
        before_material = _observation_material(
            before_index[observation_id]
        )
        after_material = _observation_material(
            after_index[observation_id]
        )

        if before_material == after_material:
            unchanged.append(observation_id)
        else:
            changed.append(observation_id)

    return {
        "added": added,
        "removed": removed,
        "changed": changed,
        "unchanged": unchanged,
    }


# ============================================================================
# STRUCTURAL VALIDATION
# ============================================================================

def validate_world_state_layer() -> tuple[str, ...]:
    """
    Validate static Layer 06 invariants.

    Returns an empty tuple on success.
    """

    errors: list[str] = []

    if PROJECT_ID != "intellect-media":
        errors.append("Project ID mismatch.")

    if CANONICAL_NAME != "Intellect Media":
        errors.append("Canonical project name mismatch.")

    if WORLD_STATE_VERSION != "1.0.0":
        errors.append("World State version mismatch.")

    if BRAIN_ARCHITECTURE_VERSION != "40.0.0":
        errors.append("Brain architecture version mismatch.")

    if LAYER_NUMBER != 6:
        errors.append("Layer number must be 6.")

    if LAYER_NAME != "World State":
        errors.append("Layer name mismatch.")

    if SCHEMA_VERSION != 1:
        errors.append("Schema version mismatch.")

    if not isinstance(EVIDENCE_RANK, dict):
        errors.append("Evidence rank map must be a dictionary.")

    if len(EVIDENCE_RANK) != len(EvidenceQuality):
        errors.append("Evidence rank map is incomplete.")

    if len(CRITICALITY_RANK) != len(StateCriticality):
        errors.append("Criticality rank map is incomplete.")

    expected_evidence_values = set(EvidenceQuality)

    if set(EVIDENCE_RANK) != expected_evidence_values:
        errors.append("Evidence rank map contains invalid keys.")

    expected_criticality_values = set(StateCriticality)

    if set(CRITICALITY_RANK) != expected_criticality_values:
        errors.append("Criticality rank map contains invalid keys.")

    return tuple(errors)


# ============================================================================
# SELF-TEST
# ============================================================================

def self_test() -> None:
    """Run deterministic Layer 06 self-tests."""

    static_errors = validate_world_state_layer()

    if static_errors:
        joined = "\n".join(
            f"- {error}"
            for error in static_errors
        )

        raise AssertionError(
            "World State static validation failed:\n"
            f"{joined}"
        )

    observed_at = "2026-01-01T10:00:00Z"
    future_reference = "2026-01-01T11:00:00Z"

    source = StateSource(
        source_type=StateSourceType.REPOSITORY,
        source_id="test-repository",
        observed_at=observed_at,
        evidence_quality=EvidenceQuality.VERIFIED,
        locator="self-test",
    )

    observation = StateObservation(
        observation_id="OBS-001",
        key="repository.branch",
        value="main",
        value_type=StateValueType.STRING,
        observed_at=observed_at,
        expires_at="2027-01-01T00:00:00Z",
        truth=StateTruth.TRUE,
        confidence=1.0,
        criticality=StateCriticality.CRITICAL,
        source=source,
        status=StateStatus.ACTIVE,
        note="Deterministic test observation.",
    )

    # Observation validation.
    assert not validate_observation(
        observation,
        reference_time=future_reference,
    )

    # Fingerprint determinism.
    fingerprint_a = calculate_fingerprint(
        (observation,)
    )
    fingerprint_b = calculate_fingerprint(
        (observation,)
    )

    assert fingerprint_a == fingerprint_b
    assert len(fingerprint_a) == 64

    # Freshness.
    refreshed = refresh_statuses(
        (observation,),
        reference_time=future_reference,
    )

    assert refreshed[0].status == StateStatus.ACTIVE

    # Latest-state query.
    latest = get_latest_for_key(
        refreshed,
        "repository.branch",
    )

    assert latest is not None
    assert latest.value == "main"

    # Valid snapshot.
    evaluation = evaluate_world_state(
        refreshed,
        reference_time=future_reference,
    )

    assert evaluation.valid is True
    assert evaluation.usable is True
    assert evaluation.stale_observation_count == 0
    assert evaluation.expired_observation_count == 0
    assert evaluation.conflicted_key_count == 0
    assert evaluation.critical_conflict_count == 0

    # Expired critical state must fail closed.
    expired_observation = StateObservation(
        observation_id="OBS-002",
        key="repository.commit",
        value="deadbeef",
        value_type=StateValueType.STRING,
        observed_at=observed_at,
        expires_at="2026-01-01T10:30:00Z",
        truth=StateTruth.TRUE,
        confidence=1.0,
        criticality=StateCriticality.CRITICAL,
        source=source,
        status=StateStatus.ACTIVE,
    )

    expired_evaluation = evaluate_world_state(
        (expired_observation,),
        reference_time="2026-01-01T11:00:00Z",
    )

    assert expired_evaluation.valid is False
    assert expired_evaluation.usable is False
    assert expired_evaluation.expired_observation_count == 1

    # Conflict detection.
    conflict_source_a = StateSource(
        source_type=StateSourceType.GIT,
        source_id="git-a",
        observed_at=observed_at,
        evidence_quality=EvidenceQuality.STRONG,
    )

    conflict_source_b = StateSource(
        source_type=StateSourceType.TOOL,
        source_id="tool-b",
        observed_at=observed_at,
        evidence_quality=EvidenceQuality.MODERATE,
    )

    conflict_a = StateObservation(
        observation_id="OBS-003",
        key="repository.status",
        value="clean",
        value_type=StateValueType.STRING,
        observed_at=observed_at,
        expires_at=None,
        truth=StateTruth.TRUE,
        confidence=0.90,
        criticality=StateCriticality.HIGH,
        source=conflict_source_a,
    )

    conflict_b = StateObservation(
        observation_id="OBS-004",
        key="repository.status",
        value="dirty",
        value_type=StateValueType.STRING,
        observed_at=observed_at,
        expires_at=None,
        truth=StateTruth.TRUE,
        confidence=0.80,
        criticality=StateCriticality.HIGH,
        source=conflict_source_b,
    )

    conflicts = detect_conflicts(
        (conflict_a, conflict_b)
    )

    assert len(conflicts) == 1
    assert conflicts[0].key == "repository.status"
    assert conflicts[0].critical is False

    conflict_evaluation = evaluate_world_state(
        (conflict_a, conflict_b),
        reference_time=future_reference,
    )

    assert conflict_evaluation.valid is True
    assert conflict_evaluation.usable is True
    assert conflict_evaluation.conflicted_key_count == 1

    # Critical conflict must fail closed.
    critical_conflict_a = StateObservation(
        observation_id="OBS-005",
        key="project.identity",
        value="intellect-media",
        value_type=StateValueType.STRING,
        observed_at=observed_at,
        expires_at=None,
        truth=StateTruth.TRUE,
        confidence=1.0,
        criticality=StateCriticality.CRITICAL,
        source=conflict_source_a,
    )

    critical_conflict_b = StateObservation(
        observation_id="OBS-006",
        key="project.identity",
        value="unknown-project",
        value_type=StateValueType.STRING,
        observed_at=observed_at,
        expires_at=None,
        truth=StateTruth.TRUE,
        confidence=0.60,
        criticality=StateCriticality.CRITICAL,
        source=conflict_source_b,
    )

    critical_evaluation = evaluate_world_state(
        (
            critical_conflict_a,
            critical_conflict_b,
        ),
        reference_time=future_reference,
    )

    assert critical_evaluation.valid is False
    assert critical_evaluation.usable is False
    assert critical_evaluation.critical_conflict_count == 1

    # Diff test.
    changed_observation = StateObservation(
        observation_id="OBS-001",
        key="repository.branch",
        value="develop",
        value_type=StateValueType.STRING,
        observed_at="2026-01-01T10:30:00Z",
        expires_at="2027-01-01T00:00:00Z",
        truth=StateTruth.TRUE,
        confidence=1.0,
        criticality=StateCriticality.CRITICAL,
        source=source,
    )

    diff = diff_world_state(
        (observation,),
        (
            changed_observation,
            expired_observation,
        ),
    )

    assert diff["changed"] == ["OBS-001"]
    assert diff["added"] == ["OBS-002"]
    assert diff["removed"] == []

    # Fail-closed assertion test.
    try:
        assert_world_state_usable(
            (expired_observation,),
            reference_time="2026-01-01T11:00:00Z",
        )
    except RuntimeError:
        pass
    else:
        raise AssertionError(
            "assert_world_state_usable() did not fail closed."
        )


# ============================================================================
# PUBLIC SUMMARY
# ============================================================================

def get_world_state_summary(
    observations: Iterable[StateObservation],
) -> dict[str, object]:
    """Return a machine-readable summary of a World State snapshot."""

    snapshot = tuple(observations)

    evaluation = evaluate_world_state(
        snapshot,
        reference_time=now_utc_iso(),
    )

    active_count = sum(
        1
        for observation in refresh_statuses(
            snapshot,
            reference_time=now_utc_iso(),
        )
        if observation.status == StateStatus.ACTIVE
    )

    critical_count = sum(
        1
        for observation in snapshot
        if observation.criticality == StateCriticality.CRITICAL
    )

    return {
        "project_id": PROJECT_ID,
        "canonical_name": CANONICAL_NAME,
        "layer_number": LAYER_NUMBER,
        "layer_name": LAYER_NAME,
        "version": WORLD_STATE_VERSION,
        "brain_architecture_version": BRAIN_ARCHITECTURE_VERSION,
        "schema_version": SCHEMA_VERSION,
        "observation_count": len(snapshot),
        "active_observation_count": active_count,
        "critical_observation_count": critical_count,
        "stale_observation_count": evaluation.stale_observation_count,
        "expired_observation_count": evaluation.expired_observation_count,
        "conflicted_key_count": evaluation.conflicted_key_count,
        "critical_conflict_count": evaluation.critical_conflict_count,
        "valid": evaluation.valid,
        "usable": evaluation.usable,
        "fingerprint": evaluation.fingerprint,
    }


# ============================================================================
# EXECUTION ENTRYPOINT
# ============================================================================

if __name__ == "__main__":
    self_test()

    summary = get_world_state_summary(())

    print(
        f"Intellect Media World State v{WORLD_STATE_VERSION}: PASS"
    )
    print(f"Project ID             : {summary['project_id']}")
    print(
        f"Layer                  : "
        f"{summary['layer_number']} — {summary['layer_name']}"
    )
    print(
        f"Brain Architecture     : "
        f"v{summary['brain_architecture_version']}"
    )
    print(f"Schema Version         : {summary['schema_version']}")
    print(f"Observations           : {summary['observation_count']}")
    print(
        f"Active Observations    : "
        f"{summary['active_observation_count']}"
    )
    print(
        f"Critical Observations  : "
        f"{summary['critical_observation_count']}"
    )
    print(
        f"Stale Observations     : "
        f"{summary['stale_observation_count']}"
    )
    print(
        f"Expired Observations   : "
        f"{summary['expired_observation_count']}"
    )
    print(
        f"Conflicted Keys        : "
        f"{summary['conflicted_key_count']}"
    )
    print(
        f"Critical Conflicts     : "
        f"{summary['critical_conflict_count']}"
    )
    print(f"Valid                  : {summary['valid']}")
    print(f"Usable                 : {summary['usable']}")
    print(f"Fingerprint            : {summary['fingerprint']}")
