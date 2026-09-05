def analyze_user_activity(log_file_path: str) -> dict:
    """
    วิเคราะห์ไฟล์ Log และคืนค่าสรุปพฤติกรรมผู้ใช้ในรูปแบบ dictionary
    """
    user_action_counts = {}  # {user_id: total_actions}
    action_counts = {}       # {action_name: count}
    total_duration = 0
    valid_lines_count = 0

    try:
        with open(log_file_path, 'r', encoding='utf-8') as file:
            for line in file:
                # ข้ามบรรทัดว่าง
                line = line.strip()
                if not line:
                    continue

                parts = line.split()
                # ตรวจสอบว่าบรรทัดมีข้อมูลครบ 4 ส่วนหรือไม่
                if len(parts) != 4:
                    continue

                timestamp, user_id, action, duration_str = parts

                # ตรวจสอบว่า duration เป็นตัวเลขหรือไม่
                try:
                    duration = float(duration_str)
                except ValueError:
                    continue

                # บันทึกข้อมูลที่ถูกต้อง
                user_action_counts[user_id] = user_action_counts.get(user_id, 0) + 1
                action_counts[action] = action_counts.get(action, 0) + 1
                total_duration += duration
                valid_lines_count += 1

    except FileNotFoundError:
        # หากไม่พบไฟล์ สามารถ return ค่าเริ่มต้นของไฟล์ว่างเปล่าได้
        pass

    # กรณีไม่มีข้อมูลที่สมบูรณ์เลย (หรือไฟล์ว่าง)
    if valid_lines_count == 0:
        return {
            "total_users": 0,
            "action_counts": {},
            "most_active_user": None,
            "average_session_time": 0.0
        }

    # หา user ที่มีกิจกรรมมากที่สุด
    most_active_user = max(user_action_counts, key=user_action_counts.get)
    
    # คำนวณระยะเวลาเฉลี่ยต่อกิจกรรม
    average_session_time = round(total_duration / valid_lines_count, 2)

    return {
        "total_users": len(user_action_counts),
        "action_counts": action_counts,
        "most_active_user": most_active_user,
        "average_session_time": average_session_time
    }


if __name__ == "__main__":
    result = analyze_user_activity("activity.log")
    from pprint import pprint
    pprint(result)

# {'action_counts': {'login': 2, 'logout': 2, 'submit': 1, 'view': 2},
#  'average_session_time': 160.0,
#  'most_active_user': 'u002',
#  'total_users': 2}
