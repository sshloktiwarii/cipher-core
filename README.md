# Foundry Omni: LangGraph Autonomous State Machine & Terminal UI

The central orchestration master node of the Foundry Local AI PaaS. It runs a deterministic 5-stage LangGraph workflow that continuously closes the loop between telemetry, knowledge retrieval, code generation, sandboxed execution, and version-controlled commits.

## The 5-Node Autonomous Remediation Pipeline
1. **`[Listen_Telemetry]`**: Intercepts incident metrics, container timeouts, and latency spikes from [[foundry-pulse]].
2. **`[Retrieve_Context(Graph)]`**: Grounded in your Obsidian second brain; queries [[foundry-graph]] vector store for architecture decisions (ADRs) and incident runbooks.
3. **`[Draft_Fix(Router)]`**: Dispatches the context and prompt to [[foundry-router]] to synthesize a minimal patch.
4. **`[Execute_Test(Crucible)]`**: Deploys candidate code directly to the [[foundry-crucible]] isolated Docker sandbox (512MB RAM, zero network, 5s timeout) to verify correctness.
5. **`[Stage_Commit(Airgap)]`**: Upon verification, requests a signed Conventional Commit through [[foundry-airgap]].

## Interactive Terminal UI (Textual)
Includes a high-density, real-time Terminal UI powered by `Textual` and `Rich`:
- **Top Pipeline Indicator**: Live active node transitions and glowing progress states.
- **Incident Telemetry Banner**: Real-time status, incident ID, and metrics thresholds.
- **Second-Brain Memory Panel**: Retrieved markdown chunks with cosine similarity ratings.
- **Crucible Execution Stream**: Real-time stdout, stderr, and container latency measurements.
- **Activity Stream**: Timestamped decision logs.

## Quickstart

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Launch Interactive Terminal UI
```bash
python3 main.py
```
*Keyboard Shortcuts:*
- `r`: Execute full automated remediation pipeline
- `s`: Simulate incident alert
- `c`: Clear log history
- `q`: Quit

### 3. Run Headless Daemon
```bash
python3 main.py --daemon
```

### 4. Single-Shot Pipeline
```bash
python3 main.py --once
```
