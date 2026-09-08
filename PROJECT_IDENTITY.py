"""
INTELLECT MEDIA — PROJECT IDENTITY
Layer 01 of the canonical 40-layer Project Brain.

Identity is a root-of-trust object, not ordinary editable metadata.
No GPT, agent, developer, runtime or repository may silently redefine it.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from hashlib import sha256
import json
from typing import Any, Final, Mapping

PROJECT_ID: Final[str] = "intellect-media"
CANONICAL_NAME: Final[str] = "Intellect Media"
IDENTITY_VERSION: Final[str] = "1.0.0"
NAMESPACE_ROOT: Final[str] = "intellect-media"
SYSTEM_CLASS: Final[str] = "autonomous_development_system"

IMMUTABLE_FIELDS: Final[frozenset[str]] = frozenset({
    "project_id", "identity_root", "namespace_root", "origin_id"
})

CONTROLLED_FIELDS: Final[frozenset[str]] = frozenset({
    "canonical_name", "aliases", "system_class", "project_role",
    "mission_binding", "vision_binding", "ownership"
})


@dataclass(frozen=True, slots=True)
class ProjectIdentity:
    project_id: str = PROJECT_ID
    identity_root: str = "intellect-media:identity-root"
    canonical_name: str = CANONICAL_NAME
    aliases: tuple[str, ...] = ("IntellectMedia", "Intellect Media AI")
    system_class: str = SYSTEM_CLASS
    project_role: str = "Autonomous development system for Intellect Media"
    origin_id: str = "intellect-media:genesis"
    mission_binding: str = "intellect-media:mission"
    vision_binding: str = "intellect-media:vision"
    ownership: str = "project_identity"
    namespace_root: str = NAMESPACE_ROOT
    identity_version: str = IDENTITY_VERSION
    authority_root: str = "project_identity"
    immutable_fields: frozenset[str] = field(default_factory=lambda: IMMUTABLE_FIELDS)
    controlled_fields: frozenset[str] = field(default_factory=lambda: CONTROLLED_FIELDS)
    invariants: tuple[str, ...] = (
        "project_id cannot be silently changed",
        "identity_root cannot be silently changed",
        "namespace_root cannot be silently changed",
        "origin_id cannot be silently changed",
        "an actor must be bound before identity-scoped work is authorized",
        "identity fingerprint must match canonical identity material",
        "unknown identity transitions must fail closed",
        "repository binding must not silently replace project identity",
    )
    repository_binding: Mapping[str, str] = field(default_factory=lambda: {
        "repository": "intellectsandy-star/Intellect-Media",
        "default_branch": "main",
    })

    def canonical_material(self) -> dict[str, Any]:
        return {
            "project_id": self.project_id,
            "identity_root": self.identity_root,
            "canonical_name": self.canonical_name,
            "aliases": list(self.aliases),
            "system_class": self.system_class,
            "project_role": self.project_role,
            "origin_id": self.origin_id,
            "mission_binding": self.mission_binding,
            "vision_binding": self.vision_binding,
            "ownership": self.ownership,
            "namespace_root": self.namespace_root,
            "identity_version": self.identity_version,
            "authority_root": self.authority_root,
            "invariants": list(self.invariants),
            "repository_binding": dict(self.repository_binding),
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

    def verify_actor(self, actor_id: str, authority_scope: str) -> bool:
        return bool(actor_id.strip()) and authority_scope in {
            "identity.read", "identity.verify", "identity.propose_change"
        }

    def verify_project_binding(self, project_id: str, namespace_root: str) -> bool:
        return project_id == self.project_id and namespace_root == self.namespace_root

    def handshake(
        self,
        *,
        actor_id: str,
        project_id: str,
        identity_version: str,
        fingerprint: str,
        authority_scope: str,
    ) -> dict[str, Any]:
        project_match = self.verify_project_binding(project_id, self.namespace_root)
        version_match = identity_version == self.identity_version
        fingerprint_match = self.verify_fingerprint(fingerprint)
        actor_valid = self.verify_actor(actor_id, authority_scope)
        authorized = project_match and version_match and fingerprint_match and actor_valid
        return {
            "status": "AUTHORIZED" if authorized else "REJECTED",
            "actor_id": actor_id,
            "project_id": self.project_id,
            "identity_version": self.identity_version,
            "identity_fingerprint": self.fingerprint(),
            "project_match": project_match,
            "version_match": version_match,
            "fingerprint_match": fingerprint_match,
            "actor_valid": actor_valid,
        }


DEFAULT_IDENTITY: Final[ProjectIdentity] = ProjectIdentity()


def get_identity() -> ProjectIdentity:
    return DEFAULT_IDENTITY


def validate_identity() -> None:
    identity = DEFAULT_IDENTITY
    if identity.project_id != PROJECT_ID:
        raise RuntimeError("Project ID invariant violated")
    if identity.namespace_root != NAMESPACE_ROOT:
        raise RuntimeError("Namespace invariant violated")
    if identity.identity_version != IDENTITY_VERSION:
        raise RuntimeError("Identity version invariant violated")
    if not identity.fingerprint():
        raise RuntimeError("Identity fingerprint generation failed")


if __name__ == "__main__":
    validate_identity()
    identity = get_identity()
    print(f"{identity.canonical_name} Project Identity v{identity.identity_version}: VALID")
    print(f"Fingerprint: {identity.fingerprint()}")
