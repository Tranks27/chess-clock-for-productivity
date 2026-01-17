"""Session statistics tracking for TrueFocus Timer."""

import os
import json
from datetime import datetime


def get_stats_dir():
    """Get the stats directory path.

    For scripts: project_root/stats
    For exe: user home directory/.productivity_clock/stats
    """
    import sys

    if getattr(sys, 'frozen', False):
        # Running as compiled executable - use user home directory
        stats_dir = os.path.join(os.path.expanduser("~"), ".productivity_clock", "stats")
    else:
        # Running as script - use project root/stats
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        stats_dir = os.path.join(project_root, "stats")

    if not os.path.exists(stats_dir):
        os.makedirs(stats_dir)
    return stats_dir


def get_stats_path():
    """Get the stats file path."""
    return os.path.join(get_stats_dir(), "stats.json")


def load_stats():
    """Load session statistics from file."""
    try:
        stats_path = get_stats_path()
        if os.path.exists(stats_path):
            with open(stats_path, 'r') as f:
                return json.load(f)
    except Exception as e:
        print(f"Error loading stats: {e}")
    return {"sessions": []}


def save_stats(stats):
    """Save session statistics to file."""
    try:
        stats_path = get_stats_path()
        with open(stats_path, 'w') as f:
            json.dump(stats, f, indent=2)
    except Exception as e:
        print(f"Error saving stats: {e}")


class StatsTracker:
    """Tracks session statistics."""
    
    def __init__(self):
        self.stats = load_stats()
        self.current_session = None
    
    def start_session(self, initial_time):
        """Start tracking a new session."""
        self.current_session = {
            "start_time": datetime.now().isoformat(),
            "initial_productivity_time": initial_time,
            "end_time": None,
            "total_slack_time": 0,
            "outcome": None
        }
    
    def end_session(self, total_slack_time, outcome="completed"):
        """End the current session and save it."""
        if self.current_session is None:
            return
        
        self.current_session["end_time"] = datetime.now().isoformat()
        self.current_session["total_slack_time"] = total_slack_time
        self.current_session["outcome"] = outcome
        
        self.stats["sessions"].append(self.current_session)
        save_stats(self.stats)
        self.current_session = None
    
    def reset_session(self, total_slack_time):
        """Mark session as reset early."""
        if self.current_session is not None:
            self.end_session(total_slack_time, outcome="reset_early")
    
    def get_all_sessions(self):
        """Get all recorded sessions."""
        return self.stats["sessions"]
    
    def get_session_count(self):
        """Get total number of sessions."""
        return len(self.stats["sessions"])
    
    def get_completed_sessions(self):
        """Get only completed sessions."""
        return [s for s in self.stats["sessions"] if s["outcome"] == "completed"]