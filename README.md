# Universal MCP Server Installer

Installing local MCP servers is a pain. Each client has different config formats, locations, and requirements. Different operating systems (MacOS, Windows, Linux) have different config file paths. This installer handles all of that automatically.

## Quick Start

1. Drop `install.py` into the root of your MCP server project that uses uv for package management.

2. Edit the configuration variables at the top of `install.py` to match your server's details:

   ```python
   # XXX: Change these to match your server
   SERVER_NAME = "your-server-name"
   SERVER_EXECUTABLE = "local/path/to/server.py"
   ```

3. Then all the end user needs to do is clone your repo and run the installer:

   ```bash
   ./install.py
   ```

## One-line Install

For convenience, there's also a shell script that can install directly from GitHub:

```bash
curl -fsSL https://raw.githubusercontent.com/user/repo/main/install.sh | sh
```

Set the `GITHUB_USERNAME`, `GITHUB_REPO`, and `GITHUB_BRANCH` variables in the script to match your repository.

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
