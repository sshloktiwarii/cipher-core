import asyncio
from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, Vertical
from textual.widgets import Header, Footer, Static, Log, Button
from textual.binding import Binding
from rich.text import Text
from rich.panel import Panel
from rich.table import Table

from graph_engine import FoundryStateGraph
from state import OrchestratorState

class PipelineProgression(Static):
    """Visualizes the 5 active nodes in the state machine"""
    def update_pipeline(self, state: OrchestratorState):
        nodes = [
            ("Listen_Telemetry", "Telemetry"),
            ("Retrieve_Context(Graph)", "Graph Context"),
            ("Draft_Fix(Router)", "Router Fix"),
            ("Execute_Test(Crucible)", "Crucible Sandbox"),
            ("Stage_Commit(Airgap)", "Airgap Commit"),
        ]

        text = Text()
        text.append(" [FOUNDRY ORCHESTRATION PIPELINE]  ", style="bold cyan")

        for i, (node_key, label) in enumerate(nodes):
            is_active = state.active_node == node_key
            is_done = state.status == "RESOLVED"

            if is_active:
                text.append(f" ▶ [{label}] ", style="bold black on #f59e0b")
            elif is_done:
                text.append(f" ✓ {label} ", style="bold #10b981")
            else:
                text.append(f" ○ {label} ", style="dim #71717a")

            if i < len(nodes) - 1:
                text.append(" ➔ ", style="bold #3f3f46")

        self.update(text)

class IncidentBanner(Static):
    """Displays current incident telemetry and state"""
    def update_banner(self, state: OrchestratorState):
        status_colors = {
            "IDLE": "dim white",
            "INVESTIGATING": "yellow",
            "REMEDIATING": "cyan",
            "TESTING": "magenta",
            "COMMITTING": "blue",
            "RESOLVED": "bold green",
            "FAILED": "bold red",
        }
        color = status_colors.get(state.status, "white")
        
        table = Table(show_header=False, box=None, padding=(0, 1))
        table.add_column("Key", style="bold #a1a1aa", width=16)
        table.add_column("Value", style="white")

        table.add_row("Incident ID:", state.incident_id)
        table.add_row("Status:", Text(state.status, style=color))
        table.add_row("Title:", state.incident_title or "Awaiting telemetry trigger...")
        if state.commit_hash:
            table.add_row("Commit SHA:", Text(state.commit_hash, style="bold green"))

        self.update(Panel(table, title="[bold]Active Incident Telemetry[/bold]", border_style=color))

class MemoryView(Static):
    """Displays retrieved Obsidian memories from foundry-graph"""
    def update_memories(self, state: OrchestratorState):
        if not state.retrieved_context:
            self.update(Panel(Text("No vault context retrieved yet. Press 'r' to execute pipeline.", style="dim"), title="[bold]Second-Brain Grounding (foundry-graph)[/bold]", border_style="#27272a"))
            return

        table = Table(show_header=True, box=None, padding=(0, 1))
        table.add_column("Source", style="cyan", width=22)
        table.add_column("Heading", style="white", width=26)
        table.add_column("Similarity", style="yellow", width=12)

        for chunk in state.retrieved_context:
            sim_pct = f"{chunk.similarity * 100:.1f}%"
            table.add_row(chunk.file, chunk.heading, sim_pct)

        self.update(Panel(table, title=f"[bold]Second-Brain Grounding ({len(state.retrieved_context)} Notes)[/bold]", border_style="#10b981"))

class CrucibleSandboxView(Static):
    """Displays live Docker sandbox results from foundry-crucible"""
    def update_sandbox(self, state: OrchestratorState):
        if not state.test_result:
            self.update(Panel(Text("Sandbox idle. No candidate patch executing.", style="dim"), title="[bold]Crucible Sandbox Execution (foundry-crucible)[/bold]", border_style="#27272a"))
            return

        res = state.test_result
        color = "green" if res.passed else "red"
        status_txt = "PASSED (ExitCode 0)" if res.passed else f"FAILED (ExitCode {res.exit_code})"

        table = Table(show_header=False, box=None, padding=(0, 1))
        table.add_row("Status:", Text(status_txt, style=f"bold {color}"))
        table.add_row("Duration:", f"{res.execution_time_ms:.1f}ms")
        table.add_row("Stdout:", Text(res.stdout.strip() or "(none)", style="dim white"))
        if res.stderr:
            table.add_row("Stderr:", Text(res.stderr.strip(), style="red"))

        self.update(Panel(table, title="[bold]Crucible Sandbox Execution[/bold]", border_style=color))

class FoundryOmniApp(App):
    """Foundry Omni Textual Terminal UI Application"""

    CSS = """
    Screen {
        background: #09090b;
        color: #f4f4f5;
    }
    PipelineProgression {
        height: 3;
        margin: 1 1 0 1;
        background: #18181b;
        border: solid #27272a;
    }
    #top-row {
        height: 8;
        margin: 0 1;
    }
    #mid-row {
        height: 12;
        margin: 0 1;
    }
    #log-container {
        height: 1fr;
        margin: 0 1 1 1;
    }
    Log {
        background: #18181b;
        border: solid #27272a;
    }
    """

    BINDINGS = [
        Binding("r", "run_pipeline", "Run Pipeline"),
        Binding("s", "simulate_alert", "Simulate Incident"),
        Binding("c", "clear_logs", "Clear Logs"),
        Binding("q", "quit", "Quit"),
    ]

    def __init__(self):
        super().__init__()
        self.engine = FoundryStateGraph(on_state_update=self.on_state_change)
        self._is_busy = False

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield PipelineProgression(id="pipeline")
        
        with Horizontal(id="top-row"):
            yield IncidentBanner(id="incident-banner")

        with Horizontal(id="mid-row"):
            yield MemoryView(id="memory-view")
            yield CrucibleSandboxView(id="sandbox-view")

        with Container(id="log-container"):
            yield Log(id="activity-log", highlight=True)

        yield Footer()

    def on_mount(self) -> None:
        self.title = "Foundry Omni — Autonomous State Machine"
        self.sub_title = "LangGraph Master Node & Terminal Telemetry"
        self.refresh_views()
        log_widget = self.query_one("#activity-log", Log)
        log_widget.write_line("⚡ Foundry Omni master daemon initialized.")
        log_widget.write_line("Press [r] to trigger automated remediation cycle, or [s] to simulate incident.")

    def on_state_change(self, state: OrchestratorState) -> None:
        self.call_from_thread(self.refresh_views)

    def refresh_views(self) -> None:
        state = self.engine.state
        self.query_one("#pipeline", PipelineProgression).update_pipeline(state)
        self.query_one("#incident-banner", IncidentBanner).update_banner(state)
        self.query_one("#memory-view", MemoryView).update_memories(state)
        self.query_one("#sandbox-view", CrucibleSandboxView).update_sandbox(state)
        
        log_widget = self.query_one("#activity-log", Log)
        if state.logs:
            latest = state.logs[-1]
            log_widget.write_line(latest)

    async def action_run_pipeline(self) -> None:
        if self._is_busy:
            return
        self._is_busy = True
        try:
            await self.engine.run_full_pipeline()
        finally:
            self._is_busy = False

    async def action_simulate_alert(self) -> None:
        if self._is_busy:
            return
        self._is_busy = True
        try:
            simulated = {
                "title": "OOM Memory Spill in Worker Thread",
                "source": "foundry-pulse",
                "metric": "container_memory_bytes",
                "value": "134217728",
                "threshold": "134217728",
            }
            await self.engine.run_full_pipeline(simulated_incident=simulated)
        finally:
            self._is_busy = False

    def action_clear_logs(self) -> None:
        self.query_one("#activity-log", Log).clear()

if __name__ == "__main__":
    app = FoundryOmniApp()
    app.run()
