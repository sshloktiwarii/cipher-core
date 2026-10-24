import os

# Cipher Service Endpoints
CIPHER_ROUTE_URL = os.getenv("CIPHER_ROUTE_URL", os.getenv("FOUNDRY_ROUTER_URL", "http://localhost:8080"))
CIPHER_EXEC_URL = os.getenv("CIPHER_EXEC_URL", os.getenv("FOUNDRY_CRUCIBLE_URL", "http://localhost:8081"))
CIPHER_LOG_URL = os.getenv("CIPHER_LOG_URL", os.getenv("FOUNDRY_PULSE_URL", "http://localhost:8082"))
CIPHER_MEM_URL = os.getenv("CIPHER_MEM_URL", os.getenv("FOUNDRY_GRAPH_URL", "http://localhost:8083"))
CIPHER_MCP_URL = os.getenv("CIPHER_MCP_URL", os.getenv("FOUNDRY_AIRGAP_URL", "http://localhost:8085"))

# Backward Compatibility Aliases
FOUNDRY_ROUTER_URL = CIPHER_ROUTE_URL
FOUNDRY_CRUCIBLE_URL = CIPHER_EXEC_URL
FOUNDRY_PULSE_URL = CIPHER_LOG_URL
FOUNDRY_GRAPH_URL = CIPHER_MEM_URL
FOUNDRY_AIRGAP_URL = CIPHER_MCP_URL

POLL_INTERVAL_SECONDS = float(os.getenv("POLL_INTERVAL_SECONDS", "3.0"))
EXECUTION_TIMEOUT = float(os.getenv("EXECUTION_TIMEOUT", "5.0"))

