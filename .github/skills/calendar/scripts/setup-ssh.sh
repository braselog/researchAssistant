#!/bin/bash

# =============================================================================
# SSH Setup Script for Remote Calendar Access
# =============================================================================
# Automates passwordless SSH authentication setup from remote to local machine
#
# USAGE:
#   bash setup-ssh.sh
# =============================================================================

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color
BOLD='\033[1m'

# Get script directory and project root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../../../.." && pwd)"
ENV_FILE="$PROJECT_ROOT/.env"

# =============================================================================
# Helper Functions
# =============================================================================

print_header() {
    echo -e "${BOLD}${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${BOLD}${BLUE}  $1${NC}"
    echo -e "${BOLD}${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
}

print_error() {
    echo -e "${RED}Error: $1${NC}" >&2
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_info() {
    echo -e "${CYAN}ℹ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

# =============================================================================
# Step 1: Check/Generate SSH Key
# =============================================================================

check_or_generate_key() {
    print_header "Step 1: SSH Key Setup"
    
    if [ -f "$HOME/.ssh/id_rsa" ]; then
        print_success "SSH key already exists at ~/.ssh/id_rsa"
    else
        print_info "Generating new RSA 4096-bit SSH key..."
        mkdir -p "$HOME/.ssh"
        chmod 700 "$HOME/.ssh"
        ssh-keygen -t rsa -b 4096 -f "$HOME/.ssh/id_rsa" -N "" -C "researchAssistant-remote-access"
        print_success "SSH key generated successfully"
    fi
    
    echo ""
}

# =============================================================================
# Step 2: Display Public Key
# =============================================================================

display_public_key() {
    print_header "Step 2: Public Key"
    
    echo -e "${BOLD}Copy this public key:${NC}"
    echo ""
    echo -e "${CYAN}───────────────────────────────────────────────────${NC}"
    cat "$HOME/.ssh/id_rsa.pub"
    echo -e "${CYAN}───────────────────────────────────────────────────${NC}"
    echo ""
}

# =============================================================================
# Step 3: Get Local Machine Details
# =============================================================================

get_local_machine_info() {
    print_header "Step 3: Local Machine Configuration"
    
    # Ask for local username with default to current user
    echo -ne "${BOLD}Enter your username on the local machine: ${NC}"
    echo ""
    echo -e "${CYAN}(Default: $USER)${NC}"
    read -r LOCAL_USER
    
    # Use current username if blank
    if [ -z "$LOCAL_USER" ]; then
        LOCAL_USER="$USER"
        print_info "Using current username: $LOCAL_USER"
    fi
    
    # Check .env file for existing IP address
    LOCAL_IP=""
    if [ -f "$ENV_FILE" ] && grep -q "^CALENDAR_LOCAL_IP=" "$ENV_FILE" 2>/dev/null; then
        LOCAL_IP=$(grep "^CALENDAR_LOCAL_IP=" "$ENV_FILE" | cut -d'=' -f2 | tr -d ' ')
        print_success "Found IP address in .env: $LOCAL_IP"
    fi
    
    # If no IP found in .env, ask for it
    if [ -z "$LOCAL_IP" ]; then
        echo -ne "${BOLD}Enter the local machine's IP address: ${NC}"
        read -r LOCAL_IP
    fi
    
    # Ask for calendar-cli.sh path on local machine
    echo -ne "${BOLD}Enter the full path to calendar-cli.sh on local machine: ${NC}"
    echo ""
    echo -e "${CYAN}(Default: /Users/$LOCAL_USER/Documents/researchAssistant/.github/skills/calendar/scripts/calendar-cli.sh)${NC}"
    read -r CALENDAR_CLI_PATH
    
    if [ -z "$CALENDAR_CLI_PATH" ]; then
        CALENDAR_CLI_PATH="/Users/$LOCAL_USER/Documents/researchAssistant/.github/skills/calendar/scripts/calendar-cli.sh"
    fi
    
    echo ""
    print_info "Configuration:"
    echo "  Username: $LOCAL_USER"
    echo "  IP Address: $LOCAL_IP"
    echo "  Calendar CLI Path: $CALENDAR_CLI_PATH"
    echo ""
}

# =============================================================================
# Step 4: Configure SSH Config
# =============================================================================

configure_ssh_config() {
    print_header "Step 4: SSH Configuration"
    
    # Ensure ~/.ssh directory exists with correct permissions
    mkdir -p "$HOME/.ssh"
    chmod 700 "$HOME/.ssh"
    
    local CONFIG_FILE="$HOME/.ssh/config"
    local HOST_ALIAS="local-pc"
    
    # Check if local-pc entry already exists
    if grep -q "^Host $HOST_ALIAS" "$CONFIG_FILE" 2>/dev/null; then
        print_warning "Host alias '$HOST_ALIAS' already exists in ~/.ssh/config"
        echo -ne "${BOLD}Do you want to update it? (y/n): ${NC}"
        read -r UPDATE_CHOICE
        
        if [ "$UPDATE_CHOICE" != "y" ] && [ "$UPDATE_CHOICE" != "Y" ]; then
            print_info "Keeping existing configuration"
            return
        fi
        
        # Remove existing entry
        # Create a temporary file without the old entry
        awk -v host="$HOST_ALIAS" '
            /^Host / { in_block = ($2 == host) }
            !in_block { print }
            /^$/ { in_block = 0 }
        ' "$CONFIG_FILE" > "$CONFIG_FILE.tmp"
        mv "$CONFIG_FILE.tmp" "$CONFIG_FILE"
    fi
    
    # Append new configuration
    cat >> "$CONFIG_FILE" <<CONFIG

Host $HOST_ALIAS
    HostName $LOCAL_IP
    User $LOCAL_USER
    IdentityFile ~/.ssh/id_rsa
    StrictHostKeyChecking no
    UserKnownHostsFile=/dev/null
CONFIG
    
    chmod 600 "$CONFIG_FILE"
    print_success "SSH config updated with alias '$HOST_ALIAS'"
    echo ""
}

# =============================================================================
# Step 5: Authorize Key on Local Machine
# =============================================================================

authorize_key_on_local() {
    print_header "Step 5: Authorize Key on Local Machine"
    
    echo "Now we need to add your public key to the local machine's authorized_keys."
    echo ""
    print_info "Attempting to copy SSH key to $LOCAL_USER@$LOCAL_IP..."
    echo ""
    print_warning "You will be prompted for your password on the local machine."
    echo ""
    
    # Try ssh-copy-id first (cleaner method)
    if command -v ssh-copy-id >/dev/null 2>&1; then
        print_info "Using ssh-copy-id..."
        if ssh-copy-id -i "$HOME/.ssh/id_rsa.pub" "$LOCAL_USER@$LOCAL_IP" 2>/dev/null; then
            print_success "SSH key successfully copied to local machine!"
            echo ""
            return 0
        else
            print_warning "ssh-copy-id failed, trying alternative method..."
        fi
    fi
    
    # Fallback: manually copy via ssh
    print_info "Copying key via SSH..."
    if cat "$HOME/.ssh/id_rsa.pub" | ssh "$LOCAL_USER@$LOCAL_IP" "mkdir -p ~/.ssh && chmod 700 ~/.ssh && cat >> ~/.ssh/authorized_keys && chmod 600 ~/.ssh/authorized_keys && echo 'Key added successfully'"; then
        print_success "SSH key successfully added to local machine!"
        echo ""
        return 0
    else
        print_error "Failed to copy SSH key to local machine"
        echo ""
        echo "Please ensure:"
        echo "  1. Your local machine is powered on and network-accessible"
        echo "  2. SSH/Remote Login is enabled (System Settings > General > Sharing > Remote Login)"
        echo "  3. The username and IP address are correct"
        echo "  4. You entered the correct password"
        echo ""
        print_warning "You can retry this setup or copy the key manually."
        return 1
    fi
}

# =============================================================================
# Step 6: Test Connection
# =============================================================================

test_ssh_connection() {
    print_header "Step 6: Test SSH Connection"
    
    print_info "Testing connection to local-pc..."
    
    if ssh -o BatchMode=yes -o ConnectTimeout=10 local-pc "echo 'Connection successful'" 2>/dev/null; then
        print_success "SSH connection to local-pc is working!"
        echo ""
        return 0
    else
        print_error "Cannot connect to local-pc"
        echo ""
        echo "Troubleshooting steps:"
        echo "  1. Verify your local machine is powered on and connected"
        echo "  2. Check if SSH/Remote Login is enabled on local machine:"
        echo "     System Settings > General > Sharing > Remote Login"
        echo "  3. Verify the public key was added correctly to ~/.ssh/authorized_keys"
        echo "  4. Check if the IP address is correct"
        echo "  5. Try manually: ssh $LOCAL_USER@$LOCAL_IP"
        echo ""
        return 1
    fi
}

# =============================================================================
# Step 7: Test Calendar Access
# =============================================================================

test_calendar_access() {
    print_header "Step 7: Test Calendar Access"
    
    print_info "Testing calendar access on local machine..."
    
    if ssh local-pc "test -f '$CALENDAR_CLI_PATH' && echo 'exists'" | grep -q 'exists'; then
        print_success "calendar-cli.sh found on local machine"
        
        # Try to run a simple command
        print_info "Running test command: calendar-cli.sh calendars"
        echo ""
        if ssh local-pc "bash '$CALENDAR_CLI_PATH' calendars" 2>/dev/null; then
            echo ""
            print_success "Calendar access is working!"
        else
            print_warning "Calendar script exists but may need permissions or icalBuddy setup"
            echo "If you see permission errors above, run this on your local machine:"
            echo "  brew install ical-buddy"
        fi
    else
        print_error "calendar-cli.sh not found at: $CALENDAR_CLI_PATH"
        echo "Please verify the path on your local machine"
    fi
    
    echo ""
}

# =============================================================================
# Step 8: Update .env File
# =============================================================================

update_env_file() {
    print_header "Step 8: Update .env Configuration"
    
    if [ ! -f "$ENV_FILE" ]; then
        print_error ".env file not found at $ENV_FILE"
        return 1
    fi
    
    # Check if calendar section exists
    if ! grep -q "^# CALENDAR REMOTE ACCESS" "$ENV_FILE" 2>/dev/null; then
        # Add calendar remote access section
        cat >> "$ENV_FILE" <<ENVCONFIG

# =============================================================================
# CALENDAR REMOTE ACCESS
# =============================================================================

# Project location: local (default) or remote
# When set to 'remote', calendar commands will be executed via SSH to local machine
CALENDAR_PROJECT_LOCATION=remote

# SSH host alias (from ~/.ssh/config)
CALENDAR_LOCAL_SSH_HOST=local-pc

# Local machine username
CALENDAR_LOCAL_SSH_USER=$LOCAL_USER

# Local machine IP address
CALENDAR_LOCAL_IP=$LOCAL_IP

# Path to calendar-cli.sh on local machine
CALENDAR_CLI_PATH=$CALENDAR_CLI_PATH

ENVCONFIG
        print_success ".env file updated with calendar remote access configuration"
    else
        # Update existing values
        sed -i.bak "s|^CALENDAR_PROJECT_LOCATION=.*|CALENDAR_PROJECT_LOCATION=remote|" "$ENV_FILE"
        sed -i.bak "s|^CALENDAR_LOCAL_SSH_HOST=.*|CALENDAR_LOCAL_SSH_HOST=local-pc|" "$ENV_FILE"
        sed -i.bak "s|^CALENDAR_LOCAL_SSH_USER=.*|CALENDAR_LOCAL_SSH_USER=$LOCAL_USER|" "$ENV_FILE"
        sed -i.bak "s|^CALENDAR_LOCAL_IP=.*|CALENDAR_LOCAL_IP=$LOCAL_IP|" "$ENV_FILE"
        sed -i.bak "s|^CALENDAR_CLI_PATH=.*|CALENDAR_CLI_PATH=$CALENDAR_CLI_PATH|" "$ENV_FILE"
        rm -f "$ENV_FILE.bak"
        print_success ".env file updated"
    fi
    
    echo ""
    print_info "Configuration saved to .env:"
    echo "  CALENDAR_PROJECT_LOCATION=remote"
    echo "  CALENDAR_LOCAL_SSH_HOST=local-pc"
    echo "  CALENDAR_LOCAL_SSH_USER=$LOCAL_USER"
    echo "  CALENDAR_LOCAL_IP=$LOCAL_IP"
    echo "  CALENDAR_CLI_PATH=$CALENDAR_CLI_PATH"
    echo ""
}

# =============================================================================
# Main Setup Flow
# =============================================================================

main() {
    print_header "Calendar Remote Access Setup"
    echo ""
    echo "This script will configure passwordless SSH access from this remote"
    echo "machine to your local machine for calendar integration."
    echo ""
    echo -ne "${BOLD}Press Enter to begin...${NC}"
    read -r
    echo ""
    
    # Execute setup steps
    check_or_generate_key
    display_public_key
    get_local_machine_info
    configure_ssh_config
    
    # Try to authorize key (returns 0 on success, 1 on failure)
    if ! authorize_key_on_local; then
        print_error "Setup failed at key authorization step"
        echo ""
        echo "The public key shown in Step 2 can be manually added if needed:"
        cat "$HOME/.ssh/id_rsa.pub"
        echo ""
        exit 1
    fi
    
    # Test connection
    if test_ssh_connection; then
        test_calendar_access
        update_env_file
        
        print_header "Setup Complete!"
        echo ""
        print_success "Calendar remote access is now configured!"
        echo ""
        echo "Next steps:"
        echo "  1. The wrapper script will now use SSH to access your local calendar"
        echo "  2. All calendar commands will work transparently"
        echo "  3. Make sure your local machine is powered on when using calendar features"
        echo ""
        echo "To switch back to local mode, edit .env and set:"
        echo "  CALENDAR_PROJECT_LOCATION=local"
        echo ""
    else
        print_warning "Setup completed but SSH connection test failed"
        echo ""
        echo "Please resolve the connection issues and run this script again,"
        echo "or test manually with: ssh local-pc"
        echo ""
    fi
}

main "$@"
