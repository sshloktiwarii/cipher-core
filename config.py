import os

# Foundry Service Endpoints
FOUNDRY_ROUTER_URL = os.getenv("FOUNDRY_ROUTER_URL", "http://localhost:8080")
FOUNDRY_CRUCIBLE_URL = os.getenv("FOUNDRY_CRUCIBLE_URL", "http://localhost:8081")
FOUNDRY_PULSE_URL = os.getenv("FOUNDRY_PULSE_URL", "http://localhost:8082")
FOUNDRY_GRAPH_URL = os.getenv("FOUNDRY_GRAPH_URL", "http://localhost:8083")
FOUNDRY_AIRGAP_URL = os.getenv("FOUNDRY_AIRGAP_URL", "http://localhost:8085")

POLL_INTERVAL_SECONDS = float(os.getenv("POLL_INTERVAL_SECONDS", "3.0"))
EXECUTION_TIMEOUT = float(os.getenv("EXECUTION_TIMEOUT", "5.0"))
