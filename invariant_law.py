"""
INTELLECT MEDIA — INVARIANT / LAW
Layer 05 of the canonical 40-layer Project Brain.

Project Identity     = WHO the project is
Project DNA          = WHY the project exists
Architecture         = WHAT structure is allowed
Authority            = WHO MAY DECIDE / ACT / OVERRIDE
Invariant / Law      = WHAT MUST NEVER BE BROKEN

Invariant / Law is the non-negotiable integrity layer.

Its purpose is to:
- define immutable system laws,
- evaluate proposed state/actions against those laws,
- fail closed when critical invariants are violated,
- prevent lower layers from silently bypassing higher authority,
- provide deterministic integrity fingerprints,
- support auditability and future autonomous verification.

This file is intentionally dependency-light and deterministic.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from hashlib import sha256
import json
from typing import Final, Mapping


# ---------------------------------------------------------------------------
# CANONICAL PROJECT CONSTANTS
# ---------------------------------------------------------------------------

PROJECT_ID: Final[str] = "intellect-media"
CANONICAL_NAME: Final[str] = "Intellect Media"

INVARIANT_LAW_VERSION: Final[str] = "1.0.0"
BRAIN_ARCHITECTURE_VERSION: Final[str] = "40.0.0"

LAYER_NUMBER: Final[int] = 5
LAYER_NAME: Final[str] = "Invariant / Law"


# ---------------------------------------------------------------------------
# ENUMERATIONS
# ---------------------------------------------------------------------------

class LawSeverity(str, Enum):
    """Severity of a law violation."""

    INFO = "info"
    WARNING = "warning"
    HIGH = "high"
    CRITICAL = "critical"
    FATAL = "fatal"


SEVERITY_RANK: Final[dict[LawSeverity, int]] = {
    LawSeverity.INFO: 0,
    LawSeverity.WARNING: 1,
    LawSeverity.HIGH: 2,
    LawSeverity.CRITICAL: 3,
    LawSeverity.FATAL: 4,
}


class LawCategory(str, Enum):
    """Canonical categories of project invariants."""

    IDENTITY = "identity"
    DNA = "dna"
    ARCHITECTURE = "architecture"
    AUTHORITY = "authority"
    INTEGRITY = "integrity"
    SAFETY = "safety"
    CONTINUITY = "continuity"
    STATE = "state"
    EXECUTION = "execution"
    AUDIT = "audit"
    REPOSITORY = "repository"
    EVOLUTION = "evolution"


class ViolationAction(str, Enum):
    """Action the system must take when a law is violated."""

    ALLOW = "allow"
    WARN = "warn"
    BLOCK = "block"
    FAIL_CLOSED = "fail_closed"
    ESCALATE = "escalate"


# ---------------------------------------------------------------------------
# LAW DEFINITION
# ---------------------------------------------------------------------------

@dataclass(frozen=True, slots=True)
class InvariantLaw:
    """
    One canonical project law.

    Laws are declarative at Layer 05 and can later be consumed by
    verification/execution layers.
    """

    law_id: str
    name: str
    category: LawCategory
    severity: LawSeverity
    description: str

    immutable: bool = True
    fail_closed: bool = True
    requires_authority: bool = True
    auditable: bool = True


@dataclass(frozen=True, slots=True)
class LawViolation:
    """Deterministic representation of a detected law violation."""

    law_id: str
    severity: LawSeverity
    action: ViolationAction
    reason: str
    evidence: str = ""


@dataclass(frozen=True, slots=True)
class LawEvaluation:
    """Result of evaluating a proposed condition against project laws."""

    allowed: bool
    fail_closed: bool
    violations: tuple[LawViolation, ...]
    warnings: tuple[LawViolation, ...]
    fingerprint: str


# ---------------------------------------------------------------------------
# CANONICAL LAWS
# ---------------------------------------------------------------------------

CANONICAL_LAWS: Final[tuple[InvariantLaw, ...]] = (
    InvariantLaw(
        law_id="LAW-001",
        name="Identity Immutability",
        category=LawCategory.IDENTITY,
        severity=LawSeverity.FATAL,
        description=(
            "Project Identity must never be silently changed by a lower "
            "authority layer, model, agent, tool, or runtime process."
        ),
    ),
    InvariantLaw(
        law_id="LAW-002",
        name="DNA Integrity",
        category=LawCategory.DNA,
        severity=LawSeverity.FATAL,
        description=(
            "Project DNA cannot be silently redefined by execution layers "
            "or autonomous actors."
        ),
    ),
    InvariantLaw(
        law_id="LAW-003",
        name="Architecture Integrity",
        category=LawCategory.ARCHITECTURE,
        severity=LawSeverity.CRITICAL,
        description=(
            "The canonical 40-layer Brain architecture must not be "
            "silently reordered, duplicated, removed, or redefined."
        ),
    ),
    InvariantLaw(
        law_id="LAW-004",
        name="Authority Precedence",
        category=LawCategory.AUTHORITY,
        severity=LawSeverity.FATAL,
        description=(
            "No lower authority may outrank, bypass, or silently override "
            "a higher authority."
        ),
    ),
    InvariantLaw(
        law_id="LAW-005",
        name="Ambiguity Fails Closed",
        category=LawCategory.SAFETY,
        severity=LawSeverity.CRITICAL,
        description=(
            "When authority, identity, intent, state, or rule applicability "
            "is materially ambiguous, the action must not proceed."
        ),
    ),
    InvariantLaw(
        law_id="LAW-006",
        name="Integrity Before Execution",
        category=LawCategory.INTEGRITY,
        severity=LawSeverity.CRITICAL,
        description=(
            "Integrity and validity checks must occur before a critical "
            "state-changing action is accepted."
        ),
    ),
    InvariantLaw(
        law_id="LAW-007",
        name="No Hidden State Mutation",
        category=LawCategory.STATE,
        severity=LawSeverity.CRITICAL,
        description=(
            "Canonical state must not be mutated invisibly or without "
            "a traceable authority and audit record."
        ),
    ),
    InvariantLaw(
        law_id="LAW-008",
        name="Verification Before Claim",
        category=LawCategory.EXECUTION,
        severity=LawSeverity.HIGH,
        description=(
            "The system must not claim successful completion without "
            "objective verification evidence."
        ),
    ),
    InvariantLaw(
        law_id="LAW-009",
        name="Continuity Preservation",
        category=LawCategory.CONTINUITY,
        severity=LawSeverity.CRITICAL,
        description=(
            "Project continuity data must remain reconstructable across "
            "sessions, agents, executions, and recovery events."
        ),
    ),
    InvariantLaw(
        law_id="LAW-010",
        name="Auditability",
        category=LawCategory.AUDIT,
        severity=LawSeverity.HIGH,
        description=(
            "Critical decisions, state changes, overrides, and failures "
            "must remain attributable and reconstructable."
        ),
    ),
    InvariantLaw(
        law_id="LAW-011",
        name="Repository Truth",
        category=LawCategory.REPOSITORY,
        severity=LawSeverity.CRITICAL,
        description=(
            "Repository state must not be falsely represented as canonical, "
            "verified, committed, or synchronized without evidence."
        ),
    ),
    InvariantLaw(
        law_id="LAW-012",
        name="Controlled Evolution",
        category=LawCategory.EVOLUTION,
        severity=LawSeverity.CRITICAL,
        description=(
            "Canonical laws may evolve only through explicit authority, "
            "versioned change control, validation, and recorded lineage."
        ),
    ),
)


EXPECTED_LAW_COUNT: Final[int] = 12


# ---------------------------------------------------------------------------
# LAW INDEX
# ---------------------------------------------------------------------------

LAW_INDEX: Final[dict[str, InvariantLaw]] = {
    law.law_id: law for law in CANONICAL_LAWS
}


# ---------------------------------------------------------------------------
# DETERMINISTIC FINGERPRINTING
# ---------------------------------------------------------------------------

def _canonical_material() -> dict[str, object]:
    """Return deterministic material used for the law fingerprint."""

    return {
        "project_id": PROJECT_ID,
        "canonical_name": CANONICAL_NAME,
        "invariant_law_version": INVARIANT_LAW_VERSION,
        "brain_architecture_version": BRAIN_ARCHITECTURE_VERSION,
        "layer_number": LAYER_NUMBER,
        "layer_name": LAYER_NAME,
        "laws": [
            {
                "law_id": law.law_id,
                "name": law.name,
                "category": law.category.value,
                "severity": law.severity.value,
                "description": law.description,
                "immutable": law.immutable,
                "fail_closed": law.fail_closed,
                "requires_authority": law.requires_authority,
                "auditable": law.auditable,
            }
            for law in CANONICAL_LAWS
        ],
    }


def calculate_fingerprint() -> str:
    """Calculate a deterministic SHA-256 fingerprint of the law set."""

    payload = json.dumps(
        _canonical_material(),
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
    )

    return sha256(payload.encode("utf-8")).hexdigest()


LAW_FINGERPRINT: Final[str] = calculate_fingerprint()


def verify_fingerprint(expected: str = LAW_FINGERPRINT) -> bool:
    """Verify that the current canonical law material matches the expected fingerprint."""

    return calculate_fingerprint() == expected


# ---------------------------------------------------------------------------
# LAW LOOKUP
# ---------------------------------------------------------------------------

def get_law(law_id: str) -> InvariantLaw:
    """Return one canonical law by ID."""

    try:
        return LAW_INDEX[law_id]
    except KeyError as exc:
        raise KeyError(f"Unknown invariant law: {law_id}") from exc


def list_laws(
    *,
    category: LawCategory | None = None,
    minimum_severity: LawSeverity | None = None,
) -> tuple[InvariantLaw, ...]:
    """Return laws filtered by category and/or minimum severity."""

    result = CANONICAL_LAWS

    if category is not None:
        result = tuple(
            law for law in result
            if law.category == category
        )

    if minimum_severity is not None:
        threshold = SEVERITY_RANK[minimum_severity]
        result = tuple(
            law for law in result
            if SEVERITY_RANK[law.severity] >= threshold
        )

    return result


# ---------------------------------------------------------------------------
# LAW EVALUATION
# ---------------------------------------------------------------------------

def evaluate_law(
    law_id: str,
    *,
    condition_holds: bool,
    evidence: str = "",
    reason: str = "",
) -> LawViolation | None:
    """
    Evaluate one law.

    Returns None when the invariant is satisfied.
    Returns a deterministic violation record when it is not.
    """

    law = get_law(law_id)

    if condition_holds:
        return None

    action = (
        ViolationAction.FAIL_CLOSED
        if law.fail_closed
        else ViolationAction.BLOCK
    )

    return LawViolation(
        law_id=law.law_id,
        severity=law.severity,
        action=action,
        reason=reason or law.description,
        evidence=evidence,
    )


def evaluate_laws(
    checks: Mapping[str, bool],
    *,
    evidence: Mapping[str, str] | None = None,
    reasons: Mapping[str, str] | None = None,
) -> LawEvaluation:
    """
    Evaluate a set of canonical law checks.

    Unknown law IDs are treated as unsafe and therefore fail closed.
    Missing canonical checks are also unsafe for critical validation.
    """

    evidence = evidence or {}
    reasons = reasons or {}

    violations: list[LawViolation] = []
    warnings: list[LawViolation] = []

    # Unknown law identifiers are never silently accepted.
    unknown_ids = sorted(set(checks) - set(LAW_INDEX))

    for law_id in unknown_ids:
        violations.append(
            LawViolation(
                law_id=law_id,
                severity=LawSeverity.FATAL,
                action=ViolationAction.FAIL_CLOSED,
                reason="Unknown law identifier supplied to evaluator.",
                evidence=evidence.get(law_id, ""),
            )
        )

    # Missing checks are treated as unsafe.
    missing_ids = sorted(set(LAW_INDEX) - set(checks))

    for law_id in missing_ids:
        law = LAW_INDEX[law_id]
        violations.append(
            LawViolation(
                law_id=law_id,
                severity=LawSeverity.CRITICAL,
                action=ViolationAction.FAIL_CLOSED,
                reason=(
                    "Canonical law was not evaluated. "
                    "Critical validation cannot proceed with missing law checks."
                ),
                evidence="",
            )
        )

    # Evaluate supplied canonical checks.
    for law_id, condition_holds in sorted(checks.items()):
        if law_id not in LAW_INDEX:
            continue

        violation = evaluate_law(
            law_id,
            condition_holds=condition_holds,
            evidence=evidence.get(law_id, ""),
            reason=reasons.get(law_id, ""),
        )

        if violation is None:
            continue

        if violation.severity in {
            LawSeverity.INFO,
            LawSeverity.WARNING,
        }:
            warnings.append(violation)
        else:
            violations.append(violation)

    fail_closed = any(
        violation.action == ViolationAction.FAIL_CLOSED
        for violation in violations
    )

    allowed = not violations

    evaluation_material = {
        "allowed": allowed,
        "fail_closed": fail_closed,
        "violations": [
            {
                "law_id": violation.law_id,
                "severity": violation.severity.value,
                "action": violation.action.value,
                "reason": violation.reason,
                "evidence": violation.evidence,
            }
            for violation in violations
        ],
        "warnings": [
            {
                "law_id": warning.law_id,
                "severity": warning.severity.value,
                "action": warning.action.value,
                "reason": warning.reason,
                "evidence": warning.evidence,
            }
            for warning in warnings
        ],
    }

    result_payload = json.dumps(
        evaluation_material,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
    )

    evaluation_fingerprint = sha256(
        result_payload.encode("utf-8")
    ).hexdigest()

    return LawEvaluation(
        allowed=allowed,
        fail_closed=fail_closed,
        violations=tuple(
            sorted(
                violations,
                key=lambda item: (
                    -SEVERITY_RANK[item.severity],
                    item.law_id,
                ),
            )
        ),
        warnings=tuple(
            sorted(
                warnings,
                key=lambda item: (
                    -SEVERITY_RANK[item.severity],
                    item.law_id,
                ),
            )
        ),
        fingerprint=evaluation_fingerprint,
    )


# ---------------------------------------------------------------------------
# FAIL-CLOSED GATE
# ---------------------------------------------------------------------------

def assert_laws_hold(
    checks: Mapping[str, bool],
    *,
    evidence: Mapping[str, str] | None = None,
    reasons: Mapping[str, str] | None = None,
) -> LawEvaluation:
    """
    Enforce canonical laws.

    Raises RuntimeError when any blocking violation exists.
    """

    evaluation = evaluate_laws(
        checks,
        evidence=evidence,
        reasons=reasons,
    )

    if not evaluation.allowed:
        primary = evaluation.violations[0]

        raise RuntimeError(
            "Invariant / Law gate failed: "
            f"{primary.law_id} | "
            f"{primary.severity.value} | "
            f"{primary.reason}"
        )

    return evaluation


# ---------------------------------------------------------------------------
# STRUCTURAL VALIDATION
# ---------------------------------------------------------------------------

def validate_laws() -> tuple[str, ...]:
    """
    Validate the canonical law set.

    Returns an empty tuple on success or deterministic error messages.
    """

    errors: list[str] = []

    if PROJECT_ID != "intellect-media":
        errors.append("Project ID mismatch.")

    if CANONICAL_NAME != "Intellect Media":
        errors.append("Canonical project name mismatch.")

    if LAYER_NUMBER != 5:
        errors.append("Layer number must be 5.")

    if LAYER_NAME != "Invariant / Law":
        errors.append("Layer name mismatch.")

    if BRAIN_ARCHITECTURE_VERSION != "40.0.0":
        errors.append("Brain architecture version mismatch.")

    if len(CANONICAL_LAWS) != EXPECTED_LAW_COUNT:
        errors.append(
            f"Expected {EXPECTED_LAW_COUNT} laws; "
            f"found {len(CANONICAL_LAWS)}."
        )

    law_ids = [law.law_id for law in CANONICAL_LAWS]

    if len(set(law_ids)) != len(law_ids):
        errors.append("Duplicate law IDs detected.")

    expected_ids = [
        f"LAW-{index:03d}"
        for index in range(1, EXPECTED_LAW_COUNT + 1)
    ]

    if law_ids != expected_ids:
        errors.append(
            "Law IDs must remain sequential from "
            "LAW-001 through LAW-012."
        )

    for law in CANONICAL_LAWS:
        if not law.name.strip():
            errors.append(f"{law.law_id} has an empty name.")

        if not law.description.strip():
            errors.append(f"{law.law_id} has an empty description.")

        if law.immutable is not True:
            errors.append(
                f"{law.law_id} must remain immutable."
            )

        if law.requires_authority is not True:
            errors.append(
                f"{law.law_id} must require authority."
            )

        if law.auditable is not True:
            errors.append(
                f"{law.law_id} must remain auditable."
            )

    if set(LAW_INDEX) != set(law_ids):
        errors.append("Law index does not match canonical laws.")

    if not verify_fingerprint():
        errors.append("Canonical law fingerprint verification failed.")

    return tuple(errors)


# ---------------------------------------------------------------------------
# SELF-TEST
# ---------------------------------------------------------------------------

def self_test() -> None:
    """Run deterministic Layer 05 self-tests."""

    errors = validate_laws()

    if errors:
        joined = "\n".join(f"- {error}" for error in errors)
        raise AssertionError(
            "Invariant / Law structural validation failed:\n"
            f"{joined}"
        )

    # Complete-validity test.
    valid_checks = {
        law.law_id: True
        for law in CANONICAL_LAWS
    }

    evaluation = evaluate_laws(valid_checks)

    assert evaluation.allowed is True
    assert evaluation.fail_closed is False
    assert not evaluation.violations
    assert len(evaluation.fingerprint) == 64

    # Deliberate violation test.
    invalid_checks = dict(valid_checks)
    invalid_checks["LAW-004"] = False

    invalid_evaluation = evaluate_laws(invalid_checks)

    assert invalid_evaluation.allowed is False
    assert invalid_evaluation.fail_closed is True
    assert any(
        violation.law_id == "LAW-004"
        for violation in invalid_evaluation.violations
    )

    # Missing-law fail-closed test.
    incomplete_checks = dict(valid_checks)
    incomplete_checks.pop("LAW-005")

    incomplete_evaluation = evaluate_laws(incomplete_checks)

    assert incomplete_evaluation.allowed is False
    assert incomplete_evaluation.fail_closed is True
    assert any(
        violation.law_id == "LAW-005"
        for violation in incomplete_evaluation.violations
    )

    # Unknown-law fail-closed test.
    unknown_checks = dict(valid_checks)
    unknown_checks["LAW-999"] = True

    unknown_evaluation = evaluate_laws(unknown_checks)

    assert unknown_evaluation.allowed is False
    assert unknown_evaluation.fail_closed is True
    assert any(
        violation.law_id == "LAW-999"
        for violation in unknown_evaluation.violations
    )

    # Fingerprint must remain deterministic.
    first = calculate_fingerprint()
    second = calculate_fingerprint()

    assert first == second
    assert first == LAW_FINGERPRINT
    assert len(first) == 64


# ---------------------------------------------------------------------------
# PUBLIC SUMMARY
# ---------------------------------------------------------------------------

def get_law_summary() -> dict[str, object]:
    """Return a machine-readable summary of Layer 05."""

    return {
        "project_id": PROJECT_ID,
        "canonical_name": CANONICAL_NAME,
        "layer_number": LAYER_NUMBER,
        "layer_name": LAYER_NAME,
        "version": INVARIANT_LAW_VERSION,
        "brain_architecture_version": BRAIN_ARCHITECTURE_VERSION,
        "law_count": len(CANONICAL_LAWS),
        "immutable_law_count": sum(
            1 for law in CANONICAL_LAWS if law.immutable
        ),
        "fail_closed_law_count": sum(
            1 for law in CANONICAL_LAWS if law.fail_closed
        ),
        "auditable_law_count": sum(
            1 for law in CANONICAL_LAWS if law.auditable
        ),
        "fingerprint": LAW_FINGERPRINT,
    }


# ---------------------------------------------------------------------------
# EXECUTION ENTRYPOINT
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    self_test()

    summary = get_law_summary()

    print(
        f"Intellect Media Invariant / Law v{INVARIANT_LAW_VERSION}: PASS"
    )
    print(f"Project ID          : {summary['project_id']}")
    print(
        f"Layer               : "
        f"{summary['layer_number']} — {summary['layer_name']}"
    )
    print(
        f"Brain Architecture  : "
        f"v{summary['brain_architecture_version']}"
    )
    print(f"Laws                : {summary['law_count']}")
    print(
        f"Immutable Laws      : "
        f"{summary['immutable_law_count']}"
    )
    print(
        f"Fail-Closed Laws    : "
        f"{summary['fail_closed_law_count']}"
    )
    print(
        f"Auditable Laws      : "
        f"{summary['auditable_law_count']}"
    )
    print(f"Fingerprint         : {summary['fingerprint']}")
