"""
INTELLECT MEDIA — PROJECT BRAIN
Canonical 40-layer Project Brain architecture.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Final

ARCHITECTURE_VERSION: Final[str] = "40.0.0"
PROJECT_ID: Final[str] = "intellect-media"
CANONICAL_NAME: Final[str] = "Intellect Media"
SYSTEM_CLASS: Final[str] = "autonomous_development_system"


@dataclass(frozen=True, slots=True)
class BrainLayer:
    number: int
    name: str
    domain: str
    purpose: str


PROJECT_BRAIN_LAYERS: Final[tuple[BrainLayer, ...]] = (
    BrainLayer(1, "Project Identity", "identity_constitution", "Canonical project identity and root-of-trust anchor."),
    BrainLayer(2, "Project DNA", "identity_constitution", "Vision, purpose, boundaries and non-negotiable principles."),
    BrainLayer(3, "Architecture Constitution", "identity_constitution", "Approved architecture and admissibility rules."),
    BrainLayer(4, "Authority", "identity_constitution", "Defines authoritative state and conflict precedence."),
    BrainLayer(5, "Invariant / Law", "identity_constitution", "Immutable laws and safety invariants."),
    BrainLayer(6, "World State", "cognitive_state", "Current factual project state."),
    BrainLayer(7, "Goal State", "cognitive_state", "Ultimate, current and immediate objectives."),
    BrainLayer(8, "Work Graph", "cognitive_state", "Tasks, subtasks, dependencies, gates and progression."),
    BrainLayer(9, "Decision Memory", "cognitive_state", "Decisions plus reasons, evidence and consequences."),
    BrainLayer(10, "Knowledge Memory", "cognitive_state", "Permanent, temporary and learned project knowledge."),
    BrainLayer(11, "Artifact Intelligence", "cognitive_state", "Purpose, schema, ownership, version and lineage of artifacts."),
    BrainLayer(12, "Context Compiler", "context_intelligence", "Compiles minimum authoritative context for a task."),
    BrainLayer(13, "Context Priority", "context_intelligence", "Orders laws, state, dependencies, task and history."),
    BrainLayer(14, "Context Compression", "context_intelligence", "Compresses history into durable structured state."),
    BrainLayer(15, "Context Resurrection", "context_intelligence", "Reconstructs usable state for new sessions and actors."),
    BrainLayer(16, "Intent Interpreter", "autonomous_development", "Maps user intent to project-level change intent."),
    BrainLayer(17, "Planner / Decomposer", "autonomous_development", "Converts objectives into executable work graphs."),
    BrainLayer(18, "Execution Controller", "autonomous_development", "Authorizes which work may execute now."),
    BrainLayer(19, "Verification Engine", "autonomous_development", "Separates implementation from verified completion."),
    BrainLayer(20, "Quality Gate", "autonomous_development", "Blocks progression until required gates pass."),
    BrainLayer(21, "Execution Journal", "continuity_recovery", "Machine-readable record of meaningful actions."),
    BrainLayer(22, "Checkpoint Engine", "continuity_recovery", "Creates recoverable project snapshots."),
    BrainLayer(23, "State Fingerprint", "continuity_recovery", "Cryptographic identity of an exact project state."),
    BrainLayer(24, "Drift Detection", "continuity_recovery", "Detects architectural, state and repository divergence."),
    BrainLayer(25, "Recovery / Fail-Closed", "continuity_recovery", "Stops unsafe progress and reconstructs known-good state."),
    BrainLayer(26, "Agent Registry", "multi_agent_continuity", "Registry of actors, roles and capabilities."),
    BrainLayer(27, "Capability Contract", "multi_agent_continuity", "Explicit permission boundaries for actors and tools."),
    BrainLayer(28, "Handoff Protocol", "multi_agent_continuity", "Structured state transfer across sessions and actors."),
    BrainLayer(29, "Conflict Arbitration", "multi_agent_continuity", "Resolves incompatible proposals using authority and evidence."),
    BrainLayer(30, "Repository State Map", "repository_intelligence", "Maps logical architecture to physical repository artifacts."),
    BrainLayer(31, "Change Lineage", "repository_intelligence", "Links changes to task, decision, actor and checkpoint."),
    BrainLayer(32, "Git/GitHub Reconciliation", "repository_intelligence", "Detects and safely reconciles repository divergence."),
    BrainLayer(33, "Output Trust & Hallucination Guard", "gpt_reliability", "Classifies model output and prevents unsupported claims becoming truth."),
    BrainLayer(34, "Reasoning & Decision Validation", "gpt_reliability", "Validates model conclusions against constraints and evidence."),
    BrainLayer(35, "Context Integrity & Memory Guard", "gpt_reliability", "Protects reasoning from stale, lost or contaminated context."),
    BrainLayer(36, "Instruction / Prompt Injection Firewall", "gpt_reliability", "Treats external content as untrusted data, not authority."),
    BrainLayer(37, "Agency & Action Safety", "gpt_reliability", "Controls high-impact tool actions through capability and authority gates."),
    BrainLayer(38, "Behavioral Drift & Model Change", "gpt_reliability", "Tracks model, prompt, tool and behavior changes with regression checks."),
    BrainLayer(39, "Failure Classification & Adaptive Recovery", "gpt_reliability", "Classifies failures and selects evidence-driven recovery paths."),
    BrainLayer(40, "Output Audit / Reproducibility / Trust Ledger", "gpt_reliability", "Preserves provenance from model output to verified project state."),
)

DOMAIN_ORDER: Final[tuple[str, ...]] = (
    "identity_constitution",
    "cognitive_state",
    "context_intelligence",
    "autonomous_development",
    "continuity_recovery",
    "multi_agent_continuity",
    "repository_intelligence",
    "gpt_reliability",
)

CANONICAL_AUTHORITY_FLOW: Final[tuple[str, ...]] = (
    "Project Identity / Constitution",
    "Project Brain",
    "Autonomous Developer",
    "GPT / Agents / Tools",
    "Verification",
    "Quality Gate",
    "Checkpoint",
    "Authorized State",
)


def get_layer(number: int) -> BrainLayer:
    if not 1 <= number <= 40:
        raise ValueError(f"Project Brain layer must be 1..40, got {number!r}")
    return PROJECT_BRAIN_LAYERS[number - 1]


def validate_architecture() -> None:
    numbers = tuple(layer.number for layer in PROJECT_BRAIN_LAYERS)
    if numbers != tuple(range(1, 41)):
        raise RuntimeError("Project Brain numbering drift detected")
    domains = tuple(dict.fromkeys(layer.domain for layer in PROJECT_BRAIN_LAYERS))
    if domains != DOMAIN_ORDER:
        raise RuntimeError("Project Brain domain ordering drift detected")


if __name__ == "__main__":
    validate_architecture()
    print(f"{CANONICAL_NAME} Project Brain v{ARCHITECTURE_VERSION}: 40 layers — VALID")
