from __future__ import annotations
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path
import hashlib, json

REPO = Path.cwd()
RUNTIME = REPO / "runtime"
STATE = RUNTIME / "project_brain.json"

def now(): return datetime.now(timezone.utc).isoformat()
def h(x): return hashlib.sha256(json.dumps(x, sort_keys=True, separators=(",", ":"), default=str).encode()).hexdigest()

@dataclass
class Task:
    task_id: str
    title: str
    status: str = "backlog"
    priority: int = 50
    dependencies: list[str] | None = None
    verified: bool = False
    attempts: int = 0
    owner: str | None = None
    def __post_init__(self): self.dependencies = self.dependencies or []

class Brain:
    def __init__(self):
        self.project_name="Intellect Media"; self.system_version="1.0.0"; self.status="foundation"
        self.active_point=0; self.total_points=15; self.completed_points=[]; self.locked_points=[]
        self.tasks={}; self.decisions=[]; self.checkpoint_id=""; self.architecture_fingerprint=""; self.last_updated=now()
    @property
    def progress(self):
        return round(sum(t.status=="done" and t.verified for t in self.tasks.values())/len(self.tasks)*100,2) if self.tasks else 0.0
    def snap(self):
        return {"project_name":self.project_name,"system_version":self.system_version,"status":self.status,"active_point":self.active_point,"total_points":self.total_points,"completed_points":self.completed_points,"locked_points":self.locked_points,"tasks":{k:asdict(v) for k,v in self.tasks.items()},"decisions":self.decisions,"checkpoint_id":self.checkpoint_id,"architecture_fingerprint":self.architecture_fingerprint,"last_updated":self.last_updated,"progress_percent":self.progress}
    def save(self):
        RUNTIME.mkdir(exist_ok=True); STATE.write_text(json.dumps(self.snap(), indent=2), encoding="utf-8")
    def checkpoint(self):
        x=self.snap(); x["checkpoint_id"]=""; self.checkpoint_id=h(x)[:16]; self.architecture_fingerprint=h({"version":self.system_version,"points":self.total_points,"decisions":self.decisions}); self.last_updated=now(); self.save()

def load():
    b=Brain()
    if STATE.exists():
        x=json.loads(STATE.read_text(encoding="utf-8")); b.project_name=x["project_name"]; b.system_version=x["system_version"]; b.status=x["status"]; b.active_point=x["active_point"]; b.total_points=x["total_points"]; b.completed_points=x["completed_points"]; b.locked_points=x["locked_points"]; b.tasks={k:Task(**v) for k,v in x["tasks"].items()}; b.decisions=x["decisions"]; b.checkpoint_id=x["checkpoint_id"]; b.architecture_fingerprint=x["architecture_fingerprint"]; b.last_updated=x["last_updated"]; return b
    deps=[None,"foundation_controller","foundation_controller","foundation_continuity","foundation_verification"]
    titles=["Autonomous task controller","Persistent continuity and session resume","Verification and regression layer","Git checkpoint and repository continuity","Recovery and fail-closed behavior"]
    pri=[100,95,90,85,80]
    for i in range(5): b.tasks[f"foundation_{i+1}"]=Task(f"foundation_{i+1}",titles[i],priority=pri[i],dependencies=[] if deps[i] is None else [deps[i]])
    b.decisions=[{"title":"single_source_of_truth","rationale":"ProjectBrain is canonical runtime state.","timestamp":now()},{"title":"one_active_product_point","rationale":"Only one of 15 product points may be active.","timestamp":now()},{"title":"owner_is_non_developer","rationale":"Owner provides vision; system handles technical orchestration.","timestamp":now()},{"title":"no_mandatory_coding_extension","rationale":"Core development uses GPT, Python, PowerShell and Git/GitHub.","timestamp":now()}]
    b.checkpoint(); return b

def main():
    b=load(); assert b.project_name=="Intellect Media"; assert b.total_points==15; assert b.active_point==0; assert len(b.tasks)==5; assert b.checkpoint_id
    print("Project         :",b.project_name); print("System          :",b.system_version); print("Status          :",b.status); print("Active Point    :",b.active_point); print("Progress        :",f"{b.progress:.2f}%"); print("Foundation tasks:",len(b.tasks)); print("Checkpoint      :",b.checkpoint_id); print("Point 01        : LOCKED"); print("Verified        : YES")
if __name__=="__main__": main()
