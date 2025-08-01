"""Entry point for running MCP server as a module.

Usage:
    python -m browser_user.mcp.server
"""

import asyncio

from browser_user.mcp.server import main

if __name__ == '__main__':
	asyncio.run(main())
