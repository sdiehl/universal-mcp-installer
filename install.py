#!/usr/bin/env python3

"""
A universal MCP Server Installer Script. Works with the following clients:

* Claude Desktop
* Cursor
* VS Code
* Cline
* Windsurf
* n8n
* 5ire

https://github.com/sdiehl/universal-mcp-installer
"""

import argparse
import json
import os
import platform
import sys
from pathlib import Path
from typing import Any, Dict, Tuple

# XXX: Change these to match your server
SERVER_NAME = "usolver"
SERVER_EXECUTABLE = "usolver_mcp/server/main.py"


def get_config_paths() -> Dict[str, Path]:
    """Get the config file paths for all supported MCP clients"""
    system = platform.system()
    home = Path.home()

    config_paths = {}

    if system == "Darwin":  # macOS
        config_paths.update(
            {
                "claude": home
                / "Library/Application Support/Claude/claude_desktop_config.json",
                "cursor": home / ".cursor/mcp.json",
                "vscode": home / ".vscode/mcp.json",
                "cline": home / ".cline/mcp.json",
                "windsurf": home / ".codeium/windsurf/mcp_config.json",
                "n8n": home / ".n8n/mcp.json",
                "5ire": home / "Library/Application Support/5ire/mcp.json",
            }
        )
    elif system == "Windows":
        appdata = os.environ.get("APPDATA", "")
        localappdata = os.environ.get("LOCALAPPDATA", "")
        config_paths.update(
            {
                "claude": Path(appdata) / "Claude/claude_desktop_config.json",
                "cursor": home / ".cursor/mcp.json",
                "vscode": home / ".vscode/mcp.json",
                "cline": home / ".cline/mcp.json",
                "windsurf": Path(localappdata) / "Codeium/Windsurf/mcp_config.json",
                "n8n": home / ".n8n/mcp.json",
                "5ire": Path(appdata) / "5ire/mcp.json",
            }
        )
    else:  # Linux and others
        config_paths.update(
            {
                "claude": home / ".config/Claude/claude_desktop_config.json",
                "cursor": home / ".cursor/mcp.json",
                "vscode": home / ".vscode/mcp.json",
                "cline": home / ".cline/mcp.json",
                "windsurf": home / ".config/windsurf/mcp_config.json",
                "n8n": home / ".n8n/mcp.json",
                "5ire": home / ".config/5ire/mcp.json",
            }
        )

    return config_paths


def load_or_create_config(
    config_path: Path, default_structure: Dict[str, Any] | None = None
) -> Dict[str, Any]:
    """Load existing config or create a new one with specified default structure"""
    if config_path.exists():
        try:
            with open(config_path) as f:
                return json.load(f)
        except (OSError, json.JSONDecodeError):
            print(f"Warning: Could not read {config_path}, creating new config")

    return default_structure or {"mcpServers": {}}


def save_config(config_path: Path, config_data: Dict[str, Any]) -> None:
    """Save config to file, creating directories if needed"""
    config_path.parent.mkdir(parents=True, exist_ok=True)
    with open(config_path, "w") as f:
        json.dump(config_data, f, indent=2)


def get_uv_command() -> str:
    """Get the uv command path"""
    possible_paths = [
        "/opt/homebrew/bin/uv",  # Homebrew on macOS
        "/usr/local/bin/uv",  # Manual install
        "uv",  # In PATH
    ]

    for path in possible_paths:
        if Path(path).exists() or path == "uv":
            return path

    return "uv"  # Fallback


def install_to_claude_cursor_format(
    config_path: Path, script_dir: Path, server_name: str
) -> bool:
    """Install MCP server configuration to Claude Desktop/Cursor format"""
    config = load_or_create_config(config_path)

    if "mcpServers" not in config:
        config["mcpServers"] = {}

    # Build server configuration
    server_config = {
        "command": get_uv_command(),
        "args": [
            "run",
            "--directory",
            str(script_dir),
            SERVER_EXECUTABLE,
        ],
    }

    # Add our server configuration
    config["mcpServers"][server_name] = server_config

    save_config(config_path, config)
    return True


def install_to_vscode_format(
    config_path: Path, script_dir: Path, server_name: str
) -> bool:
    """Install MCP server configuration to VSCode format"""
    default_structure: Dict[str, Any] = {"inputs": [], "servers": {}}

    config = load_or_create_config(config_path, default_structure)

    if "servers" not in config:
        config["servers"] = {}

    # Build server configuration for VSCode
    server_config = {
        "type": "stdio",
        "command": get_uv_command(),
        "args": [
            "run",
            "--directory",
            str(script_dir),
            SERVER_EXECUTABLE,
        ],
    }

    # Add our server configuration
    config["servers"][server_name] = server_config

    save_config(config_path, config)
    return True


def install_to_windsurf_format(
    config_path: Path, script_dir: Path, server_name: str
) -> bool:
    """Install MCP server configuration to Windsurf format"""
    default_structure: Dict[str, Any] = {"servers": []}

    config = load_or_create_config(config_path, default_structure)

    if "servers" not in config:
        config["servers"] = []

    # Build server configuration for Windsurf
    server_config = {
        "name": server_name,
        "command": get_uv_command(),
        "args": [
            "run",
            "--directory",
            str(script_dir),
            SERVER_EXECUTABLE,
        ],
    }

    # Check if server already exists and update it, otherwise add new
    existing_server = None
    for i, server in enumerate(config["servers"]):
        if server.get("name") == server_name:
            existing_server = i
            break

    if existing_server is not None:
        config["servers"][existing_server] = server_config
    else:
        config["servers"].append(server_config)

    save_config(config_path, config)
    return True


def install_to_client(
    client_name: str, config_path: Path, script_dir: Path, server_name: str
) -> Tuple[bool, str]:
    """Install to a specific client based on its format"""
    try:
        if client_name in ["claude", "cursor", "cline", "n8n", "5ire"]:
            install_to_claude_cursor_format(config_path, script_dir, server_name)
        elif client_name == "vscode":
            install_to_vscode_format(config_path, script_dir, server_name)
        elif client_name == "windsurf":
            install_to_windsurf_format(config_path, script_dir, server_name)
        else:
            return False, f"Unknown client format: {client_name}"

        return True, f"✓ Installed to {client_name.title()}: {config_path}"
    except Exception as e:
        return False, f"✗ Failed to install to {client_name.title()}: {e}"


def parse_arguments() -> argparse.Namespace:
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
        description="Universal MCP Server Installer - Install MCP servers to various clients",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Supported clients:
  claude    - Claude Desktop
  cursor    - Cursor
  vscode    - Visual Studio Code
  cline     - Cline
  windsurf  - Windsurf
  n8n       - n8n
  5ire      - 5ire

Examples:
  %(prog)s                           # Install to all available clients
  %(prog)s --clients claude cursor   # Install only to Claude Desktop and Cursor
  %(prog)s --server-name my-server   # Override the server name
  %(prog)s --yes                     # Skip confirmation prompt
        """,
    )

    parser.add_argument(
        "--clients",
        nargs="+",
        choices=["claude", "cursor", "vscode", "cline", "windsurf", "n8n", "5ire"],
        help="Specify which clients to install to (default: all available)",
    )

    parser.add_argument(
        "--server-name",
        default=SERVER_NAME,
        help=f"Override the server name (default: {SERVER_NAME})",
    )

    parser.add_argument(
        "--yes",
        "-y",
        action="store_true",
        help="Skip confirmation prompt and proceed with installation",
    )

    parser.add_argument(
        "--list-clients",
        action="store_true",
        help="List all supported clients and their config paths",
    )

    return parser.parse_args()


def list_clients() -> None:
    """List all supported clients and their configuration paths"""
    config_paths = get_config_paths()

    print("Supported MCP Clients and Configuration Paths:")
    print("=" * 50)

    for client_name, config_path in config_paths.items():
        status = "✓" if config_path.parent.exists() else "✗"
        print(f"{status} {client_name.ljust(10)} - {config_path}")

    print()
    print("✓ = Client directory exists")
    print("✗ = Client directory not found")


def main() -> None:
    """Install MCP server to local configurations"""
    args = parse_arguments()

    # Handle list clients option
    if args.list_clients:
        list_clients()
        return

    script_dir = Path(__file__).parent.absolute()
    server_name = args.server_name

    print("MCP Server Installer")
    print("======================")
    print()
    print("This will install the MCP server to your local client configurations.")
    print(f"Installation directory: {script_dir}")
    print(f"Server name: {server_name}")
    print(f"Server executable: {SERVER_EXECUTABLE}")

    # Show which clients will be targeted
    config_paths = get_config_paths()
    if args.clients:
        target_clients = {
            name: path for name, path in config_paths.items() if name in args.clients
        }
        print(f"Target clients: {', '.join(args.clients)}")
    else:
        target_clients = config_paths
        print("Target clients: all available")

    print()

    # Ask for confirmation unless --yes is specified
    if not args.yes:
        while True:
            response = (
                input("Do you want to proceed with the installation? (y/n): ")
                .lower()
                .strip()
            )
            if response in ["y", "yes"]:
                break
            elif response in ["n", "no"]:
                print("Installation cancelled.")
                sys.exit(0)
            else:
                print("Please enter 'y' for yes or 'n' for no.")
        print()

    installed_to = []

    # Install to each target client
    for client_name, config_path in target_clients.items():
        # Skip clients where the parent directory doesn't exist (except for new installations)
        if (
            client_name in ["cursor", "cline", "n8n", "5ire"]
            and not config_path.parent.exists()
        ):
            print(f"• {client_name.title()} config directory not found, skipping")
            continue

        success, message = install_to_client(
            client_name, config_path, script_dir, server_name
        )
        print(message)

        if success:
            installed_to.append(client_name.title())

    print()
    if installed_to:
        print("Installation completed successfully!")
        print(f"Installed to: {', '.join(installed_to)}")
        print()
        print("Please restart your client(s) to use the MCP server.")
        print()
        print("Note: Some clients may require additional setup:")
        print("- VSCode: Make sure the MCP extension is installed")
        print("- Windsurf: Restart the application to load the new configuration")
    else:
        print("Installation failed - no configurations were updated.")
        sys.exit(1)


if __name__ == "__main__":
    main()
