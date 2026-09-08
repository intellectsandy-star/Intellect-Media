"""
INTELLECT MEDIA — ARCHITECTURE CONSTITUTION
Layer 03 of the canonical 40-layer Project Brain.

Architecture Constitution defines what architecture is officially allowed
to exist inside Intellect Media, how architectural changes are controlled,
and how architectural integrity is protected from drift.

Project Identity defines WHO the project is.
Project DNA defines WHY the project exists.
Architecture Constitution defines WHAT STRUCTURE the system is allowed to have.
"""

from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
import json
from typing import Final


PROJECT_ID: Final[str] = "intellect-media"
CANONICAL_NAME: Final[str] = "Intellect Media"

CONSTITUTION_VERSION: Final[str] = "1.0.0"

BRAIN_ARCHITECTURE_VERSION: Final[str] = "40.0.0"

PRODUCT_CAPABILITY_COUNT: Final[int] = 15


@dataclass(frozen=True, slots=True)
class ArchitectureConstitution:
    project_id: str = PROJECT_ID
    canonical_name: str = CANONICAL_NAME
    constitution_version: str = CONSTITUTION_VERSION

    # Canonical architecture source.
    canonical_brain_source: str = "PROJECT_BRAIN.py"

    # Canonical identity source.
    canonical_identity_source: str = "PROJECT_IDENTITY.py"

    # Canonical DNA source.
    canonical_dna_source: str = "PROJECT_DNA.py"

    # Architecture model.
    brain_architecture_version: str = BRAIN_ARCHITECTURE_VERSION
    brain_layer_count: int = 40

    # Product roadmap is deliberately a separate namespace.
    product_capability_count: int = PRODUCT_CAPABILITY_COUNT

    # Structural rules.
    architecture_rules: tuple[str, ...] = (
        "Project Brain is the canonical governing architecture.",
        "Project Brain contains exactly 40 canonical layers.",
        "Layer numbering must remain sequential from 1 through 40.",
        "Each canonical layer must have one authoritative architectural definition.",
        "A layer implementation must not silently redefine another layer.",
        "Project Identity, Project DNA, and Architecture Constitution are foundational authority layers.",
        "Runtime implementation must remain subordinate to the canonical architecture.",
        "Autonomous Developer implementation must not redefine Brain architecture.",
        "Product capabilities must remain separate from Brain architecture.",
        "Architecture changes require explicit authority and versioned lineage.",
        "Deprecated architecture must never silently remain canonical.",
        "Temporary bootstrap tooling must never become hidden canonical architecture.",
    )

    # Layer authority order.
    authority_order: tuple[str, ...] = (
        "Project Identity",
        "Project DNA",
        "Architecture Constitution",
        "Authority",
        "Invariant / Law",
        "Project Brain State",
        "Autonomous Developer",
        "Agents / Models / Tools",
        "Execution Results",
    )

    # Admissibility rules for new components.
    admissibility_rules: tuple[str, ...] = (
        "Every new canonical component must have a unique responsibility.",
        "Every new component must identify its authority source.",
        "Every new component must have a defined dependency boundary.",
        "Every new component must identify its persistence requirements.",
        "Every state-changing component must support verification.",
        "Every critical component must support deterministic integrity checking.",
        "No component may introduce a competing source of truth.",
        "No component may bypass higher-order authority.",
        "No component may silently mutate immutable architectural rules.",
        "No component may claim completion without verification.",
    )

    # Dependency rules.
    dependency_rules: tuple[str, ...] = (
        "Dependencies must point toward authoritative or lower-level execution concerns.",
        "Circular authority dependencies are forbidden.",
        "Layer implementations may depend on lower layers only when explicitly permitted.",
        "Runtime modules must not become architectural authorities.",
        "External services are dependencies, not authorities.",
        "Model output is a proposal or evidence source unless explicitly verified.",
    )

    # Change-control rules.
    change_control_rules: tuple[str, ...] = (
        "Architecture changes require explicit authorization.",
        "Architecture changes must increment the architecture version when canonical structure changes.",
        "Architecture changes must preserve backward-readable lineage.",
        "Architecture changes must pass validation before becoming active.",
        "Architecture changes must record the reason for change.",
        "Architecture changes must identify affected layers and dependencies.",
        "Unsafe architectural changes must fail closed.",
    )

    # Compatibility rules.
    compatibility_rules: tuple[str, ...] = (
        "Existing canonical identity must remain compatible with the architecture.",
        "Existing Project DNA must remain compatible with the architecture.",
        "Layer identifiers must not be silently repurposed.",
        "Removed components require explicit deprecation state.",
        "Migration must be completed before destructive retirement of legacy components.",
        "Canonical state must remain reconstructable during migration.",
    )

    # Drift rules.
    drift_rules: tuple[str, ...] = (
        "Layer count drift must be detected.",
        "Layer numbering drift must be detected.",
        "Layer naming drift must be detected.",
        "Domain ordering drift must be detected.",
        "Canonical source drift must be detected.",
        "Authority-order drift must be detected.",
        "Unauthorized architecture fingerprints must be rejected.",
    )

    def canonical_material(self) -> dict[str, object]:
        return {
            "project_id": self.project_id,
            "canonical_name": self.canonical_name,
            "constitution_version": self.constitution_version,
            "canonical_brain_source": self.canonical_brain_source,
            "canonical_identity_source": self.canonical_identity_source,
            "canonical_dna_source": self.canonical_dna_source,
            "brain_architecture_version": self.brain_architecture_version,
            "brain_layer_count": self.brain_layer_count,
            "product_capability_count": self.product_capability_count,
            "architecture_rules": list(self.architecture_rules),
            "authority_order": list(self.authority_order),
            "admissibility_rules": list(self.admissibility_rules),
            "dependency_rules": list(self.dependency_rules),
            "change_control_rules": list(self.change_control_rules),
            "compatibility_rules": list(self.compatibility_rules),
            "drift_rules": list(self.drift_rules),
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


DEFAULT_CONSTITUTION: Final[ArchitectureConstitution] = (
    ArchitectureConstitution()
)


def get_architecture_constitution() -> ArchitectureConstitution:
    return DEFAULT_CONSTITUTION


def validate_architecture_constitution() -> None:
    constitution = DEFAULT_CONSTITUTION

    if constitution.project_id != PROJECT_ID:
        raise RuntimeError(
            "Architecture Constitution project ID invariant violated"
        )

    if constitution.canonical_name != CANONICAL_NAME:
        raise RuntimeError(
            "Architecture Constitution canonical name invariant violated"
        )

    if constitution.constitution_version != CONSTITUTION_VERSION:
        raise RuntimeError(
            "Architecture Constitution version invariant violated"
        )

    if constitution.canonical_brain_source != "PROJECT_BRAIN.py":
        raise RuntimeError(
            "Canonical Brain source invariant violated"
        )

    if constitution.canonical_identity_source != "PROJECT_IDENTITY.py":
        raise RuntimeError(
            "Canonical Identity source invariant violated"
        )

    if constitution.canonical_dna_source != "PROJECT_DNA.py":
        raise RuntimeError(
            "Canonical DNA source invariant violated"
        )

    if constitution.brain_architecture_version != BRAIN_ARCHITECTURE_VERSION:
        raise RuntimeError(
            "Brain architecture version mismatch"
        )

    if constitution.brain_layer_count != 40:
        raise RuntimeError(
            "Canonical Brain layer count must remain 40"
        )

    if constitution.product_capability_count != 15:
        raise RuntimeError(
            "Product capability namespace must remain 15"
        )

    required_collections = {
        "architecture_rules": constitution.architecture_rules,
        "authority_order": constitution.authority_order,
        "admissibility_rules": constitution.admissibility_rules,
        "dependency_rules": constitution.dependency_rules,
        "change_control_rules": constitution.change_control_rules,
        "compatibility_rules": constitution.compatibility_rules,
        "drift_rules": constitution.drift_rules,
    }

    for field_name, values in required_collections.items():
        if not values:
            raise RuntimeError(
                f"Architecture Constitution {field_name} is missing"
            )

    if not constitution.fingerprint():
        raise RuntimeError(
            "Architecture Constitution fingerprint generation failed"
        )


def self_test() -> dict[str, object]:
    """Run deterministic Architecture Constitution integrity checks."""
    constitution = get_architecture_constitution()

    validate_architecture_constitution()

    fingerprint = constitution.fingerprint()

    checks = {
        "project_binding": (
            constitution.project_id == PROJECT_ID
        ),
        "canonical_name": (
            constitution.canonical_name == CANONICAL_NAME
        ),
        "brain_source": (
            constitution.canonical_brain_source == "PROJECT_BRAIN.py"
        ),
        "identity_source": (
            constitution.canonical_identity_source == "PROJECT_IDENTITY.py"
        ),
        "dna_source": (
            constitution.canonical_dna_source == "PROJECT_DNA.py"
        ),
        "brain_version": (
            constitution.brain_architecture_version
            == BRAIN_ARCHITECTURE_VERSION
        ),
        "brain_layer_count": (
            constitution.brain_layer_count == 40
        ),
        "product_capability_count": (
            constitution.product_capability_count == 15
        ),
        "architecture_rules": bool(
            constitution.architecture_rules
        ),
        "authority_order": bool(
            constitution.authority_order
        ),
        "admissibility_rules": bool(
            constitution.admissibility_rules
        ),
        "dependency_rules": bool(
            constitution.dependency_rules
        ),
        "change_control_rules": bool(
            constitution.change_control_rules
        ),
        "compatibility_rules": bool(
            constitution.compatibility_rules
        ),
        "drift_rules": bool(
            constitution.drift_rules
        ),
        "fingerprint_stable": (
            constitution.verify_fingerprint(fingerprint)
        ),
    }

    passed = all(checks.values())

    return {
        "status": "PASS" if passed else "FAIL",
        "project_id": PROJECT_ID,
        "constitution_version": CONSTITUTION_VERSION,
        "brain_architecture_version": BRAIN_ARCHITECTURE_VERSION,
        "brain_layer_count": constitution.brain_layer_count,
        "product_capability_count": constitution.product_capability_count,
        "fingerprint": fingerprint,
        "checks": checks,
    }


if __name__ == "__main__":
    result = self_test()

    print(
        f"{CANONICAL_NAME} Architecture Constitution "
        f"v{CONSTITUTION_VERSION}: {result['status']}"
    )
    print(f"Project ID              : {PROJECT_ID}")
    print(
        f"Brain Architecture      : "
        f"v{BRAIN_ARCHITECTURE_VERSION}"
    )
    print(
        f"Brain Layers            : "
        f"{result['brain_layer_count']}"
    )
    print(
        f"Product Capabilities    : "
        f"{result['product_capability_count']}"
    )
    print(f"Fingerprint             : {result['fingerprint']}")
    print(
        f"Architecture Rules      : "
        f"{len(DEFAULT_CONSTITUTION.architecture_rules)}"
    )
    print(
        f"Authority Rules         : "
        f"{len(DEFAULT_CONSTITUTION.authority_order)}"
    )
    print(
        f"Admissibility Rules     : "
        f"{len(DEFAULT_CONSTITUTION.admissibility_rules)}"
    )
    print(
        f"Dependency Rules        : "
        f"{len(DEFAULT_CONSTITUTION.dependency_rules)}"
    )
    print(
        f"Change-Control Rules    : "
        f"{len(DEFAULT_CONSTITUTION.change_control_rules)}"
    )
    print(
        f"Compatibility Rules     : "
        f"{len(DEFAULT_CONSTITUTION.compatibility_rules)}"
    )
    print(
        f"Drift Rules             : "
        f"{len(DEFAULT_CONSTITUTION.drift_rules)}"
    )

    if result["status"] != "PASS":
        raise SystemExit(1)
