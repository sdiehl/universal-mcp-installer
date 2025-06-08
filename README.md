# Universal MCP Server Installer

Installing local MCP servers is a pain. Each client has different config formats, locations, and requirements. Different operating systems (MacOS, Windows, Linux) have different config file paths. This installer handles all of that automatically.

## Quick Start

1. Drop `install.py` into your MCP server project

2. Edit the configuration variables at the top:

   ```python
   # XXX: Change these to match your server
   SERVER_NAME = "your-server-name"
   SERVER_EXECUTABLE = "path/to/your/server.py"
   ```

3. Then all the end user needs to do is run the installer:
   ```bash
   uv run install.py
   ```

## Supported Clients

- **Claude Desktop** - `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Cursor** - `~/.cursor/mcp.json`
- **VS Code** - `~/.vscode/mcp.json`
- **Cline** - `~/.cline/mcp.json`
- **Windsurf** - `~/.codeium/windsurf/mcp_config.json`
- **n8n** - `~/.n8n/mcp.json`
- **5ire** - `~/.5ire/mcp.json`

## Requirements

- Python 3.8+
- `uv` package manager (for running the server)

## License

Do whatever. [WTFPL](LICENSE)
