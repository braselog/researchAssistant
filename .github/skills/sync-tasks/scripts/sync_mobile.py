#!/usr/bin/env python3
"""
Bidirectional sync between tasks.md and GitHub Projects.
Handles task content, status, and priority synchronization.
"""
import argparse
import json
import subprocess
import sys
import os
import re
from pathlib import Path

# Check for required packages
try:
    from dotenv import load_dotenv
    import yaml
except ImportError:
    print("❌ Error: Required packages not installed")
    print("\nPlease install dependencies:")
    print("  conda run -n research-assistant pip install python-dotenv PyYAML")
    sys.exit(1)

# Load configuration
SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent
PROJECT_ROOT = SKILL_DIR.parent.parent.parent

# Load .env from project root
ENV_FILE = PROJECT_ROOT / ".env"
if not ENV_FILE.exists():
    print(f"❌ Error: .env file not found at {ENV_FILE}")
    print("\nPlease create .env from example:")
    print(f"  cp {PROJECT_ROOT}/.env_example{ENV_FILE}")
    sys.exit(1)

load_dotenv(ENV_FILE)

# Load configuration from .env
ORG_NAME = os.getenv("GITHUB_ORG_NAME", "").strip()
PROJECT_NUM = os.getenv("GITHUB_PROJECT_NUM", "").strip()
FILE_NAME = os.getenv("GITHUB_TASKS_FILE", "tasks.md").strip()

# Check if initialization is needed
GH_YAML = SKILL_DIR / "gh.yaml"
needs_init = False

if not ORG_NAME or not PROJECT_NUM:
    print("⚙️  GitHub configuration incomplete - running initialization...")
    needs_init = True
elif not GH_YAML.exists():
    print("⚙️  GitHub project configuration not found - running initialization...")
    needs_init = True

# Run initialization if needed
if needs_init:
    init_script = SKILL_DIR / "scripts" / "init_config.py"
    print(f"\nRunning: {init_script}\n")
    print("=" * 70)
    
    result = subprocess.run(
        [sys.executable, str(init_script)],
        cwd=str(PROJECT_ROOT)
    )
    
    print("=" * 70)
    
    if result.returncode != 0:
        print("\n❌ Initialization failed")
        sys.exit(1)
    
    # Reload .env after initialization
    print("\n✓ Initialization complete, reloading configuration...\n")
    load_dotenv(ENV_FILE, override=True)
    ORG_NAME = os.getenv("GITHUB_ORG_NAME", "").strip()
    PROJECT_NUM = os.getenv("GITHUB_PROJECT_NUM", "").strip()
    FILE_NAME = os.getenv("GITHUB_TASKS_FILE", "tasks.md").strip()

# Load gh.yaml
try:
    with open(GH_YAML, 'r') as f:
        gh_config = yaml.safe_load(f)
    
    PROJECT_ID = gh_config["PROJECT_ID"]
    STATUS_FIELD_ID = gh_config["STATUS_FIELD_ID"]
    PRIORITY_FIELD_ID = gh_config["PRIORITY_FIELD_ID"]
    STATUS_OPTION_IDS = gh_config["STATUS_OPTION_IDS"]
    PRIORITY_OPTION_IDS = gh_config["PRIORITY_OPTION_IDS"]
except (KeyError, TypeError, FileNotFoundError) as e:
    print(f"❌ Error: Failed to load gh.yaml: {e}")
    print("\nConfiguration may be corrupted. Please delete gh.yaml and try again:")
    print(f"  rm {GH_YAML}")
    print(f"  python3 {SCRIPT_DIR / 'sync_mobile.py'}")
    sys.exit(1)


def run_gh_command(args):
    """Run a GitHub CLI command and return JSON result."""
    try:
        result = subprocess.run(
            args,
            capture_output=True,
            text=True,
            check=True
        )
        return json.loads(result.stdout) if result.stdout.strip() else None
    except subprocess.CalledProcessError as e:
        print(f"   ⚠️  Command failed: {' '.join(args)}", file=sys.stderr)
        print(f"   Error: {e.stderr}", file=sys.stderr)
        return None
    except json.JSONDecodeError:
        print(f"   ⚠️  Failed to parse JSON output", file=sys.stderr)
        return None


def parse_tasks_md():
    """Parse tasks.md and return dict of sections with their tasks."""
    with open(FILE_NAME, 'r') as f:
        lines = f.readlines()
    
    sections = {}
    current_section = None
    
    for line in lines:
        if line.startswith('## '):
            current_section = line.strip()[3:]
            sections[current_section] = []
        elif current_section:
            match = re.match(r'- \[([ x])\] (.+)', line.strip())
            if match:
                checked = match.group(1) == 'x'
                task_text = match.group(2)
                
                # Extract priority if present
                priority_match = re.search(r' - \*\*(P[0-2])\*\*$', task_text)
                priority = priority_match.group(1) if priority_match else None
                
                # Remove priority from title
                title = re.sub(r' - \*\*P[0-2]\*\*$', '', task_text)
                
                sections[current_section].append({
                    'title': title,
                    'priority': priority,
                    'checked': checked,
                    'line': line
                })
    
    return sections


def update_task_in_file(title, target_section, priority=None, checked=False):
    """Move or add a task to a specific section in tasks.md."""
    with open(FILE_NAME, 'r') as f:
        lines = f.readlines()
    
    # Find and remove the task
    task_line = None
    new_lines = []
    for line in lines:
        match = re.match(r'- \[([ x])\] (.+)', line.strip())
        if match and title in match.group(2):
            task_line = line
        else:
            new_lines.append(line)
    
    if not task_line:
        # New task - create it with priority and checked status
        priority_suffix = f" - **{priority}**" if priority else ""
        checked_str = "[x]" if checked else "[ ]"
        task_line = f"- {checked_str} {title}{priority_suffix}\n"
    else:
        # Existing task - update priority and checked status
        # Extract the task text (everything after "- [x] " or "- [ ] ")
        match = re.match(r'- \[([ x])\] (.+)', task_line.strip())
        if match:
            task_text = match.group(2)
            # Remove any existing priority
            task_text = re.sub(r' - \*\*P[0-2]\*\*$', '', task_text)
            priority_suffix = f" - **{priority}**" if priority else ""
            checked_str = "[x]" if checked else "[ ]"
            task_line = f"- {checked_str} {task_text}{priority_suffix}\n"
    
    # Insert task in target section
    final_lines = []
    i = 0
    while i < len(new_lines):
        line = new_lines[i]
        final_lines.append(line)
        
        if line.strip() == f"## {target_section}":
            # Skip existing blank lines after header
            i += 1
            while i < len(new_lines) and new_lines[i].strip() == '':
                i += 1
            # Add proper spacing: blank line, task, blank line
            final_lines.append('\n')
            final_lines.append(task_line)
            final_lines.append('\n')
            continue
        i += 1
    
    with open(FILE_NAME, 'w') as f:
        f.writelines(final_lines)


def pull_from_github(update_existing=True):
    """Pull draft issues from GitHub and update tasks.md.
    
    Args:
        update_existing: If True, update existing tasks. If False, only add new tasks.
    """
    print("📥 PULL: Fetching draft issues FROM GitHub...")
    
    # Get all items from GitHub project
    data = run_gh_command([
        'gh', 'project', 'item-list', PROJECT_NUM,
        '--owner', ORG_NAME,
        '--format', 'json'
    ])
    
    if not data or 'items' not in data:
        print("   ✓ No items found in GitHub project")
        return 0
    
    # Parse current tasks.md
    local_sections = parse_tasks_md()
    local_tasks = {}
    for section, tasks in local_sections.items():
        for task in tasks:
            local_tasks[task['title']] = {'section': section, 'priority': task['priority'], 'checked': task['checked']}
    
    pulled_count = 0
    
    # Process each draft issue
    for item in data['items']:
        if item.get('content', {}).get('type') != 'DraftIssue':
            continue
        
        title = item['title']
        github_status = item.get('status', 'Backlog')
        github_priority = item.get('priority')  # Get priority from GitHub
        local_status = github_status  # Status names match exactly
        
        current_task = local_tasks.get(title)
        
        if current_task is None:
            # New task from GitHub
            priority_str = f" ({github_priority})" if github_priority else ""
            checked = (local_status == "Done")
            print(f"   → Adding new task '{title}' to '{local_status}'{priority_str}")
            update_task_in_file(title, local_status, github_priority, checked=checked)
            pulled_count += 1
        elif update_existing:
            current_section = current_task['section']
            current_priority = current_task['priority']
            current_checked = current_task['checked']
            
            # Check if status or priority changed
            status_changed = current_section != local_status
            # Only consider priority changed if GitHub has a value AND it's different
            priority_changed = github_priority is not None and current_priority != github_priority
            checked_changed = current_checked != (local_status == "Done")
            
            if status_changed or priority_changed or checked_changed:
                changes = []
                if status_changed:
                    changes.append(f"status: {current_section} → {local_status}")
                if priority_changed:
                    old_p = current_priority or "none"
                    new_p = github_priority or "none"
                    changes.append(f"priority: {old_p} → {new_p}")
                if checked_changed:
                    old_c = "checked" if current_checked else "unchecked"
                    new_c = "checked" if (local_status == "Done") else "unchecked"
                    changes.append(f"checked: {old_c} → {new_c}")
                print(f"   → Updating task '{title}' ({', '.join(changes)})")
                # Preserve local priority if GitHub doesn't have one
                final_priority = github_priority if github_priority is not None else current_priority
                final_checked = (local_status == "Done")
                update_task_in_file(title, local_status, final_priority, checked=final_checked)
                pulled_count += 1
    
    print(f"   ✓ Pulled/updated {pulled_count} tasks from GitHub")
    return pulled_count


def push_to_github(update_existing=True):
    """Push tasks from tasks.md to GitHub (creates new items and updates existing ones).
    
    Args:
        update_existing: If True, update existing tasks. If False, only create new tasks.
    """
    print("")
    print("📤 PUSH: Syncing tasks TO GitHub...")
    
    # Get existing GitHub draft issues with their details
    data = run_gh_command([
        'gh', 'project', 'item-list', PROJECT_NUM,
        '--owner', ORG_NAME,
        '--format', 'json'
    ])
    
    github_items = {}
    if data and 'items' in data:
        for item in data['items']:
            if item.get('content', {}).get('type') == 'DraftIssue':
                github_items[item['title']] = {
                    'id': item['id'],
                    'status': item.get('status', 'Backlog'),
                    'priority': item.get('priority')
                }
    
    # Parse local tasks
    local_sections = parse_tasks_md()
    created_count = 0
    updated_count = 0
    
    for section, tasks in local_sections.items():
        # Validate section is a known status
        valid_statuses = list(STATUS_OPTION_IDS.keys())
        if section not in valid_statuses:
            continue
        
        for task in tasks:
            title = task['title']
            priority = task['priority']
            checked = task['checked']
            
            # Determine GitHub status: if checked, force to "Done", else use section
            github_status = "Done" if checked else section
            
            if title in github_items:
                # Task exists - check if status or priority needs updating
                item_id = github_items[title]['id']
                current_github_status = github_items[title]['status']
                current_github_priority = github_items[title]['priority']
                
                if not update_existing:
                    # Skip updating existing tasks when update_existing is False
                    continue
                
                needs_update = False
                updates = []
                
                # Check if status changed
                if current_github_status != github_status:
                    needs_update = True
                    updates.append(f"status: {current_github_status} → {github_status}")
                
                # Check if priority changed (tasks.md is source of truth)
                if priority != current_github_priority:
                    needs_update = True
                    old_p = current_github_priority or "none"
                    new_p = priority or "none"
                    updates.append(f"priority: {old_p} → {new_p}")
                
                if needs_update:
                    print(f"   → Updating: {title} ({', '.join(updates)})")
                    
                    # Update status if changed
                    if current_github_status != github_status:
                        status_option_id = STATUS_OPTION_IDS.get(github_status)
                        if status_option_id:
                            subprocess.run([
                                'gh', 'project', 'item-edit',
                                '--id', item_id,
                                '--project-id', PROJECT_ID,
                                '--field-id', STATUS_FIELD_ID,
                                '--single-select-option-id', status_option_id
                            ], capture_output=True)
                    
                    # Set/update priority if present
                    if priority:
                        priority_option_id = PRIORITY_OPTION_IDS.get(priority)
                        if priority_option_id:
                            print(f"      Setting priority {priority} (option ID: {priority_option_id})")
                            result = subprocess.run([
                                'gh', 'project', 'item-edit',
                                '--id', item_id,
                                '--project-id', PROJECT_ID,
                                '--field-id', PRIORITY_FIELD_ID,
                                '--single-select-option-id', priority_option_id
                            ], capture_output=True, text=True)
                            if result.returncode != 0:
                                print(f"      ⚠️  Failed to set priority: {result.stderr}")
                        else:
                            print(f"      ⚠️  Unknown priority: {priority}")
                    elif current_github_priority:
                        # Clear priority if it was removed from tasks.md
                        print(f"      Clearing priority")
                        result = subprocess.run([
                            'gh', 'project', 'item-edit',
                            '--id', item_id,
                            '--project-id', PROJECT_ID,
                            '--field-id', PRIORITY_FIELD_ID,
                            '--clear'
                        ], capture_output=True, text=True)
                        if result.returncode != 0:
                            print(f"      ⚠️  Failed to clear priority: {result.stderr}")
                    
                    updated_count += 1
            else:
                # New task - create it
                priority_str = f", Priority: {priority}" if priority else ""
                checked_str = ", Checked" if checked else ""
                print(f"   → Creating: {title} (Status: {github_status}{priority_str}{checked_str})")
                
                # Create draft issue
                result = run_gh_command([
                    'gh', 'project', 'item-create', PROJECT_NUM,
                    '--owner', ORG_NAME,
                    '--title', title,
                    '--format', 'json'
                ])
                
                if not result or 'id' not in result:
                    print(f"   ⚠️  Failed to create: {title}")
                    continue
                
                item_id = result['id']
                
                # Set status
                status_option_id = STATUS_OPTION_IDS.get(github_status)
                if status_option_id:
                    subprocess.run([
                        'gh', 'project', 'item-edit',
                        '--id', item_id,
                        '--project-id', PROJECT_ID,
                        '--field-id', STATUS_FIELD_ID,
                        '--single-select-option-id', status_option_id
                    ], capture_output=True)
                
                # Set priority if present
                if priority:
                    priority_option_id = PRIORITY_OPTION_IDS.get(priority)
                    if priority_option_id:
                        print(f"      Setting priority {priority} (option ID: {priority_option_id})")
                        result = subprocess.run([
                            'gh', 'project', 'item-edit',
                            '--id', item_id,
                            '--project-id', PROJECT_ID,
                            '--field-id', PRIORITY_FIELD_ID,
                            '--single-select-option-id', priority_option_id
                        ], capture_output=True, text=True)
                        if result.returncode != 0:
                            print(f"      ⚠️  Failed to set priority: {result.stderr}")
                    else:
                        print(f"      ⚠️  Unknown priority: {priority}")
                
                created_count += 1
    
    if created_count == 0 and updated_count == 0:
        print("   ✓ Everything in sync")
    else:
        if created_count > 0:
            print(f"   ✓ Created {created_count} new tasks")
        if updated_count > 0:
            print(f"   ✓ Updated {updated_count} tasks")
    
    return created_count + updated_count


def main():
    parser = argparse.ArgumentParser(
        description='Sync tasks.md with GitHub Projects',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Priority modes:
  github    GitHub takes precedence (your changes on mobile override local)
  local     tasks.md takes precedence (your local changes override GitHub)
  (none)    Bidirectional sync (both sources can update each other)

Examples:
  python sync_mobile.py                # Bidirectional sync
  python sync_mobile.py github         # GitHub has priority
  python sync_mobile.py local          # Local has priority
        ''')
    parser.add_argument('priority', nargs='?', choices=['github', 'local'], 
                       help='Which source takes precedence during conflicts')
    
    args = parser.parse_args()
    
    if args.priority == 'github':
        print("🔄 Starting sync (GitHub priority mode)...")
        print("   GitHub changes will override local changes")
        print("")
        # Pull first with updates, then push only new tasks
        pull_from_github(update_existing=True)
        push_to_github(update_existing=False)
        print("")
        print("✅ Sync complete!")
        print("📋 GitHub changes applied to tasks.md")
        
    elif args.priority == 'local':
        print("🔄 Starting sync (Local priority mode)...")
        print("   Local changes will override GitHub changes")
        print("")
        # Push first with updates, then pull only new tasks
        push_to_github(update_existing=True)
        pull_from_github(update_existing=False)
        print("")
        print("✅ Sync complete!")
        print("📋 Local changes applied to GitHub")
        
    else:
        print("🔄 Starting bidirectional sync...")
        print("   Both sources can update each other")
        print("")
        # PUSH FIRST - tasks.md is the source of truth for local changes
        # This ensures if you move a task locally, it gets updated in GitHub
        push_to_github(update_existing=True)
        
        # THEN PULL - get any new tasks created in GitHub mobile
        pull_from_github(update_existing=True)
        
        print("")
        print("✅ Sync complete!")
        print("📋 Bidirectional sync - both sources updated")


if __name__ == "__main__":
    main()
