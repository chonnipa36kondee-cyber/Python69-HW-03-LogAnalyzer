def analyze_user_activity(log_file_path: str) -> dict:
    from collections import defaultdict
    from datetime import datetime

    action_counts = defaultdict(int)
    user_action_counts = defaultdict(int)
    user_events = defaultdict(list)   # user_id -> [(timestamp, action), ...]
    session_durations = []

    with open(log_file_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            parts = line.split(",")
            if len(parts) < 3:
                continue

            timestamp_str, user_id, action = (
                parts[0].strip(),
                parts[1].strip(),
                parts[2].strip(),
            )

            try:
                timestamp = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
            except ValueError:
                continue

            action_counts[action] += 1
            user_action_counts[user_id] += 1
            user_events[user_id].append((timestamp, action))

    for user_id, events in user_events.items():
        events.sort(key=lambda e: e[0])
        login_time = None
        for timestamp, action in events:
            if action == "login":
                login_time = timestamp
            elif action == "logout" and login_time is not None:
                duration = (timestamp - login_time).total_seconds()
                session_durations.append(duration)
                login_time = None

    total_users = len(user_events)
    average_session_time = (
        sum(session_durations) / len(session_durations)
        if session_durations
        else 0.0
    )
    most_active_user = (
        max(user_action_counts, key=user_action_counts.get)
        if user_action_counts
        else None
    )

    return {
        "action_counts": dict(action_counts),
        "average_session_time": average_session_time,
        "most_active_user": most_active_user,
        "total_users": total_users,
    }


if __name__ == "__main__":
    result = analyze_user_activity("activity.log")
    from pprint import pprint
    pprint(result)

# {'action_counts': {'login': 2, 'logout': 2, 'submit': 1, 'view': 2},
#  'average_session_time': 160.0,
#  'most_active_user': 'u002',
#  'total_users': 2}
