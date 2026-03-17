"""
OftalmoClaw Gateway
Messaging platform integrations (Telegram, WhatsApp, Discord, etc.)
Based on Hermes Agent gateway architecture.
"""


def start_gateway():
    """Start the messaging gateway."""
    print("\n  OftalmoClaw Gateway")
    print("  Configure messaging platforms in .env")
    print("  Supported: Telegram, WhatsApp, Discord, Slack, Email\n")

    from config import settings

    platforms = []
    if settings.telegram_token:
        platforms.append("Telegram")
    if settings.whatsapp_token:
        platforms.append("WhatsApp")
    if settings.discord_token:
        platforms.append("Discord")

    if not platforms:
        print("  No messaging platforms configured.")
        print("  Set TELEGRAM_TOKEN, WHATSAPP_TOKEN, or DISCORD_TOKEN in .env")
        return

    print(f"  Active platforms: {', '.join(platforms)}")
    print("  Gateway starting...")
    # TODO: Initialize platform adapters and start event loops
