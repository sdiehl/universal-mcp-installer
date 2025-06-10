#!/bin/bash

# Universal MCP Server Installer Script
# Configure these variables for your repository
GITHUB_USERNAME="${GITHUB_USERNAME:-sdiehl}"
GITHUB_REPO="${GITHUB_REPO:-usolver}"
GITHUB_BRANCH="${GITHUB_BRANCH:-main}"

# Usage: curl -fsSL https://raw.githubusercontent.com/${GITHUB_USERNAME}/${GITHUB_REPO}/${GITHUB_BRANCH}/install.sh | sh
# Or: curl -fsSL https://raw.githubusercontent.com/${GITHUB_USERNAME}/${GITHUB_REPO}/${GITHUB_BRANCH}/install.sh | sh -s -- [options]

set -e

# Default values - these can be overridden by environment variables
REPO_URL="${REPO_URL:-https://github.com/${GITHUB_USERNAME}/${GITHUB_REPO}.git}"
BRANCH="${BRANCH:-${GITHUB_BRANCH}}"
SERVER_NAME="${SERVER_NAME:-${GITHUB_REPO}}"

# Function to print status messages
print_status() {
    echo "[INFO] $1"
}

print_success() {
    echo "[SUCCESS] $1"
}

print_warning() {
    echo "[WARNING] $1"
}

print_error() {
    echo "[ERROR] $1"
}

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to install uv if it doesn't exist
install_uv() {
    if command_exists uv; then
        print_status "uv is already installed"
        return 0
    fi

    print_status "Installing uv..."
    if command_exists curl; then
        curl -LsSf https://astral.sh/uv/install.sh | sh
    else
        print_error "curl is required to install uv"
        exit 1
    fi

    # Source the shell profile to make uv available
    if [ -f "$HOME/.cargo/env" ]; then
        # shellcheck source=/dev/null
        . "$HOME/.cargo/env"
    fi

    # Add to PATH for current session
    export PATH="$HOME/.cargo/bin:$PATH"

    if command_exists uv; then
        print_success "uv installed successfully"
    else
        print_error "Failed to install uv"
        exit 1
    fi
}

# Function to parse command line arguments
parse_args() {
    while [ $# -gt 0 ]; do
        case $1 in
            --repo)
                REPO_URL="$2"
                shift 2
                ;;
            --branch)
                BRANCH="$2"
                shift 2
                ;;
            --server-name)
                SERVER_NAME="$2"
                shift 2
                ;;
            --help|-h)
                show_help
                exit 0
                ;;
            *)
                print_error "Unknown option: $1"
                show_help
                exit 1
                ;;
        esac
    done
}

# Function to show help
show_help() {
    cat << EOF
Universal MCP Server Installer

Usage: 
  ./install.sh
  ./install.sh [options]

Options:
  --repo URL          Git repository URL (default: $REPO_URL)
  --branch BRANCH     Git branch to clone (default: $BRANCH)
  --server-name NAME  Server name for installation (default: $SERVER_NAME)
  --help, -h          Show this help message

Environment Variables:
  REPO_URL           Override default repository URL
  BRANCH             Override default branch
  SERVER_NAME        Override default server name

Examples:
  # Install with defaults
  ./install.sh

  # Install with custom repository
  ./install.sh --repo https://github.com/user/repo.git

  # Install with custom branch and server name
  ./install.sh --branch main --server-name myserver
EOF
}

# Function to extract repository name from URL
get_repo_name() {
    basename "$1" .git
}

# Main installation function
main() {
    print_status "Starting Universal MCP Server Installation"
    
    # Parse command line arguments
    parse_args "$@"
    
    # Check for required commands
    if ! command_exists git; then
        print_error "git is required but not installed"
        exit 1
    fi

    if ! command_exists python3; then
        print_error "python3 is required but not installed"
        exit 1
    fi

    # Install uv if needed
    install_uv

    # Create installation directory
    INSTALL_DIR="$HOME/.local/share/$SERVER_NAME"
    print_status "Installing to: $INSTALL_DIR"

    # Remove existing installation if it exists
    if [ -d "$INSTALL_DIR" ]; then
        print_warning "Existing installation found, removing..."
        rm -rf "$INSTALL_DIR"
    fi

    # Create parent directory
    mkdir -p "$(dirname "$INSTALL_DIR")"

    # Clone the repository
    print_status "Cloning repository: $REPO_URL (branch: $BRANCH)"
    if ! git clone --branch "$BRANCH" --depth 1 "$REPO_URL" "$INSTALL_DIR"; then
        print_error "Failed to clone repository"
        exit 1
    fi

    # Change to installation directory
    cd "$INSTALL_DIR"

    # Check if install.py exists
    if [ ! -f "install.py" ]; then
        print_error "install.py not found in repository"
        exit 1
    fi

    # Make install.py executable
    chmod +x install.py

    # Run the installer
    print_status "Running MCP server installer..."
    if python3 install.py; then
        print_success "MCP server '$SERVER_NAME' installed successfully!"
        print_status "Installation location: $INSTALL_DIR"
        print_status ""
        print_status "The server has been configured for all supported MCP clients:"
        print_status "• Claude Desktop"
        print_status "• Cursor"
        print_status "• VS Code"
        print_status "• Cline"
        print_status "• Windsurf"
        print_status "• n8n"
        print_status "• 5ire"
        print_status ""
        print_status "You may need to restart your MCP clients for the changes to take effect."
    else
        print_error "Failed to install MCP server"
        exit 1
    fi
}

# Run main function with all arguments
main "$@" 