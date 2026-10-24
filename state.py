from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field
import time
import uuid

class MemoryChunk(BaseModel):
    id: str
    file: str
    title: str
    heading: str
    content: str
    similarity: float = 0.0

class SandboxExecution(BaseModel):
    stdout: str = ""
    stderr: str = ""
    exit_code: int = 0
    execution_time_ms: float = 0.0
    passed: bool = False

class OrchestratorState(BaseModel):
    incident_id: str = Field(default_factory=lambda: str(uuid.uuid4())[:8])
    status: str = "IDLE"  # IDLE, INVESTIGATING, REMEDIATING, TESTING, COMMITTING, RESOLVED, FAILED
    active_node: str = "Listen_Telemetry"
    incident_title: str = ""
    incident_details: Dict[str, Any] = Field(default_factory=dict)
    retrieved_context: List[MemoryChunk] = Field(default_factory=list)
    drafted_fix: str = ""
    target_file: str = "main.py"
    test_result: Optional[SandboxExecution] = None
    commit_hash: str = ""
    logs: List[str] = Field(default_factory=list)
    updated_at: float = Field(default_factory=time.time)

    def log(self, message: str) -> None:
        timestamp = time.strftime("%H:%M:%S")
        if len(self.logs) >= 500:
            self.logs.pop(0)
        self.logs.append(f"[{timestamp}] {message}")
        self.updated_at = time.time()
