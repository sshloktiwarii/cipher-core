import argparse
import asyncio
import sys
import logging
from graph_engine import FoundryStateGraph

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("foundry-omni")

async def run_headless_daemon():
    logger.info("Starting Foundry Omni in headless daemon mode...")
    engine = FoundryStateGraph(
        on_state_update=lambda state: logger.info(f"[{state.active_node}] {state.status}: {state.logs[-1] if state.logs else ''}")
    )

    while True:
        try:
            logger.info("Polling for active incidents...")
            await engine.run_full_pipeline()
            await asyncio.sleep(10)
        except asyncio.CancelledError:
            break
        except Exception as e:
            logger.error(f"Error in daemon loop: {e}")
            await asyncio.sleep(5)

def main():
    parser = argparse.ArgumentParser(description="Foundry Omni: Autonomous LangGraph State Machine & Orchestrator")
    parser.add_argument("--daemon", action="store_true", help="Run as headless background daemon without TUI")
    parser.add_argument("--once", action="store_true", help="Execute single autonomous remediation pipeline and exit")
    args = parser.parse_args()

    if args.once:
        engine = FoundryStateGraph(
            on_state_update=lambda s: print(f"[{s.active_node}] {s.logs[-1] if s.logs else ''}")
        )
        asyncio.run(engine.run_full_pipeline())
        sys.exit(0)

    if args.daemon:
        asyncio.run(run_headless_daemon())
    else:
        try:
            from tui import FoundryOmniApp
            app = FoundryOmniApp()
            app.run()
        except ImportError as e:
            logger.error(f"Textual not installed ({e}). Falling back to headless runner.")
            asyncio.run(run_headless_daemon())

if __name__ == "__main__":
    main()
