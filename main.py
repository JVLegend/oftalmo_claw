"""
OftalmoClaw - AI-Powered Ophthalmology Mission Control
Created by GeekVision

Entry point for all modes: web, cli, gateway
"""

import sys
import uvicorn
from config import settings


def main():
    mode = "web"
    if len(sys.argv) > 1:
        if "--mode" in sys.argv:
            idx = sys.argv.index("--mode")
            if idx + 1 < len(sys.argv):
                mode = sys.argv[idx + 1]
        elif "--setup" in sys.argv:
            mode = "setup"

    if mode == "web":
        print(f"\n  OftalmoClaw v{settings.app_version}")
        print(f"  by GeekVision")
        print(f"  Mission Control: http://{settings.host}:{settings.port}\n")
        uvicorn.run(
            "web.app:app",
            host=settings.host,
            port=settings.port,
            reload=settings.debug,
            log_level=settings.log_level.lower(),
        )
    elif mode == "cli":
        from agent.core import run_cli
        run_cli()
    elif mode == "gateway":
        from gateway.run import start_gateway
        start_gateway()
    elif mode == "setup":
        print("Setup wizard coming soon...")
    else:
        print(f"Unknown mode: {mode}")
        print("Usage: python main.py [--mode web|cli|gateway] [--setup]")
        sys.exit(1)


if __name__ == "__main__":
    main()
