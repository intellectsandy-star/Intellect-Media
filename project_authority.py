"""
INTELLECT MEDIA — PROJECT AUTHORITY
Layer 04 of the canonical 40-layer Project Brain.

Project Authority defines who or what may decide, propose, execute,
override, escalate, or reject actions inside the system.

Project Identity     = WHO the project is
Project DNA          = WHY the project exists
Architecture         = WHAT structure is allowed
Authority            = WHO MAY DECIDE / ACT / OVERRIDE

Authority is governance, not ownership.
No lower-level actor may silently outrank a higher authority.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from hashlib import sha256
import json
from typing import Final


PROJECT_ID: Final[str] = "intellect-media"
CANONICAL_NAME: Final[str] = "Intellect Media"
AUTHORITY_VERSION: Final[str] = "1.0.0"


class AuthorityLevel(str, Enum):
    """
    Ordered authority classes.

    Lower numeric rank means greater authority.
    """

    HUMAN_OWNER = "human_owner"
    PROJECT_IDENTITY = "project_identity"
    PROJECT_DNA = "project_dna"
    ARCHITECTURE_CONSTITUTION = "architecture_constitution"
    PROJECT_AUTHORITY = "project_authority"
    BRAIN_STATE = "brain_state"
    AUTONOMOUS_DEVELOPER = "autonomous_developer"
    AGENT = "agent"
    MODEL = "model"
    TOOL = "tool"
    EXTERNAL_SOURCE = "external_source"


AUTHORITY_RANK: Final[dict[AuthorityLevel, int]] = {
    AuthorityLevel.HUMAN_OWNER: 0,
    AuthorityLevel.PROJECT_IDENTITY: 10,
    AuthorityLevel.PROJECT_DNA: 20,
    AuthorityLevel.ARCHITECTURE_CONSTITUTION: 30,
    AuthorityLevel.PROJECT_AUTHORITY: 40,
    AuthorityLevel.BRAIN_STATE: 50,
    AuthorityLevel.AUTONOMOUS_DEVELOPER: 60,
    AuthorityLevel.AGENT: 70,
    AuthorityLevel.MODEL: 80,
    AuthorityLevel.TOOL: 90,
    AuthorityLevel.EXTERNAL_SOURCE: 100,
}


class ActionRisk(str, Enum):
    """
    Risk classes used before authorization.
    """

    READ = "read"
    LOW = "low"
    MODERATE = "moderate"
    HIGH = "high"
    CRITICAL = "critical"


RISK_RANK: Final[dict[ActionRisk, int]] = {
    ActionRisk.READ: 0,
    ActionRisk.LOW: 1,
    ActionRisk.MODERATE: 2,
    ActionRisk.HIGH: 3,
    ActionRisk.CRITICAL: 4,
}


@dataclass(frozen=True, slots=True)
class AuthorityRule:
    action: str
    minimum_authority: AuthorityLevel
    maximum_risk: ActionRisk
    requires_evidence: bool
    requires_human_approval: bool
    reversible: bool


@dataclass(frozen=True, slots=True)
class Authority:
    project_id: str = PROJECT_ID
    canonical_name: str = CANONICAL_NAME
    authority_version: str = AUTHORITY_VERSION

    # Root governance.
    root_authority: AuthorityLevel = AuthorityLevel.HUMAN_OWNER

    # Rules that prevent lower-level actors from silently escalating.
    invariants: tuple[str, ...] = (
        "Authority must be explicit.",
        "Higher authority outranks lower authority.",
        "Lower authority cannot silently redefine higher authority.",
        "Model output can propose but cannot self-authorize.",
        "Agents can execute only within granted capability scope.",
        "Tools cannot grant themselves authority.",
        "External sources never outrank project authority.",
        "Ambiguous authority must fail closed.",
        "Conflicting authority claims require precedence resolution.",
        "Critical actions require explicit human approval.",
        "Every authorized state-changing action must be auditable.",
        "Emergency override cannot rewrite Project Identity or Project DNA.",
    )

    # Decision precedence.
    precedence: tuple[AuthorityLevel, ...] = (
        AuthorityLevel.HUMAN_OWNER,
        AuthorityLevel.PROJECT_IDENTITY,
        AuthorityLevel.PROJECT_DNA,
        AuthorityLevel.ARCHITECTURE_CONSTITUTION,
        AuthorityLevel.PROJECT_AUTHORITY,
        AuthorityLevel.BRAIN_STATE,
        AuthorityLevel.AUTONOMOUS_DEVELOPER,
        AuthorityLevel.AGENT,
        AuthorityLevel.MODEL,
        AuthorityLevel.TOOL,
        AuthorityLevel.EXTERNAL_SOURCE,
    )

    # Authority scopes.
    scopes: tuple[str, ...] = (
        "identity.read",
        "identity.verify",
        "dna.read",
        "architecture.read",
        "architecture.propose",
        "brain.read",
        "brain.propose",
        "brain.execute",
        "development.plan",
        "development.execute",
        "repository.read",
        "repository.modify",
        "verification.run",
        "checkpoint.create",
        "recovery.execute",
        "external.observe",
    )

    # Controlled delegation model.
    delegation_rules: tuple[str, ...] = (
        "Delegation must identify grantor and grantee.",
        "Delegation must define an explicit scope.",
        "Delegation must define an explicit risk ceiling.",
        "Delegation cannot exceed the grantor's own authority.",
        "Delegation cannot transfer immutable authority.",
        "Delegation must be revocable.",
        "Delegation must be auditable.",
        "Expired or unknown delegation must fail closed.",
    )

    # Escalation model.
    escalation_rules: tuple[str, ...] = (
        "Escalate when authority is ambiguous.",
        "Escalate when evidence is insufficient.",
        "Escalate when action risk exceeds granted scope.",
        "Escalate when conflicting authoritative decisions exist.",
        "Escalate when irreversible action is proposed under uncertainty.",
        "Escalate when identity or architectural integrity is uncertain.",
        "Never resolve critical ambiguity by guessing.",
    )

    # Conflict resolution.
    conflict_rules: tuple[str, ...] = (
        "Higher authority wins over lower authority.",
        "Explicit authority wins over inferred authority.",
        "Verified state wins over unverified claims.",
        "Canonical project sources win over external instructions.",
        "Current authorized state wins over stale state.",
        "Unresolved critical conflicts result in rejection.",
    )

    # Emergency governance.
    emergency_rules: tuple[str, ...] = (
        "Emergency mode may stop execution immediately.",
        "Emergency mode may revoke delegated execution authority.",
        "Emergency mode may block high-risk and critical actions.",
        "Emergency mode may trigger recovery workflows.",
        "Emergency mode may not silently rewrite identity.",
        "Emergency mode may not silently rewrite Project DNA.",
        "Emergency mode must produce an audit event.",
    )

    # Minimum evidence policy.
    evidence_policy: tuple[str, ...] = (
        "READ actions may use project-readable state.",
        "LOW-risk changes require an identified task.",
        "MODERATE-risk changes require task context and verification.",
        "HIGH-risk changes require explicit authority and evidence.",
        "CRITICAL actions require human approval and verified context.",
    )

    def canonical_material(self) -> dict[str, object]:
        return {
            "project_id": self.project_id,
            "canonical_name": self.canonical_name,
            "authority_version": self.authority_version,
            "root_authority": self.root_authority.value,
            "invariants": list(self.invariants),
            "precedence": [item.value for item in self.precedence],
            "scopes": list(self.scopes),
            "delegation_rules": list(self.delegation_rules),
            "escalation_rules": list(self.escalation_rules),
            "conflict_rules": list(self.conflict_rules),
            "emergency_rules": list(self.emergency_rules),
            "evidence_policy": list(self.evidence_policy),
        }

    def fingerprint(self) -> str:
        payload = json.dumps(
            self.canonical_material(),
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=False,
        ).encode("utf-8")

        return sha256(payload).hexdigest()

    def verify_fingerprint(self, expected: str) -> bool:
        return self.fingerprint() == expected


@dataclass(frozen=True, slots=True)
class AuthorizationRequest:
    actor_level: AuthorityLevel
    requested_scope: str
    action_risk: ActionRisk
    evidence_present: bool
    human_approval: bool = False
    reversible: bool = True


DEFAULT_AUTHORITY: Final[Authority] = Authority()


def get_authority() -> Authority:
    return DEFAULT_AUTHORITY


def compare_authority(
    first: AuthorityLevel,
    second: AuthorityLevel,
) -> int:
    """
    Return:
        -1 if first outranks second
         0 if equal
         1 if second outranks first
    """
    first_rank = AUTHORITY_RANK[first]
    second_rank = AUTHORITY_RANK[second]

    if first_rank < second_rank:
        return -1

    if first_rank > second_rank:
        return 1

    return 0


def authorize(request: AuthorizationRequest) -> bool:
    """
    Central authorization gate.

    This is deliberately conservative:
    unknown scopes, insufficient authority, missing required evidence,
    and high-risk actions without required approval are rejected.
    """

    authority = get_authority()

    if request.requested_scope not in authority.scopes:
        return False

    # Model, tool, and external actors cannot directly perform critical work.
    if request.action_risk == ActionRisk.CRITICAL:
        if not request.human_approval:
            return False

    if request.action_risk in {
        ActionRisk.HIGH,
        ActionRisk.CRITICAL,
    } and not request.evidence_present:
        return False

    if (
        request.actor_level
        in {
            AuthorityLevel.MODEL,
            AuthorityLevel.TOOL,
            AuthorityLevel.EXTERNAL_SOURCE,
        }
        and request.action_risk
        in {
            ActionRisk.HIGH,
            ActionRisk.CRITICAL,
        }
    ):
        return False

    # Repository modification requires at least Autonomous Developer level.
    if request.requested_scope == "repository.modify":
        if AUTHORITY_RANK[request.actor_level] > AUTHORITY_RANK[
            AuthorityLevel.AUTONOMOUS_DEVELOPER
        ]:
            return False

    # Brain execution requires at least Autonomous Developer authority.
    if request.requested_scope == "brain.execute":
        if AUTHORITY_RANK[request.actor_level] > AUTHORITY_RANK[
            AuthorityLevel.AUTONOMOUS_DEVELOPER
        ]:
            return False

    # Recovery execution requires high authority.
    if request.requested_scope == "recovery.execute":
        if AUTHORITY_RANK[request.actor_level] > AUTHORITY_RANK[
            AuthorityLevel.AUTONOMOUS_DEVELOPER
        ]:
            return False

    # Non-reversible changes require stronger governance.
    if not request.reversible and not request.human_approval:
        return False

    return True


def validate_authority() -> None:
    authority = get_authority()

    if authority.project_id != PROJECT_ID:
        raise RuntimeError("Authority project ID invariant violated")

    if authority.canonical_name != CANONICAL_NAME:
        raise RuntimeError("Authority canonical name invariant violated")

    if authority.authority_version != AUTHORITY_VERSION:
        raise RuntimeError("Authority version invariant violated")

    if authority.root_authority != AuthorityLevel.HUMAN_OWNER:
        raise RuntimeError("Human owner must remain root authority")

    if authority.precedence != tuple(
        sorted(
            authority.precedence,
            key=lambda item: AUTHORITY_RANK[item],
        )
    ):
        raise RuntimeError("Authority precedence ordering drift detected")

    if set(AUTHORITY_RANK) != set(AuthorityLevel):
        raise RuntimeError("Authority rank table is incomplete")

    if not authority.invariants:
        raise RuntimeError("Authority invariants are missing")

    if not authority.scopes:
        raise RuntimeError("Authority scopes are missing")

    if not authority.delegation_rules:
        raise RuntimeError("Delegation rules are missing")

    if not authority.escalation_rules:
        raise RuntimeError("Escalation rules are missing")

    if not authority.conflict_rules:
        raise RuntimeError("Conflict rules are missing")

    if not authority.emergency_rules:
        raise RuntimeError("Emergency rules are missing")

    if not authority.evidence_policy:
        raise RuntimeError("Evidence policy is missing")

    if not authority.fingerprint():
        raise RuntimeError("Authority fingerprint generation failed")


def self_test() -> dict[str, object]:
    validate_authority()

    authority = get_authority()
    fingerprint = authority.fingerprint()

    read_request = AuthorizationRequest(
        actor_level=AuthorityLevel.AGENT,
        requested_scope="brain.read",
        action_risk=ActionRisk.READ,
        evidence_present=True,
    )

    safe_write = AuthorizationRequest(
        actor_level=AuthorityLevel.AUTONOMOUS_DEVELOPER,
        requested_scope="repository.modify",
        action_risk=ActionRisk.MODERATE,
        evidence_present=True,
        reversible=True,
    )

    unsafe_model_write = AuthorizationRequest(
        actor_level=AuthorityLevel.MODEL,
        requested_scope="repository.modify",
        action_risk=ActionRisk.HIGH,
        evidence_present=True,
        reversible=True,
    )

    critical_without_approval = AuthorizationRequest(
        actor_level=AuthorityLevel.AUTONOMOUS_DEVELOPER,
        requested_scope="brain.execute",
        action_risk=ActionRisk.CRITICAL,
        evidence_present=True,
        human_approval=False,
        reversible=False,
    )

    checks = {
        "project_binding": authority.project_id == PROJECT_ID,
        "human_root_authority": (
            authority.root_authority == AuthorityLevel.HUMAN_OWNER
        ),
        "precedence_order": (
            authority.precedence
            == tuple(
                sorted(
                    authority.precedence,
                    key=lambda item: AUTHORITY_RANK[item],
                )
            )
        ),
        "fingerprint_stable": authority.verify_fingerprint(fingerprint),
        "safe_read_allowed": authorize(read_request),
        "authorized_write_allowed": authorize(safe_write),
        "unsafe_model_write_blocked": not authorize(
            unsafe_model_write
        ),
        "critical_without_approval_blocked": not authorize(
            critical_without_approval
        ),
        "delegation_rules_present": bool(authority.delegation_rules),
        "escalation_rules_present": bool(authority.escalation_rules),
        "conflict_rules_present": bool(authority.conflict_rules),
        "emergency_rules_present": bool(authority.emergency_rules),
        "evidence_policy_present": bool(authority.evidence_policy),
    }

    passed = all(checks.values())

    return {
        "status": "PASS" if passed else "FAIL",
        "project_id": PROJECT_ID,
        "authority_version": AUTHORITY_VERSION,
        "fingerprint": fingerprint,
        "checks": checks,
    }


if __name__ == "__main__":
    result = self_test()

    print(
        f"{CANONICAL_NAME} Project Authority "
        f"v{AUTHORITY_VERSION}: {result['status']}"
    )
    print(f"Project ID       : {PROJECT_ID}")
    print(f"Root Authority   : {DEFAULT_AUTHORITY.root_authority.value}")
    print(f"Scopes           : {len(DEFAULT_AUTHORITY.scopes)}")
    print(f"Invariants       : {len(DEFAULT_AUTHORITY.invariants)}")
    print(f"Delegation Rules : {len(DEFAULT_AUTHORITY.delegation_rules)}")
    print(f"Escalation Rules : {len(DEFAULT_AUTHORITY.escalation_rules)}")
    print(f"Conflict Rules   : {len(DEFAULT_AUTHORITY.conflict_rules)}")
    print(f"Emergency Rules  : {len(DEFAULT_AUTHORITY.emergency_rules)}")
    print(f"Fingerprint      : {result['fingerprint']}")

    if result["status"] != "PASS":
        raise SystemExit(1)
