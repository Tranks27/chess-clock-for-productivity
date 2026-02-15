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


def get_stats_path_for_month(year, month):
    """Get the stats file path for a specific month (YYYY-MM.json format)."""
    filename = f"{year:04d}-{month:02d}.json"
    return os.path.join(get_stats_dir(), filename)


def load_stats():
    """Load all session statistics from month files."""
    stats_dir = get_stats_dir()
    all_sessions = []

    try:
        # Look for all YYYY-MM.json files in the stats directory
        if os.path.exists(stats_dir):
            for filename in sorted(os.listdir(stats_dir)):
                if filename.endswith('.json'):
                    filepath = os.path.join(stats_dir, filename)
                    try:
                        with open(filepath, 'r') as f:
                            data = json.load(f)
                            if isinstance(data, dict) and "sessions" in data:
                                all_sessions.extend(data["sessions"])
                    except Exception as e:
                        print(f"Error loading {filename}: {e}")
    except Exception as e:
        print(f"Error loading stats: {e}")

    return {"sessions": all_sessions}


def save_stats(stats, year=None, month=None):
    """Save session statistics to a month file.

    If year/month not provided, uses current year/month.
    """
    try:
        if year is None or month is None:
            now = datetime.now()
            year = now.year
            month = now.month

        stats_path = get_stats_path_for_month(year, month)
        with open(stats_path, 'w') as f:
            json.dump(stats, f, indent=2)
    except Exception as e:
        print(f"Error saving stats: {e}")


class StatsTracker:
    """Tracks session statistics."""
    
    def __init__(self):
        self.stats = load_stats()
        self.current_session = None
        self._slack_segment_start = None
    
    def start_session(self, initial_time):
        """Start tracking a new session."""
        self.current_session = {
            "start_time": datetime.now().isoformat(),
            "initial_productivity_time": initial_time,
            "end_time": None,
            "total_slack_time": 0,
            "work_time_actual": 0,
            "slack_events_count": 0,
            "slack_segments": [],
            "outcome": None
        }
        self._slack_segment_start = None

    def start_slack_segment(self, start_time=None):
        """Start a slack segment if not already in one."""
        if self.current_session is None or self._slack_segment_start is not None:
            return
        self._slack_segment_start = start_time or datetime.now()

    def end_slack_segment(self, end_time=None):
        """End the current slack segment and store it."""
        if self.current_session is None or self._slack_segment_start is None:
            return
        segment_end = end_time or datetime.now()
        duration = (segment_end - self._slack_segment_start).total_seconds()
        self.current_session["slack_segments"].append({
            "start_time": self._slack_segment_start.isoformat(),
            "end_time": segment_end.isoformat(),
            "duration_seconds": max(int(duration), 0)
        })
        self._slack_segment_start = None
    
    def end_session(self, total_slack_time, outcome="completed"):
        """End the current session and save it."""
        if self.current_session is None:
            return

        end_time = datetime.now()
        self.end_slack_segment(end_time=end_time)
        self.current_session["end_time"] = end_time.isoformat()
        total_slack_time_int = int(round(total_slack_time))
        self.current_session["total_slack_time"] = total_slack_time_int
        initial_time = self.current_session.get("initial_productivity_time", 0)
        self.current_session["work_time_actual"] = max(int(initial_time) - total_slack_time_int, 0)
        self.current_session["outcome"] = outcome

        # Extract year and month from session start time for file organization
        start_dt = datetime.fromisoformat(self.current_session["start_time"])
        year = start_dt.year
        month = start_dt.month

        # Load existing sessions for this month
        month_stats_path = get_stats_path_for_month(year, month)
        month_stats = {"sessions": []}
        if os.path.exists(month_stats_path):
            try:
                with open(month_stats_path, 'r') as f:
                    month_stats = json.load(f)
            except Exception as e:
                print(f"Error loading month stats: {e}")

        # Add current session to month file
        month_stats["sessions"].append(self.current_session)
        save_stats(month_stats, year, month)

        # Update in-memory stats for the session
        self.stats["sessions"].append(self.current_session)
        self.current_session = None
    
    def reset_session(self, total_slack_time):
        """Mark session as reset early."""
        if self.current_session is not None:
            self.end_session(total_slack_time, outcome="reset_early")
    
    def get_all_sessions(self):
        """Get all recorded sessions."""
        return self.stats["sessions"]

    def compute_session_metrics(self, session):
        """Compute derived metrics for a session."""
        start_time = session.get("start_time")
        end_time = session.get("end_time")
        initial_time = session.get("initial_productivity_time", 0)
        total_slack = session.get("total_slack_time", 0)

        wall_clock_duration = 0
        if start_time and end_time:
            try:
                start_dt = datetime.fromisoformat(start_time)
                end_dt = datetime.fromisoformat(end_time)
                wall_clock_duration = max(int((end_dt - start_dt).total_seconds()), 0)
            except ValueError:
                wall_clock_duration = 0

        if session.get("outcome") == "completed":
            actual_focus_time = int(initial_time)
        elif wall_clock_duration:
            actual_focus_time = max(int(wall_clock_duration - total_slack), 0)
        else:
            actual_focus_time = max(int(initial_time - total_slack), 0)
        slack_ratio = (total_slack / (actual_focus_time + total_slack)) if (actual_focus_time + total_slack) else 0
        overrun_time = wall_clock_duration - initial_time

        return {
            "wall_clock_duration": wall_clock_duration,
            "actual_focus_time": actual_focus_time,
            "slack_ratio": slack_ratio,
            "overrun_time": overrun_time
        }

    def get_sessions_with_metrics(self):
        """Return sessions with derived metrics included."""
        return [
            {**session, **self.compute_session_metrics(session)}
            for session in self.stats["sessions"]
        ]
    
    def get_session_count(self):
        """Get total number of sessions."""
        return len(self.stats["sessions"])
    
    def get_completed_sessions(self):
        """Get only completed sessions."""
        return [s for s in self.stats["sessions"] if s["outcome"] == "completed"]
