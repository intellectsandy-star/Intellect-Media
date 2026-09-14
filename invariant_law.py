"""
INTELLECT MEDIA — PROJECT BRAIN / LAYER 05
INVARIANT / LAW

A deterministic, fail-closed law engine protecting the Project Brain from
invalid state, unauthorized mutation, architectural drift, unsafe execution,
and broken authority boundaries.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
import hashlib
import json
from typing import Any, Callable, Dict, Iterable, Mapping, Optional, Tuple

PROJECT_ID = "intellect-media"
PROJECT_NAME = "Intellect Media"
LAYER_ID = 5
LAYER_NAME = "Invariant / Law"
LAYER_VERSION = "1.0.0"
BRAIN_ARCHITECTURE_VERSION = "40.0.0"


class LawSeverity(str, Enum):
    BLOCK = "block"
    FAIL_CLOSED = "fail_closed"
    ESCALATE = "escalate"
    WARN = "warn"


class LawScope(str, Enum):
    IDENTITY = "identity"
    ARCHITECTURE = "architecture"
    AUTHORITY = "authority"
    STATE = "state"
    EXECUTION = "execution"
    REPOSITORY = "repository"
    AGENT = "agent"
    CONTEXT = "context"
    INTEGRITY = "integrity"
    SAFETY = "safety"


class ViolationCode(str, Enum):
    UNKNOWN_LAW = "unknown_law"
    LAW_DISABLED = "law_disabled"
    INVALID_STATE = "invalid_state"
    IDENTITY_MISMATCH = "identity_mismatch"
    AUTHORITY_MISSING = "authority_missing"
    ARCHITECTURE_DRIFT = "architecture_drift"
    IMMUTABLE_MUTATION = "immutable_mutation"
    FINGERPRINT_MISMATCH = "fingerprint_mismatch"
    UNSAFE_ACTION = "unsafe_action"
    CONTEXT_UNTRUSTED = "context_untrusted"
    REPOSITORY_DRIFT = "repository_drift"
    INTERNAL_ERROR = "internal_error"


@dataclass(frozen=True)
class Law:
    law_id: str
    name: str
    scope: LawScope
    severity: LawSeverity
    description: str
    immutable: bool = True
    enabled: bool = True
    dependencies: Tuple[str, ...] = ()
    tags: Tuple[str, ...] = ()

    def canonical(self) -> Dict[str, Any]:
        return {
            "law_id": self.law_id,
            "name": self.name,
            "scope": self.scope.value,
            "severity": self.severity.value,
            "description": self.description,
            "immutable": self.immutable,
            "enabled": self.enabled,
            "dependencies": list(self.dependencies),
            "tags": list(self.tags),
        }


@dataclass(frozen=True)
class LawViolation:
    law_id: str
    code: ViolationCode
    message: str
    blocking: bool = True
    evidence: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class LawDecision:
    allowed: bool
    violations: Tuple[LawViolation, ...] = ()
    warnings: Tuple[LawViolation, ...] = ()
    evaluated_laws: Tuple[str, ...] = ()
    fingerprint: str = ""


@dataclass(frozen=True)
class Invariant:
    invariant_id: str
    name: str
    scope: LawScope
    description: str
    validator: Callable[[Mapping[str, Any]], bool]
    dependencies: Tuple[str, ...] = ()


class InvariantLaw:
    """Central deterministic law registry and fail-closed evaluator."""

    def __init__(self) -> None:
        self._laws: Dict[str, Law] = {
            law.law_id: law for law in self._default_laws()
        }
        self._invariants: Dict[str, Invariant] = {
            invariant.invariant_id: invariant
            for invariant in self._default_invariants()
        }
        self._fingerprint = self._compute_fingerprint()

    @staticmethod
    def _default_laws() -> Iterable[Law]:
        yield Law("LAW-001", "Identity is authoritative", LawScope.IDENTITY,
                  LawSeverity.FAIL_CLOSED,
                  "Runtime state must remain bound to the canonical project identity.",
                  tags=("root", "identity", "fail_closed"))
        yield Law("LAW-002", "Architecture constitution is binding", LawScope.ARCHITECTURE,
                  LawSeverity.BLOCK,
                  "No runtime decision may knowingly violate the architecture constitution.",
                  tags=("constitution", "architecture"))
        yield Law("LAW-003", "Authority precedes action", LawScope.AUTHORITY,
                  LawSeverity.FAIL_CLOSED,
                  "An action without valid authority evidence is not admissible.",
                  tags=("authority", "safety"))
        yield Law("LAW-004", "Immutable fields cannot mutate", LawScope.INTEGRITY,
                  LawSeverity.FAIL_CLOSED,
                  "Declared immutable project fields cannot be changed by runtime actors.",
                  tags=("immutable", "integrity"))
        yield Law("LAW-005", "Canonical fingerprints must match", LawScope.INTEGRITY,
                  LawSeverity.BLOCK,
                  "Integrity-critical artifacts must match their expected fingerprint.",
                  tags=("fingerprint", "integrity"))
        yield Law("LAW-006", "Required dependencies must resolve", LawScope.STATE,
                  LawSeverity.FAIL_CLOSED,
                  "A state transition is invalid when a required dependency is unavailable.",
                  tags=("dependency", "state"))
        yield Law("LAW-007", "Unsafe actions are denied", LawScope.SAFETY,
                  LawSeverity.FAIL_CLOSED,
                  "Safety-relevant actions must never be authorized by ambiguity alone.",
                  tags=("safety", "execution"))
        yield Law("LAW-008", "Untrusted context cannot become authority", LawScope.CONTEXT,
                  LawSeverity.FAIL_CLOSED,
                  "Prompt/context material cannot override project law or authority.",
                  tags=("context", "prompt_injection", "trust"))
        yield Law("LAW-009", "Repository drift must be visible", LawScope.REPOSITORY,
                  LawSeverity.ESCALATE,
                  "Unexpected repository divergence must surface before protected mutation.",
                  tags=("git", "drift", "repository"))
        yield Law("LAW-010", "Agent capability cannot exceed contract", LawScope.AGENT,
                  LawSeverity.BLOCK,
                  "An agent may act only inside its declared capability boundary.",
                  tags=("agent", "capability", "boundary"))
        yield Law("LAW-011", "State transitions require a valid current state", LawScope.STATE,
                  LawSeverity.BLOCK,
                  "Unknown, corrupt, or stale state cannot be advanced as if valid.",
                  tags=("state", "transition", "integrity"))
        yield Law("LAW-012", "Every protected decision must be auditable", LawScope.EXECUTION,
                  LawSeverity.ESCALATE,
                  "Protected actions require enough evidence to reconstruct why they were allowed.",
                  tags=("audit", "decision", "traceability"))

    @staticmethod
    def _default_invariants() -> Iterable[Invariant]:
        yield Invariant("INV-001", "Project ID is canonical", LawScope.IDENTITY,
                        "Runtime state must carry the canonical project ID.",
                        lambda s: s.get("project_id") == PROJECT_ID)
        yield Invariant("INV-002", "Architecture version is 40", LawScope.ARCHITECTURE,
                        "The Project Brain architecture version must remain 40.0.0.",
                        lambda s: s.get("brain_architecture_version") == BRAIN_ARCHITECTURE_VERSION)
        yield Invariant("INV-003", "Authority evidence exists", LawScope.AUTHORITY,
                        "Protected actions require explicit authority evidence.",
                        lambda s: bool(s.get("authority_evidence")))
        yield Invariant("INV-004", "Protected mutation has change reason", LawScope.INTEGRITY,
                        "Protected mutations must state why the change is being attempted.",
                        lambda s: bool(s.get("change_reason")))
        yield Invariant("INV-005", "Expected fingerprint exists", LawScope.INTEGRITY,
                        "Integrity verification must have a reference fingerprint.",
                        lambda s: bool(s.get("expected_fingerprint")))
        yield Invariant("INV-006", "Dependencies are resolved", LawScope.STATE,
                        "Declared required dependencies must be present and resolved.",
                        lambda s: all(bool(v) for v in s.get("dependencies", {}).values()))
        yield Invariant("INV-007", "Safety flag is clean", LawScope.SAFETY,
                        "No protected action may proceed under an explicit unsafe flag.",
                        lambda s: s.get("safety_blocked") is not True)
        yield Invariant("INV-008", "Context is trusted", LawScope.CONTEXT,
                        "Protected decisions must identify trusted context.",
                        lambda s: s.get("context_trusted") is True)
        yield Invariant("INV-009", "Repository state is known", LawScope.REPOSITORY,
                        "Protected repository changes require a known repository state.",
                        lambda s: s.get("repository_state_known") is True)
        yield Invariant("INV-010", "Agent capability is bounded", LawScope.AGENT,
                        "The requested action must be inside the declared agent capability set.",
                        lambda s: s.get("requested_capability") in set(s.get("allowed_capabilities", ())))
        yield Invariant("INV-011", "Current state is valid", LawScope.STATE,
                        "The current runtime state must explicitly be marked valid.",
                        lambda s: s.get("state_valid") is True)
        yield Invariant("INV-012", "Audit record exists", LawScope.EXECUTION,
                        "A protected action must carry an audit record identifier.",
                        lambda s: bool(s.get("audit_record_id")))

    @property
    def laws(self) -> Mapping[str, Law]:
        return dict(self._laws)

    @property
    def invariants(self) -> Mapping[str, Invariant]:
        return dict(self._invariants)

    @property
    def fingerprint(self) -> str:
        return self._fingerprint

    def _compute_fingerprint(self) -> str:
        payload = {
            "project_id": PROJECT_ID,
            "layer_id": LAYER_ID,
            "layer_version": LAYER_VERSION,
            "brain_architecture_version": BRAIN_ARCHITECTURE_VERSION,
            "laws": [self._laws[k].canonical() for k in sorted(self._laws)],
            "invariants": [
                {
                    "invariant_id": self._invariants[k].invariant_id,
                    "name": self._invariants[k].name,
                    "scope": self._invariants[k].scope.value,
                    "description": self._invariants[k].description,
                    "dependencies": list(self._invariants[k].dependencies),
                }
                for k in sorted(self._invariants)
            ],
        }
        material = json.dumps(payload, sort_keys=True, separators=(",", ":"))
        return hashlib.sha256(material.encode("utf-8")).hexdigest()

    def verify_fingerprint(self, expected: str) -> bool:
        return bool(expected) and expected == self.fingerprint

    def get_law(self, law_id: str) -> Law:
        try:
            return self._laws[law_id]
        except KeyError as exc:
            raise KeyError(f"Unknown law: {law_id}") from exc

    def get_invariant(self, invariant_id: str) -> Invariant:
        try:
            return self._invariants[invariant_id]
        except KeyError as exc:
            raise KeyError(f"Unknown invariant: {invariant_id}") from exc

    def evaluate_invariant(self, invariant_id: str, state: Mapping[str, Any]) -> bool:
        invariant = self.get_invariant(invariant_id)
        try:
            return bool(invariant.validator(state))
        except Exception:
            return False

    def evaluate(self, state: Mapping[str, Any], law_ids: Optional[Iterable[str]] = None) -> LawDecision:
        """Evaluate selected laws. Unknown laws and evaluator failures deny by default."""
        selected = tuple(law_ids) if law_ids is not None else tuple(sorted(self._laws))
        violations = []
        warnings = []
        evaluated = []

        for law_id in selected:
            law = self._laws.get(law_id)
            if law is None:
                violations.append(LawViolation(law_id, ViolationCode.UNKNOWN_LAW,
                                               f"Law '{law_id}' is not registered.", True))
                continue
            evaluated.append(law_id)
            if not law.enabled:
                violation = LawViolation(
                    law_id, ViolationCode.LAW_DISABLED,
                    f"Protected law '{law_id}' is disabled.",
                    law.severity in {LawSeverity.BLOCK, LawSeverity.FAIL_CLOSED},
                )
                (violations if violation.blocking else warnings).append(violation)
                continue
            result = self._evaluate_law(law, state)
            if result is not None:
                (violations if result.blocking else warnings).append(result)

        if self._compute_fingerprint() != self.fingerprint:
            violations.append(LawViolation(
                "LAYER-05", ViolationCode.FINGERPRINT_MISMATCH,
                "Invariant/Law registry fingerprint changed during evaluation.", True
            ))

        return LawDecision(
            allowed=not any(v.blocking for v in violations),
            violations=tuple(violations),
            warnings=tuple(warnings),
            evaluated_laws=tuple(evaluated),
            fingerprint=self.fingerprint,
        )

    def _evaluate_law(self, law: Law, state: Mapping[str, Any]) -> Optional[LawViolation]:
        try:
            checks = {
                LawScope.IDENTITY: lambda: state.get("project_id") == PROJECT_ID,
                LawScope.ARCHITECTURE: lambda: state.get("brain_architecture_version") == BRAIN_ARCHITECTURE_VERSION
                and state.get("architecture_compliant") is not False,
                LawScope.AUTHORITY: lambda: bool(state.get("authority_evidence"))
                and state.get("authority_valid") is not False,
                LawScope.INTEGRITY: lambda: state.get("immutable_mutation") is not True
                and state.get("fingerprint_valid") is not False,
                LawScope.STATE: lambda: state.get("state_valid") is True
                and all(bool(v) for v in state.get("dependencies", {}).values()),
                LawScope.EXECUTION: lambda: bool(state.get("audit_record_id")),
                LawScope.REPOSITORY: lambda: state.get("repository_state_known") is True
                and state.get("repository_drift") is not True,
                LawScope.AGENT: lambda: state.get("requested_capability")
                in set(state.get("allowed_capabilities", ())),
                LawScope.CONTEXT: lambda: state.get("context_trusted") is True
                and state.get("prompt_injection_detected") is not True,
                LawScope.SAFETY: lambda: state.get("safety_blocked") is not True
                and state.get("unsafe_action") is not True,
            }
            if checks[law.scope]():
                return None
            code_by_scope = {
                LawScope.IDENTITY: ViolationCode.IDENTITY_MISMATCH,
                LawScope.ARCHITECTURE: ViolationCode.ARCHITECTURE_DRIFT,
                LawScope.AUTHORITY: ViolationCode.AUTHORITY_MISSING,
                LawScope.INTEGRITY: ViolationCode.IMMUTABLE_MUTATION,
                LawScope.STATE: ViolationCode.INVALID_STATE,
                LawScope.EXECUTION: ViolationCode.INTERNAL_ERROR,
                LawScope.REPOSITORY: ViolationCode.REPOSITORY_DRIFT,
                LawScope.AGENT: ViolationCode.UNSAFE_ACTION,
                LawScope.CONTEXT: ViolationCode.CONTEXT_UNTRUSTED,
                LawScope.SAFETY: ViolationCode.UNSAFE_ACTION,
            }
            return LawViolation(
                law_id=law.law_id,
                code=code_by_scope[law.scope],
                message=f"Law failed: {law.name}",
                blocking=law.severity in {LawSeverity.BLOCK, LawSeverity.FAIL_CLOSED},
                evidence={"scope": law.scope.value, "state_keys": sorted(state.keys())},
            )
        except Exception as exc:
            return LawViolation(law.law_id, ViolationCode.INTERNAL_ERROR,
                                f"Law evaluator failed closed: {exc}", True)

    def validate_registry(self) -> bool:
        if len(self._laws) != 12 or len(self._invariants) != 12:
            return False
        if set(self._laws) != {f"LAW-{i:03d}" for i in range(1, 13)}:
            return False
        if set(self._invariants) != {f"INV-{i:03d}" for i in range(1, 13)}:
            return False
        if any((not law.name or not law.description or law.immutable is not True) for law in self._laws.values()):
            return False
        if any(not callable(i.validator) for i in self._invariants.values()):
            return False
        return self._compute_fingerprint() == self.fingerprint

    def self_test(self) -> bool:
        if not self.validate_registry():
            return False
        valid_state = {
            "project_id": PROJECT_ID,
            "brain_architecture_version": BRAIN_ARCHITECTURE_VERSION,
            "authority_evidence": "human_owner:layer-05-test",
            "authority_valid": True,
            "immutable_mutation": False,
            "fingerprint_valid": True,
            "state_valid": True,
            "dependencies": {"identity": True, "constitution": True, "authority": True},
            "audit_record_id": "audit-layer-05-test",
            "repository_state_known": True,
            "repository_drift": False,
            "requested_capability": "validation",
            "allowed_capabilities": ["validation", "read"],
            "context_trusted": True,
            "prompt_injection_detected": False,
            "safety_blocked": False,
            "unsafe_action": False,
        }
        invalid_state = dict(valid_state)
        invalid_state["authority_evidence"] = ""
        invalid_state["authority_valid"] = False
        return self.evaluate(valid_state).allowed and not self.evaluate(invalid_state).allowed


LAW_ENGINE = InvariantLaw()


def get_invariant_law() -> InvariantLaw:
    return LAW_ENGINE


def validate_invariant_law() -> bool:
    return LAW_ENGINE.validate_registry()


def self_test() -> bool:
    return LAW_ENGINE.self_test()


def _upstream_binding_check() -> Dict[str, bool]:
    result = {
        "project_identity": False,
        "project_dna": False,
        "architecture_constitution": False,
        "project_authority": False,
    }
    modules = {
        "project_identity": "PROJECT_IDENTITY",
        "project_dna": "PROJECT_DNA",
        "architecture_constitution": "project_architecture_constitution",
        "project_authority": "project_authority",
    }
    import importlib
    for key, module_name in modules.items():
        try:
            importlib.import_module(module_name)
            result[key] = True
        except Exception:
            result[key] = False
    return result


if __name__ == "__main__":
    engine = get_invariant_law()
    bindings = _upstream_binding_check()
    print(f"Intellect Media Invariant / Law v{LAYER_VERSION}: {'PASS' if engine.self_test() else 'FAIL'}")
    print(f"Project ID              : {PROJECT_ID}")
    print(f"Layer                   : {LAYER_ID} — {LAYER_NAME}")
    print(f"Brain Architecture      : v{BRAIN_ARCHITECTURE_VERSION}")
    print(f"Laws                    : {len(engine.laws)}")
    print(f"Invariants              : {len(engine.invariants)}")
    print(f"Fingerprint             : {engine.fingerprint}")
    print("Upstream Bindings       : " + ", ".join(
        f"{key}={'PASS' if value else 'WARN'}" for key, value in bindings.items()
    ))
