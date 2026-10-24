# cipher-core

Five-node autonomous self-healing state machine for local AI environments.

Written in pure Go. Continuously evaluates telemetry signals, retrieves contextual runbooks, synthesizes minimal patches, verifies them in the execution sandbox, and commits validated fixes.

Looking for a plain-English, non-technical summary? See [EXPLAINER.md](EXPLAINER.md).

---

## The 5-Node Pipeline

```text
Listen_Telemetry ---> Retrieve_Context ---> Draft_Fix ---> Execute_Test ---> Stage_Commit
```

1. **`Listen_Telemetry`**: Polls `/tmp/cipher/log.sock` for incident alerts and container execution timeouts.
2. **`Retrieve_Context`**: Queries `/tmp/cipher/mem.sock` for architecture decisions and past incident resolutions.
3. **`Draft_Fix`**: Submits context and error trace to the local routing gateway (`/tmp/cipher/route.sock` or `http://localhost:8080`).
4. **`Execute_Test`**: Sends candidate code to `/tmp/cipher/exec.sock` for isolated execution under a 3-second timeout ceiling.
5. **`Stage_Commit`**: On verified zero exit code, dispatches a signed Conventional Commit through `/tmp/cipher/mcp.sock`.

---

## Build

```bash
go build -o cipher-core .
```

---

## Usage

### Run Single Remediation Loop
```bash
./cipher-core --once
```

### Run Continuous Daemon
```bash
./cipher-core --poll-interval 2s --socket /tmp/cipher/core.sock
```

---

## License

MIT License. Copyright (c) 2026 Shlok Tiwari.
