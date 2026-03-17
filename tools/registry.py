"""
Tool Registry - Central registration and dispatch for all agent tools.
Based on Hermes Agent tool registry pattern.
"""

from typing import Callable, Optional

_registry: dict[str, dict] = {}


def register(
    name: str,
    handler: Callable,
    schema: dict,
    toolset: str = "general",
    description: str = "",
    requires_env: Optional[list[str]] = None,
):
    """Register a tool in the central registry."""
    _registry[name] = {
        "name": name,
        "handler": handler,
        "schema": schema,
        "toolset": toolset,
        "description": description,
        "requires_env": requires_env or [],
    }


def get_definitions(toolsets: Optional[list[str]] = None) -> list[dict]:
    """Get OpenAI-format tool definitions, optionally filtered by toolset."""
    tools = []
    for tool in _registry.values():
        if toolsets and tool["toolset"] not in toolsets:
            continue
        tools.append({
            "type": "function",
            "function": {
                "name": tool["name"],
                "description": tool["description"],
                "parameters": tool["schema"],
            },
        })
    return tools


def dispatch(name: str, arguments: dict):
    """Execute a registered tool by name."""
    if name not in _registry:
        return {"error": f"Tool '{name}' not found"}
    return _registry[name]["handler"](**arguments)


def list_tools() -> list[str]:
    """List all registered tool names."""
    return list(_registry.keys())
