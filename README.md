# Universal MCP Server Installer

Installing local MCP servers is a pain. Each client has different config formats, locations, and requirements. Different operating systems (MacOS, Windows, Linux) have different config file paths. This installer handles all of that automatically.

## Quick Start

1. Drop `install.py` into the root of your MCP server project that uses uv for package management.

2. Edit the configuration variables at the top of `install.py` to match your server's details.

   ```python

   ```python
   # XXX: Change these to match your server
   SERVER_NAME = "your-server-name"
   SERVER_EXECUTABLE = "local/path/to/server.py"
   ```

3. Then all the end user needs to do is clone you repo and run the installer:

   ```bash
   ./install.py
   ```

## Supported Clients

- **Claude Desktop**
- **Cursor**
- **VS Code**
- **Cline**
- **Windsurf**
- **n8n**
- **5ire**

## License

Just do whatever. [WTFPL](LICENSE)
