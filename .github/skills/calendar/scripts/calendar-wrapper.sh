#!/bin/bash

# =============================================================================
# Calendar Wrapper Script
# =============================================================================
# Routes calendar commands to local or remote execution based on .env config
#
# USAGE:
#   ./calendar-wrapper.sh <command> [options]
#   (Same arguments as calendar-cli.sh)
# =============================================================================

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Get script directory and project root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../../../.." && pwd)"
ENV_FILE="$PROJECT_ROOT/.env"

# =============================================================================
# Helper Functions
# =============================================================================

print_error() {
    echo -e "${RED}Error: $1${NC}" >&2
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_info() {
    echo -e "${CYAN}ℹ $1${NC}"
}

# =============================================================================
# Load Configuration
# =============================================================================

load_config() {
    if [ ! -f "$ENV_FILE" ]; then
        print_error ".env file not found at $ENV_FILE"
        exit 1
    fi
    
    # Load calendar section variables
    PROJECT_LOCATION=$(grep -E "^CALENDAR_PROJECT_LOCATION=" "$ENV_FILE" | cut -d'=' -f2- | tr -d '"' | tr -d "'")
    LOCAL_SSH_HOST=$(grep -E "^CALENDAR_LOCAL_SSH_HOST=" "$ENV_FILE" | cut -d'=' -f2- | tr -d '"' | tr -d "'")
    LOCAL_SSH_USER=$(grep -E "^CALENDAR_LOCAL_SSH_USER=" "$ENV_FILE" | cut -d'=' -f2- | tr -d '"' | tr -d "'")
    LOCAL_IP=$(grep -E "^CALENDAR_LOCAL_IP=" "$ENV_FILE" | cut -d'=' -f2- | tr -d '"' | tr -d "'")
    CALENDAR_CLI_PATH=$(grep -E "^CALENDAR_CLI_PATH=" "$ENV_FILE" | cut -d'=' -f2- | tr -d '"' | tr -d "'")
    
    # Set defaults
    if [ -z "$PROJECT_LOCATION" ]; then
        PROJECT_LOCATION="local"
    fi
    
    if [ -z "$CALENDAR_CLI_PATH" ]; then
        CALENDAR_CLI_PATH="$SCRIPT_DIR/calendar-cli.sh"
    fi
}

# =============================================================================
# SSH Setup Check
# =============================================================================

check_ssh_setup() {
    # Check if SSH key exists
    if [ ! -f "$HOME/.ssh/id_rsa" ]; then
        print_error "SSH key not found. Please run the SSH setup first:"
        echo "  bash $SCRIPT_DIR/setup-ssh.sh"
        exit 1
    fi
    
    # Check if config exists
    if [ ! -f "$HOME/.ssh/config" ]; then
        print_error "SSH config not found. Please run the SSH setup first:"
        echo "  bash $SCRIPT_DIR/setup-ssh.sh"
        exit 1
    fi
    
    # Check if we can connect
    if [ -n "$LOCAL_SSH_HOST" ]; then
        if ! ssh -o BatchMode=yes -o ConnectTimeout=5 "$LOCAL_SSH_HOST" "echo 'SSH connection successful'" >/dev/null 2>&1; then
            print_error "Cannot connect to $LOCAL_SSH_HOST. Please verify:"
            echo "  1. Your local machine is powered on and connected to the network"
            echo "  2. SSH is enabled on your local machine (System Settings > General > Sharing > Remote Login)"
            echo "  3. Your public key is in ~/.ssh/authorized_keys on the local machine"
            echo "  4. The IP address in .env is correct"
            echo ""
            echo "To reconfigure SSH, run: bash $SCRIPT_DIR/setup-ssh.sh"
            exit 1
        fi
    else
        print_error "CALENDAR_LOCAL_SSH_HOST not set in .env. Please run SSH setup:"
        echo "  bash $SCRIPT_DIR/setup-ssh.sh"
        exit 1
    fi
}

# =============================================================================
# Main Execution
# =============================================================================

main() {
    load_config
    
    if [ "$PROJECT_LOCATION" = "local" ]; then
        # Local execution - run calendar-cli.sh directly
        bash "$CALENDAR_CLI_PATH" "$@"
    elif [ "$PROJECT_LOCATION" = "remote" ]; then
        # Remote execution - verify SSH setup and run via SSH
        check_ssh_setup
        
        # Build the remote command
        # We need to escape arguments properly for SSH
        local args=""
        for arg in "$@"; do
            # Escape single quotes and wrap in single quotes
            local escaped_arg="${arg//\'/\'\\\'\'}"
            args="$args '$escaped_arg'"
        done
        
        # Execute on local machine via SSH
        ssh "$LOCAL_SSH_HOST" "bash '$CALENDAR_CLI_PATH' $args"
    else
        print_error "Invalid CALENDAR_PROJECT_LOCATION in .env: '$PROJECT_LOCATION'"
        echo "Must be either 'local' or 'remote'"
        exit 1
    fi
}

main "$@"
