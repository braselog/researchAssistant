#!/bin/bash

# =============================================================================
# Apple Calendar CLI
# =============================================================================
# A command-line interface for interacting with Apple Calendar via icalBuddy
# Uses Terminal.app workaround to access calendar data
#
# USAGE:
#   ./calendar-cli.sh <command> [options]
#
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

# Find micromamba path dynamically
MICROMAMBA_PATH=$(which conda 2>/dev/null || which micromamba 2>/dev/null)

# =============================================================================
# Configuration - Calendars to include by default
# =============================================================================

# Try to load .env file if it exists
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../../../.." && pwd)"
ENV_FILE="$PROJECT_ROOT/.env"

if [ -f "$ENV_FILE" ]; then
    # Skip init if command is calendars (to avoid loop)
    if [ "$1" != "calendars" ]; then
        # Load DEFAULT_CALENDARS from .env file
        DEFAULT_CALENDARS_RAW=$(grep -E "^DEFAULT_CALENDARS=" "$ENV_FILE" | cut -d'=' -f2-)
        if [ -n "$DEFAULT_CALENDARS_RAW" ]; then
            # Convert comma-separated string to array
            IFS=',' read -ra DEFAULT_CALENDARS <<< "$DEFAULT_CALENDARS_RAW"
        else
            # DEFAULT_CALENDARS not set - run automated setup
            echo -e "${YELLOW}⚠ DEFAULT_CALENDARS not configured in .env${NC}" >&2
            echo -e "${CYAN}Installing dependencies and running calendar configuration setup...${NC}" >&2
            echo "" >&2
            
            # Install python-dotenv if needed
            # $MICROMAMBA_PATH run -n research-assistant pip install python-dotenv >/dev/null 2>&1
            
            # Run init script
            if $MICROMAMBA_PATH run -n research-assistant python "$SCRIPT_DIR/init_config.py"; then
                # Reload from .env after init
                DEFAULT_CALENDARS_RAW=$(grep -E "^DEFAULT_CALENDARS=" "$ENV_FILE" | cut -d'=' -f2-)
                if [ -n "$DEFAULT_CALENDARS_RAW" ]; then
                    IFS=',' read -ra DEFAULT_CALENDARS <<< "$DEFAULT_CALENDARS_RAW"
                else
                    # Init failed to set calendars, use fallback
                    echo -e "${YELLOW}Warning: Configuration incomplete, using fallback values.${NC}" >&2
                    exit 1
                fi
            else
                # Init script failed, use fallback
                echo -e "${YELLOW}Warning: Configuration failed, using fallback values.${NC}" >&2
                exit 1
            fi
        fi
        
        # Load DEFAULT_WRITE_CALENDAR from .env file
        DEFAULT_WRITE_CALENDAR=$(grep -E "^DEFAULT_WRITE_CALENDAR=" "$ENV_FILE" | cut -d'=' -f2-)
        if [ -z "$DEFAULT_WRITE_CALENDAR" ]; then
            # Use first calendar from DEFAULT_CALENDARS if not set
            DEFAULT_WRITE_CALENDAR="${DEFAULT_CALENDARS[0]}"
        fi
        
        # Load DEFAULT_REMINDER_MINUTES from .env file
        DEFAULT_REMINDER_MINUTES=$(grep -E "^DEFAULT_REMINDER_MINUTES=" "$ENV_FILE" | cut -d'=' -f2-)
        if [ -z "$DEFAULT_REMINDER_MINUTES" ]; then
            # Default to 15 minutes if not set
            DEFAULT_REMINDER_MINUTES=15
        fi
    else
        # For calendars command, set empty array
        DEFAULT_CALENDARS=()
        DEFAULT_WRITE_CALENDAR=""
        DEFAULT_REMINDER_MINUTES=15
    fi
else
    # .env file doesn't exist, use fallback
    echo -e "${RED}Error: .env file not found at $ENV_FILE${NC}" >&2
    echo -e "${YELLOW}Create it first: cp .env.example .env${NC}" >&2
    exit 1
fi

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

# Build calendar filter flags for icalBuddy
# icalBuddy accepts comma-separated calendar names in a single -ic flag
build_calendar_flags() {
    local cal_list=$(get_calendar_list)
    # Single -ic flag with comma-separated list
    echo "-ic '$cal_list'"
}

# Get comma-separated calendar list for display
get_calendar_list() {
    local first=true
    local result=""
    for cal in "${DEFAULT_CALENDARS[@]}"; do
        if [ "$first" = true ]; then
            result="$cal"
            first=false
        else
            result="$result,$cal"
        fi
    done
    echo "$result"
}

# Get work hours from researcher_telos.md
# Arguments: $1 = target date (YYYY-MM-DD) - optional
# Returns: "HH:MM HH:MM" (start end) or empty string if not found
get_work_hours_from_telos() {
    local target_date="$1"
    local telos_file="$HOME/.researchAssistant/researcher_telos.md"
    
    if [ ! -f "$telos_file" ]; then
        return 1
    fi
    
    # If date provided, try to get day-specific hours first
    if [ -n "$target_date" ]; then
        # Get day of week (Monday, Tuesday, etc.)
        local day_name=$(date -j -f "%Y-%m-%d" "$target_date" "+%A" 2>/dev/null)
        
        if [ -n "$day_name" ]; then
            # Try to find day-specific hours (e.g., "- **Monday**: 07:30-16:00")
            # Use grep with -E for extended regex, escape the ** properly
            local day_hours=$(grep -E "\\*\\*${day_name}\\*\\*" "$telos_file" | sed -E 's/.*[^0-9]([0-9]{2}:[0-9]{2})-([0-9]{2}:[0-9]{2}).*/\1 \2/' | head -1)
            
            # Check if we got valid time format
            if [[ "$day_hours" =~ ^[0-9]{2}:[0-9]{2}[[:space:]][0-9]{2}:[0-9]{2}$ ]]; then
                echo "$day_hours"
                return 0
            fi
        fi
    fi
    
    # Fall back to generic "Work day start" and "Work day end"
    local work_start=$(grep -i "Work day start" "$telos_file" | sed -E 's/.*Work day start[^:]*:[[:space:]]*([0-9]{2}:[0-9]{2}).*/\1/' | head -1)
    local work_end=$(grep -i "Work day end" "$telos_file" | sed -E 's/.*Work day end[^:]*:[[:space:]]*([0-9]{2}:[0-9]{2}).*/\1/' | head -1)
    
    # Only return if both values are valid time formats
    if [[ "$work_start" =~ ^[0-9]{2}:[0-9]{2}$ ]] && [[ "$work_end" =~ ^[0-9]{2}:[0-9]{2}$ ]]; then
        echo "$work_start $work_end"
        return 0
    fi
    
    return 1
}

# Get start of current week (Monday)
get_week_start() {
    local dow=$(date +%u)
    local days_to_monday=$((dow - 1))
    date -v-${days_to_monday}d +%Y-%m-%d
}

# Get end of current week (Sunday)
get_week_end() {
    local dow=$(date +%u)
    local days_to_sunday=$((7 - dow))
    date -v+${days_to_sunday}d +%Y-%m-%d
}

# =============================================================================
# icalBuddy via Terminal.app Workaround
# =============================================================================

# Run icalBuddy command through Terminal.app to bypass permissions
run_icalbuddy() {
    local cmd="$1"
    local tmp_file="/tmp/icalbuddy_output_$$.txt"
    
    # Clean up any existing file
    rm -f "$tmp_file"
    
    # Escape double quotes and backslashes for AppleScript
    local escaped_cmd="${cmd//\\/\\\\}"
    escaped_cmd="${escaped_cmd//\"/\\\"}"
    
    # Run icalBuddy via Terminal.app, then close the window
    osascript 2>/dev/null <<APPLESCRIPT
tell application "Terminal"
    -- Create new window with the command
    do script "cd /tmp && $escaped_cmd > '$tmp_file' 2>&1; exit"
    delay 0.3
    -- Wait for command to finish
    repeat while busy of front window
        delay 0.1
    end repeat
    delay 0.2
    -- Close the front window (the one we just created)
    close front window
end tell
APPLESCRIPT
    
    # Read and return output
    if [ -f "$tmp_file" ]; then
        cat "$tmp_file"
        rm -f "$tmp_file"
    fi
}

# =============================================================================
# Calendar Commands
# =============================================================================

# List all available calendars
list_calendars() {
    print_header "Available Calendars"
    run_icalbuddy "icalBuddy calendars"
}

# List events for a date range
list_events() {
    local from_date="$1"
    local to_date="$2"
    local calendar_filter="$3"
    local brief="$4"
    
    print_header "Events: $from_date to $to_date"
    
    # Build calendar include flag
    local cal_flag=""
    if [ -n "$calendar_filter" ]; then
        local escaped_cal="${calendar_filter//\'/\'\\\'\'}"
        cal_flag="-ic '$escaped_cal'"
        print_info "Filtering by calendar: $calendar_filter"
    else
        # Use default calendars
        cal_flag=$(build_calendar_flags)
        local cal_list=$(get_calendar_list)
        print_info "Calendars: $cal_list"
    fi
    
    # Build icalBuddy command
    local cmd="icalBuddy -f $cal_flag"
    if [ "$brief" = "true" ]; then
        cmd="$cmd -eep notes,attendees,url"
    fi
    cmd="$cmd eventsFrom:$from_date to:$to_date"
    
    echo ""
    run_icalbuddy "$cmd"
}

# Add a new event using JXA (this still works without Terminal workaround)
add_event() {
    local title="$1"
    local event_date="$2"
    local start_time="$3"
    local end_time="$4"
    local calendar_name="$5"
    local location="$6"
    local notes="$7"
    local all_day="$8"
    
    if [ -z "$title" ] || [ -z "$event_date" ]; then
        print_error "Title and date are required"
        return 1
    fi
    
    # Default times if not provided
    if [ -z "$start_time" ]; then
        start_time="09:00"
    fi
    if [ -z "$end_time" ]; then
        end_time="10:00"
    fi
    
    # Parse date components
    local event_year="${event_date:0:4}"
    local event_month="${event_date:5:2}"
    local event_day="${event_date:8:2}"
    
    # Remove leading zeros
    event_month=$((10#$event_month))
    event_day=$((10#$event_day))
    
    # Parse time components
    local start_hour="${start_time%%:*}"
    local start_min="${start_time##*:}"
    local end_hour="${end_time%%:*}"
    local end_min="${end_time##*:}"
    
    # Remove leading zeros
    start_hour=$((10#$start_hour))
    start_min=$((10#$start_min))
    end_hour=$((10#$end_hour))
    end_min=$((10#$end_min))
    
    # Escape special characters
    local escaped_title="${title//\\/\\\\}"
    escaped_title="${escaped_title//\"/\\\"}"
    local escaped_location="${location//\\/\\\\}"
    escaped_location="${escaped_location//\"/\\\"}"
    local escaped_notes="${notes//\\/\\\\}"
    escaped_notes="${escaped_notes//\"/\\\"}"
    
    # Calculate trigger interval in minutes (negative for before event)
    local trigger_interval_minutes=$((-DEFAULT_REMINDER_MINUTES))
    
    local result
    if [ "$all_day" = "true" ]; then
        result=$(osascript -l JavaScript - "$calendar_name" "$escaped_title" "$event_year" "$event_month" "$event_day" "$escaped_location" "$escaped_notes" "$trigger_interval_minutes" <<'JSEOF'
function run(argv) {
    const app = Application('Calendar');
    const [calName, evtTitle, evtYear, evtMonth, evtDay, evtLoc, evtNotes, triggerInterval] = argv;
    
    let targetCal = null;
    if (calName) {
        const calendars = app.calendars.whose({ name: calName })();
        if (calendars.length > 0) {
            targetCal = calendars[0];
        }
    }
    if (!targetCal) {
        targetCal = app.calendars()[0];
    }
    
    const eventDate = new Date(parseInt(evtYear), parseInt(evtMonth) - 1, parseInt(evtDay), 0, 0, 0);
    
    const evt = app.Event({
        summary: evtTitle,
        startDate: eventDate,
        alldayEvent: true
    });
    
    targetCal.events.push(evt);
    
    if (evtLoc) evt.location = evtLoc;
    if (evtNotes) evt.description = evtNotes;
    
    // Add display alarm with configurable trigger interval (in minutes)
    const alarm = app.DisplayAlarm({ 
        triggerInterval: parseInt(triggerInterval) 
    });
    evt.displayAlarms.push(alarm);
    
    return "Event created: " + evtTitle + " on " + evtYear + "-" + evtMonth + "-" + evtDay + " (all day)";
}
JSEOF
)
    else
        result=$(osascript -l JavaScript - "$calendar_name" "$escaped_title" "$event_year" "$event_month" "$event_day" "$start_hour" "$start_min" "$end_hour" "$end_min" "$escaped_location" "$escaped_notes" "$trigger_interval_minutes" <<'JSEOF'
function run(argv) {
    const app = Application('Calendar');
    const [calName, evtTitle, evtYear, evtMonth, evtDay, startH, startM, endH, endM, evtLoc, evtNotes, triggerInterval] = argv;
    
    let targetCal = null;
    if (calName) {
        const calendars = app.calendars.whose({ name: calName })();
        if (calendars.length > 0) {
            targetCal = calendars[0];
        }
    }
    if (!targetCal) {
        targetCal = app.calendars()[0];
    }
    
    const startDate = new Date(parseInt(evtYear), parseInt(evtMonth) - 1, parseInt(evtDay), parseInt(startH), parseInt(startM), 0);
    const endDate = new Date(parseInt(evtYear), parseInt(evtMonth) - 1, parseInt(evtDay), parseInt(endH), parseInt(endM), 0);
    
    const evt = app.Event({
        summary: evtTitle,
        startDate: startDate,
        endDate: endDate
    });
    
    targetCal.events.push(evt);
    
    if (evtLoc) evt.location = evtLoc;
    if (evtNotes) evt.description = evtNotes;
    
    // Add display alarm with configurable trigger interval (in minutes)
    const alarm = app.DisplayAlarm({ 
        triggerInterval: parseInt(triggerInterval) 
    });
    evt.displayAlarms.push(alarm);
    
    const pad = (n) => String(n).padStart(2, "0");
    return "Event created: " + evtTitle + " on " + evtYear + "-" + evtMonth + "-" + evtDay + " " + pad(startH) + ":" + pad(startM) + "-" + pad(endH) + ":" + pad(endM);
}
JSEOF
)
    fi
    
    if [ $? -eq 0 ]; then
        print_success "$result"
    else
        print_error "Failed to create event"
        return 1
    fi
}

# Show today's events
show_today() {
    local brief="$1"
    
    print_header "Today's Events"
    
    local cal_list=$(get_calendar_list)
    print_info "Calendars: $cal_list"
    echo ""
    
    local cal_flags=$(build_calendar_flags)
    local cmd="icalBuddy -f $cal_flags"
    if [ "$brief" = "true" ]; then
        # Exclude notes, attendees, url - just show title, time, location
        cmd="$cmd -eep notes,attendees,url"
    fi
    cmd="$cmd eventsToday"
    
    run_icalbuddy "$cmd"
}

# Show this week's events
show_week() {
    local brief="$1"
    local week_start=$(get_week_start)
    local week_end=$(get_week_end)
    
    print_header "This Week ($week_start to $week_end)"
    
    local cal_list=$(get_calendar_list)
    print_info "Calendars: $cal_list"
    echo ""
    
    local cal_flags=$(build_calendar_flags)
    local cmd="icalBuddy -f $cal_flags"
    if [ "$brief" = "true" ]; then
        cmd="$cmd -eep notes,attendees,url"
    fi
    cmd="$cmd eventsFrom:$week_start to:$week_end"
    
    run_icalbuddy "$cmd"
}

# Show next week's events
show_next_week() {
    local brief="$1"
    local week_start=$(date -v+1w -v-$(($(date +%u)-1))d +%Y-%m-%d)
    local week_end=$(date -v+1w -v+$((7-$(date +%u)))d +%Y-%m-%d)
    
    print_header "Next Week ($week_start to $week_end)"
    
    local cal_list=$(get_calendar_list)
    print_info "Calendars: $cal_list"
    echo ""
    
    local cal_flags=$(build_calendar_flags)
    local cmd="icalBuddy -f $cal_flags"
    if [ "$brief" = "true" ]; then
        cmd="$cmd -eep notes,attendees,url"
    fi
    cmd="$cmd eventsFrom:$week_start to:$week_end"
    
    run_icalbuddy "$cmd"
}

# Get events in parseable format
list_events_json() {
    local from_date="$1"
    local to_date="$2"
    local calendar_filter="$3"
    
    local cal_flag=""
    if [ -n "$calendar_filter" ]; then
        local escaped_cal="${calendar_filter//\'/\'\\\'\'}"
        cal_flag="-ic '$escaped_cal'"
    else
        cal_flag=$(build_calendar_flags)
    fi
    
    local cmd="icalBuddy -f -nc -nrd -df %Y-%m-%d -tf %H:%M -iep datetime,title,location,calendar -b '' $cal_flag eventsFrom:$from_date to:$to_date"
    
    run_icalbuddy "$cmd"
}

# Get free time slots for a given day
get_free_slots() {
    local target_date="$1"
    local work_start="${2:-09:00}"
    local work_end="${3:-18:00}"
    
    print_header "Free Time Slots: $target_date"
    print_info "Working hours: $work_start - $work_end"
    echo ""
    
    local cal_flags=$(build_calendar_flags)
    local cmd="icalBuddy -f -nc -nrd -df %Y-%m-%d -tf %H:%M -iep datetime,title -b '' $cal_flags eventsFrom:$target_date to:$target_date"
    
    local events=$(run_icalbuddy "$cmd")
    
    # Parse events and find free slots using Python
    EVENTS="$events" WORK_START="$work_start" WORK_END="$work_end" uv run python3 <<'PYEOF'
import os
import re

events_raw = os.environ.get('EVENTS', '')
work_start = os.environ['WORK_START']
work_end = os.environ['WORK_END']

# Strip ANSI color codes
ansi_escape = re.compile(r'\x1b\[[0-9;]*m')
events_raw = ansi_escape.sub('', events_raw)

def time_to_minutes(t):
    h, m = map(int, t.split(':'))
    return h * 60 + m

def minutes_to_time(m):
    return f"{m // 60:02d}:{m % 60:02d}"

work_start_min = time_to_minutes(work_start)
work_end_min = time_to_minutes(work_end)

busy = []
current_title = None
lines = events_raw.strip().split('\n')

for i, line in enumerate(lines):
    if not line.strip():
        continue
    
    # Check if this is a datetime line (indented with "at")
    datetime_match = re.match(r'\s+\d{4}-\d{2}-\d{2}\s+at\s+(\d{2}:\d{2})(?:\s*-\s*(\d{2}:\d{2}))?', line)
    if datetime_match:
        start_time = datetime_match.group(1)
        end_time = datetime_match.group(2)
        
        start = time_to_minutes(start_time)
        if end_time:
            end = time_to_minutes(end_time)
        else:
            # Point event, assume 1 hour duration
            end = start + 60
        
        if end > work_start_min and start < work_end_min:
            start = max(start, work_start_min)
            end = min(end, work_end_min)
            busy.append((start, end, current_title or "Unknown"))
    else:
        # This is an event title line (not indented)
        if not line.startswith(' '):
            current_title = line.strip()

busy.sort(key=lambda x: x[0])

free_slots = []
current = work_start_min

for start, end, title in busy:
    if start > current:
        duration = start - current
        free_slots.append((current, start, duration))
    current = max(current, end)

if current < work_end_min:
    free_slots.append((current, work_end_min, work_end_min - current))

if free_slots:
    print("FREE TIME SLOTS:")
    print("-" * 40)
    for start, end, duration in free_slots:
        hours = duration // 60
        mins = duration % 60
        dur_str = f"{hours}h {mins}m" if hours > 0 else f"{mins}m"
        print(f"  {minutes_to_time(start)} - {minutes_to_time(end)}  ({dur_str})")
else:
    print("No free slots available during working hours.")

if busy:
    print("\nSCHEDULED EVENTS:")
    print("-" * 40)
    for start, end, title in busy:
        print(f"  {minutes_to_time(start)} - {minutes_to_time(end)}  {title}")
PYEOF
}

# =============================================================================
# Help
# =============================================================================

show_help() {
    cat <<'HELP'
Apple Calendar CLI - Command Line Interface for Apple Calendar

USAGE:
    calendar-cli.sh <command> [options]

COMMANDS:
    today                   Show today's events
    week                    Show this week's events (Mon-Sun)
    next-week               Show next week's events
    list                    List events for a date range
    add                     Add a new event
    calendars               List available calendars
    free                    Show free time slots for a day
    json                    Get events in parseable format
    help                    Show this help message

GLOBAL OPTIONS:
    --brief, -b             Hide notes, attendees, URLs (compact output)

OPTIONS FOR 'list' and 'json':
    --from DATE             Start date (YYYY-MM-DD)
    --to DATE               End date (YYYY-MM-DD)
    --calendar NAME         Filter by calendar name

OPTIONS FOR 'add':
    --title TITLE           Event title (required)
    --date DATE             Event date YYYY-MM-DD (required)
    --start TIME            Start time HH:MM (default: 09:00)
    --end TIME              End time HH:MM (default: 10:00)
    --calendar NAME         Calendar to add event to
    --location LOC          Event location
    --notes TEXT            Event notes/description
    --all-day               Create an all-day event

OPTIONS FOR 'free':
    --date DATE             Date to check (default: today)
    --work-start TIME       Work day start (default: 09:00)
    --work-end TIME         Work day end (default: 18:00)

EXAMPLES:
    calendar-cli.sh today
    calendar-cli.sh week --brief
    calendar-cli.sh list --from 2025-12-01 --to 2025-12-07 --brief
    calendar-cli.sh add --title "Team Meeting" --date 2025-12-03 --start 14:00 --end 15:00
    calendar-cli.sh free --date 2025-12-03

AI ASSISTANT USAGE (use --brief to reduce context size):
    1. Get week's events:    calendar-cli.sh week --brief
    2. Check free slots:     calendar-cli.sh free --date YYYY-MM-DD
    3. Block focus time:     calendar-cli.sh add --title "Focus: [task]" --date ... --start ... --end ...
HELP
}

# =============================================================================
# Main Command Parser
# =============================================================================

main() {
    local command="${1:-help}"
    shift || true
    
    case "$command" in
        today)
            local brief="false"
            while [[ $# -gt 0 ]]; do
                case "$1" in
                    --brief|-b) brief="true"; shift ;;
                    *) shift ;;
                esac
            done
            show_today "$brief"
            ;;
        week)
            local brief="false"
            while [[ $# -gt 0 ]]; do
                case "$1" in
                    --brief|-b) brief="true"; shift ;;
                    *) shift ;;
                esac
            done
            show_week "$brief"
            ;;
        next-week)
            local brief="false"
            while [[ $# -gt 0 ]]; do
                case "$1" in
                    --brief|-b) brief="true"; shift ;;
                    *) shift ;;
                esac
            done
            show_next_week "$brief"
            ;;
        list)
            local from_date=""
            local to_date=""
            local calendar=""
            local brief="false"
            
            while [[ $# -gt 0 ]]; do
                case "$1" in
                    --from) from_date="$2"; shift 2 ;;
                    --to) to_date="$2"; shift 2 ;;
                    --calendar) calendar="$2"; shift 2 ;;
                    --brief|-b) brief="true"; shift ;;
                    *) shift ;;
                esac
            done
            
            if [ -z "$from_date" ] || [ -z "$to_date" ]; then
                print_error "Both --from and --to dates are required"
                exit 1
            fi
            
            list_events "$from_date" "$to_date" "$calendar" "$brief"
            ;;
        json)
            local from_date=""
            local to_date=""
            local calendar=""
            
            while [[ $# -gt 0 ]]; do
                case "$1" in
                    --from) from_date="$2"; shift 2 ;;
                    --to) to_date="$2"; shift 2 ;;
                    --calendar) calendar="$2"; shift 2 ;;
                    *) shift ;;
                esac
            done
            
            if [ -z "$from_date" ] || [ -z "$to_date" ]; then
                print_error "Both --from and --to dates are required"
                exit 1
            fi
            
            list_events_json "$from_date" "$to_date" "$calendar"
            ;;
        add)
            local title=""
            local event_date=""
            local start_time=""
            local end_time=""
            local calendar=""
            local location=""
            local notes=""
            local all_day="false"
            
            while [[ $# -gt 0 ]]; do
                case "$1" in
                    --title) title="$2"; shift 2 ;;
                    --date) event_date="$2"; shift 2 ;;
                    --start) start_time="$2"; shift 2 ;;
                    --end) end_time="$2"; shift 2 ;;
                    --calendar) calendar="$2"; shift 2 ;;
                    --location) location="$2"; shift 2 ;;
                    --notes) notes="$2"; shift 2 ;;
                    --all-day) all_day="true"; shift ;;
                    *) shift ;;
                esac
            done
            
            # Use DEFAULT_WRITE_CALENDAR if no calendar specified
            if [ -z "$calendar" ]; then
                calendar="$DEFAULT_WRITE_CALENDAR"
            fi
            
            add_event "$title" "$event_date" "$start_time" "$end_time" "$calendar" "$location" "$notes" "$all_day"
            ;;
        calendars)
            list_calendars
            ;;
        free)
            local target_date=$(date +%Y-%m-%d)
            local work_start=""
            local work_end=""
            local work_hours_source=""
            
            # Parse command-line arguments first (they take precedence)
            local cli_work_start=""
            local cli_work_end=""
            while [[ $# -gt 0 ]]; do
                case "$1" in
                    --date) target_date="$2"; shift 2 ;;
                    --work-start) cli_work_start="$2"; shift 2 ;;
                    --work-end) cli_work_end="$2"; shift 2 ;;
                    *) shift ;;
                esac
            done
            
            # Determine work hours with fallback chain
            if [ -n "$cli_work_start" ] && [ -n "$cli_work_end" ]; then
                # CLI flags take highest precedence
                work_start="$cli_work_start"
                work_end="$cli_work_end"
                work_hours_source="command-line flags"
            else
                # Try to get from researcher_telos.md (with day-specific detection)
                local telos_hours=$(get_work_hours_from_telos "$target_date")
                if [ -n "$telos_hours" ]; then
                    work_start=$(echo "$telos_hours" | cut -d' ' -f1)
                    work_end=$(echo "$telos_hours" | cut -d' ' -f2)
                    local day_name=$(date -j -f "%Y-%m-%d" "$target_date" "+%A" 2>/dev/null)
                    work_hours_source="researcher_telos.md ($day_name)"
                else
                    # Fall back to hardcoded defaults
                    work_start="09:00"
                    work_end="18:00"
                    work_hours_source="default values"
                fi
            fi
            
            # Log work hours source
            echo -e "${CYAN}Using work hours from ${work_hours_source}: ${work_start}-${work_end}${NC}" >&2
            echo "" >&2
            
            get_free_slots "$target_date" "$work_start" "$work_end"
            ;;
        help|--help|-h)
            show_help
            ;;
        *)
            print_error "Unknown command: $command"
            echo "Use 'calendar-cli.sh help' for usage information"
            exit 1
            ;;
    esac
}

main "$@"
