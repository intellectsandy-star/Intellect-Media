from __future__ import annotations

from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from pathlib import Path
import hashlib
import json
from typing import Optional


STATE_FILE = Path("runtime/project_brain.json")


def now():
    return datetime.now(timezone.utc).isoformat()


def fingerprint(data):
    raw = json.dumps(data, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


@dataclass
class Task:
    id: str
    title: str
    status: str = "backlog"
    priority: int = 50
    dependencies: list[str] = field(default_factory=list)
    verified: bool = False


@dataclass
class ProjectBrain:
    project_name: str = "Intellect Media"
    status: str = "foundation"
    architecture_version: str = "0.2.0"

    active_point: int = 0
    total_points: int = 15

    completed_points: list[int] = field(default_factory=list)
    locked_points: list[int] = field(default_factory=list)

    tasks: dict[str, Task] = field(default_factory=dict)
    decisions: list[dict] = field(default_factory=list)

    checkpoint_id: str = ""
    last_updated: str = field(default_factory=now)

    @property
    def progress_percent(self):
        if not self.tasks:
            return 0.0
        done = sum(
            task.status == "done" and task.verified
            for task in self.tasks.values()
        )
        return round(done / len(self.tasks) * 100, 2)

    def touch(self):
        self.last_updated = now()
        self.checkpoint_id = ""

    def add_task(self, task_id, title, priority=50, dependencies=None):
        if task_id in self.tasks:
            return
        self.tasks[task_id] = Task(
            id=task_id,
            title=title,
            priority=priority,
            dependencies=dependencies or [],
        )
        self.touch()

    def dependencies_done(self, task):
        return all(
            dep in self.tasks
            and self.tasks[dep].status == "done"
            and self.tasks[dep].verified
            for dep in task.dependencies
        )

    def next_task(self):
        ready = [
            t for t in self.tasks.values()
            if t.status in {"backlog", "ready"}
            and self.dependencies_done(t)
        ]
        if not ready:
            return None
        return max(ready, key=lambda x: x.priority)

    def set_active_point(self, point):
        if point == 0:
            self.active_point = 0
            self.status = "foundation"
            self.touch()
            return

        if not 1 <= point <= self.total_points:
            raise ValueError("Point must be between 1 and 15.")

        if self.active_point not in (0, point):
            raise ValueError(
                f"Point {self.active_point} is already active."
            )

        if point > 1:
            previous = point - 1
            if previous not in self.locked_points:
                raise ValueError(
                    f"Point {point} cannot start before Point {previous} is locked."
                )

        self.active_point = point
        self.status = "development"
        self.touch()

    def complete_task(self, task_id):
        task = self.tasks[task_id]
        if not self.dependencies_done(task):
            raise ValueError("Dependencies are incomplete.")
        task.status = "done"
        task.verified = True
        self.touch()

    def lock_point(self, point):
        if self.active_point != point:
            raise ValueError("Only the active point can be locked.")

        unfinished = [
            t.id for t in self.tasks.values()
            if t.status != "done" or not t.verified
        ]

        if unfinished:
            raise ValueError(
                f"Cannot lock point {point}; unfinished tasks: {unfinished}"
            )

        if point not in self.completed_points:
            self.completed_points.append(point)

        if point not in self.locked_points:
            self.locked_points.append(point)

        self.active_point = 0
        self.status = "ready_for_next_point"
        self.touch()

    def add_decision(self, title, rationale):
        self.decisions.append({
            "title": title,
            "rationale": rationale,
            "timestamp": now(),
        })
        self.touch()

    def snapshot(self, without_checkpoint=False):
        data = {
            "project_name": self.project_name,
            "status": self.status,
            "architecture_version": self.architecture_version,
            "active_point": self.active_point,
            "total_points": self.total_points,
            "completed_points": self.completed_points,
            "locked_points": self.locked_points,
            "tasks": {
                k: asdict(v) for k, v in self.tasks.items()
            },
            "decisions": self.decisions,
            "checkpoint_id": self.checkpoint_id,
            "last_updated": self.last_updated,
        }

        if without_checkpoint:
            data["checkpoint_id"] = ""

        data["progress_percent"] = self.progress_percent
        return data

    def checkpoint(self):
        identity = fingerprint(self.snapshot(without_checkpoint=True))
        self.checkpoint_id = identity[:16]
        self.save()
        return self.checkpoint_id

    def save(self):
        STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
        STATE_FILE.write_text(
            json.dumps(self.snapshot(), indent=2),
            encoding="utf-8",
        )

    @classmethod
    def load_or_create(cls):
        if not STATE_FILE.exists():
            brain = cls()
            brain.save()
            return brain

        raw = json.loads(
            STATE_FILE.read_text(encoding="utf-8")
        )

        tasks = {
            k: Task(**v)
            for k, v in raw.pop("tasks", {}).items()
        }

        raw.pop("progress_percent", None)

        return cls(
            tasks=tasks,
            **raw
        )


if __name__ == "__main__":
    brain = ProjectBrain.load_or_create()

    if not brain.tasks:
        brain.add_task(
            "foundation_state",
            "Canonical project state",
            100,
        )
        brain.add_task(
            "foundation_progress",
            "Automatic progress tracking",
            95,
            ["foundation_state"],
        )
        brain.add_task(
            "foundation_point_lock",
            "One active point enforcement",
            95,
            ["foundation_state"],
        )
        brain.add_task(
            "foundation_checkpoint",
            "Persistent checkpoint fingerprint",
            90,
            ["foundation_state"],
        )

        brain.add_decision(
            "single_source_of_truth",
            "ProjectBrain is the canonical project runtime state.",
        )

    brain.save()

    print("=== INTELLECT MEDIA / PROJECT BRAIN V2 ===")
    print(f"Status       : {brain.status}")
    print(f"Active Point : {brain.active_point}")
    print(f"Progress     : {brain.progress_percent:.2f}%")
    print(f"Tasks        : {len(brain.tasks)}")

    nxt = brain.next_task()
    print(f"Next Task    : {nxt.id if nxt else 'NONE'}")

    print(f"Checkpoint   : {brain.checkpoint()}")
