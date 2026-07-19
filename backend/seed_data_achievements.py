"""成就定义种子数据"""

ACHIEVEMENTS = [
    # 学习成就
    {"id": "first_lesson", "name": "初学者", "description": "完成第一个课程", "icon": "🎓", "criteria_type": "lessons_completed", "criteria_value": 1},
    {"id": "lessons_5", "name": "勤学者", "description": "完成5个课程", "icon": "📚", "criteria_type": "lessons_completed", "criteria_value": 5},
    {"id": "lessons_10", "name": "好学者", "description": "完成10个课程", "icon": "📖", "criteria_type": "lessons_completed", "criteria_value": 10},
    {"id": "lessons_20", "name": "博学者", "description": "完成20个课程", "icon": "🎓", "criteria_type": "lessons_completed", "criteria_value": 20},
    {"id": "lessons_30", "name": "数学大师", "description": "完成全部30个课程", "icon": "👑", "criteria_type": "lessons_completed", "criteria_value": 30},

    # 测验成就
    {"id": "first_quiz", "name": "小试牛刀", "description": "完成第一次测验", "icon": "✏️", "criteria_type": "quizzes_taken", "criteria_value": 1},
    {"id": "quizzes_10", "name": "测验达人", "description": "完成10次测验", "icon": "📝", "criteria_type": "quizzes_taken", "criteria_value": 10},
    {"id": "quizzes_50", "name": "测验大师", "description": "完成50次测验", "icon": "🏆", "criteria_type": "quizzes_taken", "criteria_value": 50},
    {"id": "perfect_score", "name": "满分达人", "description": "测验获得满分", "icon": "⭐", "criteria_type": "perfect_score", "criteria_value": 1},
    {"id": "perfect_10", "name": "满分收割机", "description": "获得10次满分", "icon": "🌟", "criteria_type": "perfect_score", "criteria_value": 10},

    # 连续学习成就
    {"id": "streak_3", "name": "三日坚持", "description": "连续学习3天", "icon": "🔥", "criteria_type": "streak", "criteria_value": 3},
    {"id": "streak_7", "name": "一周达人", "description": "连续学习7天", "icon": "🔥", "criteria_type": "streak", "criteria_value": 7},
    {"id": "streak_14", "name": "两周坚持", "description": "连续学习14天", "icon": "💪", "criteria_type": "streak", "criteria_value": 14},
    {"id": "streak_30", "name": "月度学霸", "description": "连续学习30天", "icon": "🏆", "criteria_type": "streak", "criteria_value": 30},

    # 积分成就
    {"id": "points_100", "name": "积分新手", "description": "获得100积分", "icon": "💎", "criteria_type": "points", "criteria_value": 100},
    {"id": "points_500", "name": "积分达人", "description": "获得500积分", "icon": "💎", "criteria_type": "points", "criteria_value": 500},
    {"id": "points_1000", "name": "积分大师", "description": "获得1000积分", "icon": "💎", "criteria_type": "points", "criteria_value": 1000},
    {"id": "points_5000", "name": "积分传奇", "description": "获得5000积分", "icon": "👑", "criteria_type": "points", "criteria_value": 5000},

    # 特殊成就
    {"id": "no_wrong", "name": "零失误", "description": "连续10题答对", "icon": "🎯", "criteria_type": "perfect_streak", "criteria_value": 10},
    {"id": "speed_demon", "name": "速算达人", "description": "5分钟内完成测验", "icon": "⚡", "criteria_type": "speed_quiz", "criteria_value": 300},
    {"id": "night_owl", "name": "夜猫子", "description": "晚上10点后学习", "icon": "🦉", "criteria_type": "time_of_day", "criteria_value": 22},
    {"id": "early_bird", "name": "早起鸟", "description": "早上6点前学习", "icon": "🐦", "criteria_type": "time_of_day", "criteria_value": 6},
    {"id": "note_taker", "name": "笔记达人", "description": "添加10条笔记", "icon": "📝", "criteria_type": "notes_count", "criteria_value": 10},
    {"id": "collector", "name": "收藏家", "description": "收藏10个主题", "icon": "❤️", "criteria_type": "favorites_count", "criteria_value": 10},
]


def seed_achievements(conn):
    """导入成就定义"""
    for a in ACHIEVEMENTS:
        try:
            conn.execute(
                "INSERT OR IGNORE INTO achievements (id, name, description, icon, criteria_type, criteria_value) VALUES (?,?,?,?,?,?)",
                (a["id"], a["name"], a["description"], a["icon"], a["criteria_type"], a["criteria_value"])
            )
        except Exception as e:
            print(f"导入成就 {a['id']} 失败: {e}")
    print(f"已导入 {len(ACHIEVEMENTS)} 个成就定义")
