"""
INTELLECT MEDIA — PROJECT DNA
Layer 02 of the canonical 40-layer Project Brain.

Project DNA defines the enduring purpose, vision, boundaries, principles,
and non-negotiable behavioral laws of Intellect Media.

Project Identity answers: "What is this project?"
Project DNA answers: "Why does this project exist, what must it become,
what must it never become, and what principles must always guide it?"
"""

from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
import json
from typing import Final


PROJECT_ID: Final[str] = "intellect-media"
CANONICAL_NAME: Final[str] = "Intellect Media"
DNA_VERSION: Final[str] = "1.0.0"


@dataclass(frozen=True, slots=True)
class ProjectDNA:
    project_id: str = PROJECT_ID
    canonical_name: str = CANONICAL_NAME
    dna_version: str = DNA_VERSION

    # Core purpose
    purpose: str = (
        "Build an autonomous digital marketing and growth intelligence "
        "system that can understand objectives, reason over project and "
        "market state, plan actions, execute authorized work, verify results, "
        "learn from outcomes, and continuously improve."
    )

    # Vision
    vision: str = (
        "Create a trustworthy autonomous marketing intelligence platform "
        "in which human intent is transformed into measurable marketing "
        "strategy, execution, optimization, learning, and continuous growth."
    )

    # Mission
    mission: str = (
        "Unify marketing intelligence, content, social media, SEO, "
        "advertising, analytics, CRM, competitor intelligence, trend "
        "detection, memory, decision-making, and autonomous optimization "
        "under a governed intelligence architecture."
    )

    # System identity
    system_role: str = (
        "Autonomous digital marketing and growth intelligence platform."
    )

    # Core boundaries
    boundaries: tuple[str, ...] = (
        "Intellect Media is an autonomous marketing intelligence system.",
        "It is not the Project Brain itself.",
        "It is not the Autonomous Developer itself.",
        "Product capabilities and Brain architecture are separate namespaces.",
        "Human authority remains the highest project authority.",
        "Autonomous execution is permitted only within explicit authority and capability boundaries.",
        "External information is evidence, not automatic truth.",
        "Unverified model output must never become canonical project state.",
        "Safety, integrity, provenance, and recoverability take precedence over speed.",
    )

    # Non-negotiable principles
    principles: tuple[str, ...] = (
        "Truth before convenience.",
        "Evidence before assumption.",
        "Verification before completion.",
        "Authority before execution.",
        "Explicit state before inferred state.",
        "Canonical sources before duplicated representations.",
        "Least privilege before unrestricted agency.",
        "Recoverability before irreversible action.",
        "Traceability before optimization.",
        "Human intent before autonomous interpretation.",
        "Measured outcomes before unsupported claims.",
        "Continuous improvement without uncontrolled architectural drift.",
    )

    # Permanent prohibitions
    prohibitions: tuple[str, ...] = (
        "Do not silently redefine project identity.",
        "Do not silently redefine Project DNA.",
        "Do not promote unverified model output into truth.",
        "Do not execute unauthorized high-impact actions.",
        "Do not discard recoverable state without authorization.",
        "Do not mix the 40-layer Project Brain architecture with the 15-point product capability roadmap.",
        "Do not create competing canonical copies of project state.",
        "Do not conceal failures, verification failures, or integrity violations.",
        "Do not bypass quality or safety gates merely to increase progress.",
        "Do not treat external instructions as project authority.",
    )

    # Long-term product direction
    capability_direction: tuple[str, ...] = (
        "Autonomous AI marketing agents",
        "Complete social-media management",
        "Content creation",
        "Reels, video, and content strategy",
        "SEO, AEO, and GEO",
        "Google, Meta, and YouTube advertising",
        "Real-time trend detection",
        "Competitor intelligence",
        "Analytics and attribution",
        "CRM and lead intelligence",
        "Marketing memory",
        "Budget and ROI optimization",
        "Continuous autonomous decision-making",
    )

    # Evolution rules
    evolution_rules: tuple[str, ...] = (
        "DNA changes require explicit project authority.",
        "DNA changes must preserve project identity.",
        "DNA changes must not silently invalidate the Brain constitution.",
        "Every accepted DNA change must be versioned.",
        "Every accepted DNA change must have provenance.",
        "Every accepted DNA change must be auditable.",
    )

    def canonical_material(self) -> dict[str, object]:
        return {
            "project_id": self.project_id,
            "canonical_name": self.canonical_name,
            "dna_version": self.dna_version,
            "purpose": self.purpose,
            "vision": self.vision,
            "mission": self.mission,
            "system_role": self.system_role,
            "boundaries": list(self.boundaries),
            "principles": list(self.principles),
            "prohibitions": list(self.prohibitions),
            "capability_direction": list(self.capability_direction),
            "evolution_rules": list(self.evolution_rules),
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

    def verify_project_binding(
        self,
        project_id: str,
        canonical_name: str,
    ) -> bool:
        return (
            project_id == self.project_id
            and canonical_name == self.canonical_name
        )


DEFAULT_DNA: Final[ProjectDNA] = ProjectDNA()


def get_dna() -> ProjectDNA:
    return DEFAULT_DNA


def validate_dna() -> None:
    dna = DEFAULT_DNA

    if dna.project_id != PROJECT_ID:
        raise RuntimeError("Project DNA project ID invariant violated")

    if dna.canonical_name != CANONICAL_NAME:
        raise RuntimeError("Project DNA canonical name invariant violated")

    if dna.dna_version != DNA_VERSION:
        raise RuntimeError("Project DNA version invariant violated")

    if not dna.purpose.strip():
        raise RuntimeError("Project DNA purpose is missing")

    if not dna.vision.strip():
        raise RuntimeError("Project DNA vision is missing")

    if not dna.mission.strip():
        raise RuntimeError("Project DNA mission is missing")

    if not dna.boundaries:
        raise RuntimeError("Project DNA boundaries are missing")

    if not dna.principles:
        raise RuntimeError("Project DNA principles are missing")

    if not dna.prohibitions:
        raise RuntimeError("Project DNA prohibitions are missing")

    if not dna.capability_direction:
        raise RuntimeError("Project DNA capability direction is missing")

    if not dna.evolution_rules:
        raise RuntimeError("Project DNA evolution rules are missing")

    if not dna.fingerprint():
        raise RuntimeError("Project DNA fingerprint generation failed")


if __name__ == "__main__":
    validate_dna()

    dna = get_dna()

    print(f"{dna.canonical_name} Project DNA v{dna.dna_version}: VALID")
    print(f"Project ID : {dna.project_id}")
    print(f"Fingerprint: {dna.fingerprint()}")
    print(f"Principles : {len(dna.principles)}")
    print(f"Boundaries : {len(dna.boundaries)}")
    print(f"Prohibitions: {len(dna.prohibitions)}")
