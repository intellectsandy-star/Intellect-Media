"""
Intellect Media
Autonomous Development Controller
Foundation entry point.
"""

from core.state.project_brain import ProjectBrain


def main() -> None:
    brain = ProjectBrain.load_or_create()
    print("Intellect Media Autonomous Development System")
    print(f"Project: {brain.project_name}")
    print(f"Active point: {brain.active_point}")
    print(f"Progress: {brain.progress_percent:.2f}%")
    print(f"Status: {brain.status}")


if __name__ == "__main__":
    main()
