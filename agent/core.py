"""
OftalmoClaw Agent Core
Based on Hermes Agent architecture by Nous Research.

This module will contain the main AI agent loop, tool calling,
memory management, and skill loading.
"""


def run_cli():
    """Start the agent in CLI mode."""
    print("\n  OftalmoClaw CLI Agent")
    print("  Type 'exit' to quit.\n")

    while True:
        try:
            user_input = input("  > ")
            if user_input.strip().lower() in ("exit", "quit", "q"):
                print("  Ate logo!")
                break
            # TODO: Connect to LLM provider and process with tools/skills
            print(f"  [Agent] Received: {user_input}")
            print("  [Agent] LLM provider not configured. Set OPENROUTER_API_KEY or ANTHROPIC_API_KEY in .env\n")
        except (KeyboardInterrupt, EOFError):
            print("\n  Ate logo!")
            break
