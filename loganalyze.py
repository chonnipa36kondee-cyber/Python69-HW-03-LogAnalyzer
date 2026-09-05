def analyze_user_activity(log_file_path: str) -> dict:
    #your code here
    pass
    from collections import defaultdict

    action_counts = defaultdict(int)
    users = set()
    session_durations = []                     # ค่า duration จากทุก login
    user_total_duration = defaultdict(float)    # user_id -> ผลรวม duration ของ login ที่มี

    with open(log_file_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split()
            if len(parts) < 4:
                continue
            timestamp_str, user_id, action, value_str = parts[0], parts[1], parts[2], parts[3]
            value = float(value_str)

            users.add(user_id)
            action_counts[action] += 1

            if action == "login":
                session_durations.append(value)
                user_total_duration[user_id] += value

    average_session_time = round(sum(session_durations) / len(session_durations), 2) if session_durations else 0.0
    most_active_user = max(user_total_duration, key=user_total_duration.get) if user_total_duration else None

    return {
        "action_counts": dict(action_counts),
        "average_session_time": average_session_time,
        "most_active_user": most_active_user,
        "total_users": len(users),
    }
   


if __name__ == "__main__":
    result = analyze_user_activity("activity.log")
    from pprint import pprint
    pprint(result)

# {'action_counts': {'login': 2, 'logout': 2, 'submit': 1, 'view': 2},
#  'average_session_time': 160.0,
#  'most_active_user': 'u002',
#  'total_users': 2}
