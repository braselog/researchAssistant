#!/usr/bin/env python3
"""
Initialize GitHub Project sync configuration.

This script:
1. Checks .env for GITHUB_ORG_NAME and GITHUB_PROJECT_NUM
2. Prompts for missing values and updates .env
3. Uses gh CLI to discover project IDs and field configurations
4. Generates gh.yaml with discovered values
"""

import os
import sys
import json
import subprocess
from pathlib import Path
from typing import Dict, Optional

try:
    from dotenv import load_dotenv, set_key
    import yaml
except ImportError:
    print("❌ Error: Required packages not installed")
    print("\nPlease install dependencies:")
    print("  conda run -n research-assistant pip install python-dotenv PyYAML")
    sys.exit(1)


class ConfigInitializer:
    def __init__(self):
        self.project_root = Path(__file__).resolve().parents[4]
        self.skill_dir = Path(__file__).resolve().parent.parent
        self.env_file = self.project_root / ".env"
        self.gh_yaml = self.skill_dir / "gh.yaml"
        self.gh_template = self.skill_dir / "gh_template.yaml"
        
        # Load existing .env
        if self.env_file.exists():
            load_dotenv(self.env_file)
        else:
            print(f"❌ Error: .env file not found at {self.env_file}")
            print("\nPlease create .env from .env_example first:")
            print(f"  cp {self.project_root}/.env_example {self.env_file}")
            sys.exit(1)
    
    def get_or_prompt_env_var(self, var_name: str, prompt: str, allow_empty: bool = False) -> str:
        """Get value from .env or prompt user if empty."""
        value = os.getenv(var_name, "").strip()
        
        if value:
            print(f"✓ {var_name} found in .env: {value}")
            return value
        
        # Prompt for value
        while True:
            value = input(f"\n{prompt}: ").strip()
            if value or allow_empty:
                break
            print("⚠️  This field is required. Please enter a value.")
        
        # Update .env file
        if value and value != '0':
            print(f"  Updating .env with {var_name}={value}")
            set_key(str(self.env_file), var_name, value)
        
        return value
    
    def run_gh_command(self, args: list) -> Dict:
        """Run gh CLI command and return JSON output."""
        cmd = ["gh"] + args
        
        print(f"  Running: {' '.join(args[:4])}...")
        
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True
            )
            return json.loads(result.stdout)
        except subprocess.CalledProcessError as e:
            print(f"❌ Error running gh command: {e}")
            print(f"   stdout: {e.stdout}")
            print(f"   stderr: {e.stderr}")
            sys.exit(1)
        except json.JSONDecodeError as e:
            print(f"❌ Error parsing JSON output: {e}")
            sys.exit(1)
    
    def get_user_login(self) -> str:
        """Get the authenticated user's GitHub login."""
        cmd = ["gh", "api", "user", "--jq", ".login"]
        
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            print(f"❌ Error getting user login: {e}")
            sys.exit(1)
    
    def list_organizations(self) -> list:
        """List organizations the user is a member of."""
        cmd = ["gh", "org", "list"]
        
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True
            )
            # Parse org list - each line is an org name
            orgs = [line.strip() for line in result.stdout.strip().split('\n') if line.strip()]
            return orgs
        except subprocess.CalledProcessError as e:
            # User might not be part of any orgs
            return []
    
    def prompt_for_owner(self) -> str:
        """Prompt user to select owner (personal account or organization)."""
        print("\n📋 Select the owner for your GitHub Project:")
        print()
        
        # Get user login
        user_login = self.get_user_login()
        print(f"  [1] {user_login} (your personal account)")
        
        # Get organizations
        orgs = self.list_organizations()
        
        options = [user_login]
        if orgs:
            for i, org in enumerate(orgs, start=2):
                print(f"  [{i}] {org}")
                options.append(org)
        
        print()
        
        # Prompt for selection
        while True:
            choice = input(f"Enter your choice [1-{len(options)}]: ").strip()
            try:
                choice_num = int(choice)
                if 1 <= choice_num <= len(options):
                    selected = options[choice_num - 1]
                    print(f"  Selected: {selected}")
                    return selected
                else:
                    print(f"⚠️  Please enter a number between 1 and {len(options)}")
            except ValueError:
                print("⚠️  Please enter a valid number")
    
    def list_available_projects(self, org: str):
        """List available projects for the organization in table format."""
        owner_type = "your personal account" if org == self.get_user_login() else org
        print(f"\n📋 Available projects in {owner_type}:")
        print()
        
        cmd = ["gh", "project", "list", "--owner", org]
        
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True
            )
            # Parse and format the output to show only NUMBER and TITLE
            lines = result.stdout.strip().split('\n')
            if len(lines) > 1:
                # Skip header line and process project lines
                for line in lines:
                    parts = line.split('\t')
                    if len(parts) >= 2:
                        number = parts[0].strip()
                        title = parts[1].strip()
                        print(f"  [{number}] {title}")
                print()
            else:
                print("  No projects found.\n")

            print(f"  OR\n\n  [0] Create a new project")
        except subprocess.CalledProcessError as e:
            print(f"❌ Error listing projects: {e}")
            print(f"   stderr: {e.stderr}")
            print("\n⚠️  Could not list projects. You'll need to enter the project number manually.")
            if org == self.get_user_login():
                print(f"   Visit: https://github.com/users/{org}/projects to see your projects")
            else:
                print(f"   Visit: https://github.com/orgs/{org}/projects to see your projects")
    
    def discover_project_id(self, org: str, project_num: str) -> str:
        """Discover the project ID from org and project number."""
        print(f"\n🔍 Discovering project ID for {org}/projects/{project_num}...")
        
        # List all projects for the org
        data = self.run_gh_command([
            "project", "list",
            "--owner", org,
            "--format", "json",
            "--limit", "100"
        ])
        
        projects = data.get("projects", [])
        
        # Find the project by number
        for project in projects:
            if str(project.get("number")) == str(project_num):
                project_id = project.get("id")
                print(f"✓ Found project ID: {project_id}")
                return project_id
        
        print(f"❌ Error: Could not find project {project_num} in organization {org}")
        print(f"   Available projects: {[p.get('number') for p in projects]}")
        sys.exit(1)
    
    def discover_field_ids(self, org: str, project_num: str) -> Dict:
        """Discover field IDs for Status and Priority."""
        print(f"\n🔍 Discovering field IDs...")
        
        data = self.run_gh_command([
            "project", "field-list", project_num,
            "--owner", org,
            "--format", "json"
        ])
        
        fields = data.get("fields", [])
        field_ids = {}
        
        for field in fields:
            field_name = field.get("name", "")
            field_id = field.get("id", "")
            
            if field_name == "Status":
                field_ids["status"] = field_id
                print(f"✓ Found Status field ID: {field_id}")
            elif field_name == "Priority":
                field_ids["priority"] = field_id
                print(f"✓ Found Priority field ID: {field_id}")
        
        if "status" not in field_ids:
            print("❌ Error: Could not find 'Status' field in project")
            sys.exit(1)
        
        if "priority" not in field_ids:
            # create board view
            view_cmd = [
                "gh", "project", "view", project_num,
                "--owner", org, "--format", "json" #TODO: create a board view in the project
            ]
            subprocess.run(
                view_cmd,
                capture_output=True,
                text=True,
                check=True
            )
            print("❌ Error: Could not find 'Priority' field in project")
            sys.exit(1)
        
        return field_ids
    
    def discover_field_options(self, org: str, project_num: str, field_name: str) -> Dict[str, str]:
        """Discover option IDs for a single-select field."""
        print(f"\n🔍 Discovering {field_name} option IDs...")
        
        data = self.run_gh_command([
            "project", "field-list", project_num,
            "--owner", org,
            "--format", "json"
        ])
        
        fields = data.get("fields", [])
        
        for field in fields:
            if field.get("name") == field_name:
                options = field.get("options", [])
                option_map = {}
                
                for option in options:
                    option_name = option.get("name", "")
                    option_id = option.get("id", "")
                    option_map[option_name] = option_id
                    print(f"✓ {option_name}: {option_id}")
                
                return option_map
        
        print(f"❌ Error: Could not find '{field_name}' field")
        sys.exit(1)
    
    def generate_gh_yaml(self, config: Dict):
        """Generate gh.yaml from template with discovered values."""
        print(f"\n📝 Generating {self.gh_yaml}...")
        
        # Read template
        if not self.gh_template.exists():
            print(f"❌ Error: Template not found at {self.gh_template}")
            sys.exit(1)
        
        with open(self.gh_template, 'r') as f:
            gh_config = yaml.safe_load(f)
        
        # Update with discovered values
        gh_config["PROJECT_ID"] = config["project_id"]
        gh_config["STATUS_FIELD_ID"] = config["status_field_id"]
        gh_config["PRIORITY_FIELD_ID"] = config["priority_field_id"]
        gh_config["STATUS_OPTION_IDS"] = config["status_options"]
        gh_config["PRIORITY_OPTION_IDS"] = config["priority_options"]
        
        # Write to gh.yaml
        with open(self.gh_yaml, 'w') as f:
            yaml.dump(gh_config, f, default_flow_style=False, sort_keys=False)
        
        print(f"✓ Configuration saved to {self.gh_yaml}")

    def create_new_project(self, org: str) -> str:
        """Create a new project and return its number."""
        print(f"\n🆕 Creating a new project in {org}...")
        
        project_name = ''
        while project_name == '':
            project_name = input("Enter the name for the new project: ").strip()
            if not project_name:
                print("❌ Error: Project name cannot be empty.")
        
        cmd = [
            "gh", "project", "create",
            "--owner", org,
            "--title", project_name,
            "--format", "json"
        ]
        
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True
            )
            project_data = json.loads(result.stdout)
            project_number = str(project_data.get("number"))
            print(f"✓ Created new project '{project_name}' with number: {project_number}")
            return project_number
        except subprocess.CalledProcessError as e:
            print(f"❌ Error creating new project: {e}")
            print(f"   stderr: {e.stderr}")
            sys.exit(1)
        except json.JSONDecodeError as e:
            print(f"❌ Error parsing JSON output: {e}")
            sys.exit(1)
    
    def run(self):
        """Run the full initialization process."""
        print("=" * 70)
        print("GitHub Project Sync - Configuration Initialization")
        print("=" * 70)
        
        # Step 1: Get or prompt for owner (personal account or org)
        org_name = os.getenv("GITHUB_ORG_NAME", "").strip()
        if org_name:
            print(f"✓ GITHUB_ORG_NAME found in .env: {org_name}")
        else:
            org_name = self.prompt_for_owner()
            print(f"  Updating .env with GITHUB_ORG_NAME={org_name}")
            set_key(str(self.env_file), "GITHUB_ORG_NAME", org_name)
        
        # Step 2: Get or prompt for project number
        # If not already set, list available projects first
        if not os.getenv("GITHUB_PROJECT_NUM", "").strip():
            self.list_available_projects(org_name)
        
        project_num = self.get_or_prompt_env_var(
            "GITHUB_PROJECT_NUM",
            f"Enter your project NUMBER from the list above"
        )
        if project_num == '0':
            project_num = self.create_new_project(org_name)
        
        # Step 3: Get tasks file (with default)
        tasks_file = os.getenv("GITHUB_TASKS_FILE", "tasks.md").strip()
        if not tasks_file:
            tasks_file = "tasks.md"
            set_key(str(self.env_file), "GITHUB_TASKS_FILE", tasks_file)
        print(f"✓ Using tasks file: {tasks_file}")
        
        # Step 4: Discover project ID
        project_id = self.discover_project_id(org_name, project_num)
        
        # Step 5: Discover field IDs
        field_ids = self.discover_field_ids(org_name, project_num)
        
        # Step 6: Discover status options
        status_options = self.discover_field_options(org_name, project_num, "Status")
        
        # Step 7: Discover priority options
        priority_options = self.discover_field_options(org_name, project_num, "Priority")
        
        # Step 8: Generate gh.yaml
        config = {
            "project_id": project_id,
            "status_field_id": field_ids["status"],
            "priority_field_id": field_ids["priority"],
            "status_options": status_options,
            "priority_options": priority_options
        }
        
        self.generate_gh_yaml(config)
        
        print("\n" + "=" * 70)
        print("✅ Configuration complete!")
        print("=" * 70)
        print(f"\nYou can now run the sync script:")
        print(f"  python3 {self.skill_dir}/scripts/sync_mobile.py")
        print("\nTo reconfigure, delete gh.yaml and run this script again.")


if __name__ == "__main__":
    initializer = ConfigInitializer()
    initializer.run()
