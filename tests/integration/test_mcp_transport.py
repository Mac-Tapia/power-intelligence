"""Real stdio handshake and calls; helper tests alone do not prove MCP works."""

import asyncio
import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]


def test_stdio_handshake_and_readonly_tools():
    pytest.importorskip("mcp")
    from mcp import ClientSession, StdioServerParameters, stdio_client

    async def exercise():
        params = StdioServerParameters(command=sys.executable,
                                       args=[str(ROOT / "tools/mcp/unitesis_server.py")])
        async with stdio_client(params) as streams, ClientSession(*streams) as session:
            initialized = await session.initialize()
            assert initialized.server_info.name == "unitesis-project"
            tools = await session.list_tools()
            assert len(tools.tools) == 4
            result = await session.call_tool("unitesis_list_features", {})
            assert not result.is_error
            assert "009" in json.dumps(result.model_dump())
            denied = await session.call_tool("unitesis_read_document", {"path": "../../.env"})
            assert denied.is_error

    asyncio.run(asyncio.wait_for(exercise(), timeout=30))
