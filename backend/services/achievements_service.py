"""成就与激励系统服务"""
from datetime import datetime
from database import get_db


# 积分规则
POINT_RULES = {
    "lesson_complete": 10,
    "quiz_pass": 20,
    "quiz_perfect": 50,
    "daily_streak": 5,
    "favorite": 2,
    "note": 3,
    "placement_complete": 30,
}


def add_points(user_id: int, points: int, reason: str, reference_id: str = None) -> int:
    """添加积分，返回总积分"""
    with get_db() as conn:
        # 记录积分历史
        conn.execute(
            "INSERT INTO point_history (user_id, points, reason, reference_id) VALUES (?, ?, ?, ?)",
            (user_id, points, reason, reference_id)
        )

        # 更新总积分
        existing = conn.execute(
            "SELECT total_points FROM user_points WHERE user_id = ?",
            (user_id,)
        ).fetchone()

        if existing:
            new_total = existing["total_points"] + points
            conn.execute(
                "UPDATE user_points SET total_points = ? WHERE user_id = ?",
                (new_total, user_id)
            )
        else:
            new_total = points
            conn.execute(
                "INSERT INTO user_points (user_id, total_points) VALUES (?, ?)",
                (user_id, new_total)
            )

        # 检查积分成就
        _check_points_achievements(conn, user_id, new_total)

        return new_total


def get_points(user_id: int) -> dict:
    """获取用户积分信息"""
    with get_db() as conn:
        row = conn.execute(
            "SELECT total_points FROM user_points WHERE user_id = ?",
            (user_id,)
        ).fetchone()

        return {"total_points": row["total_points"] if row else 0}


def get_points_history(user_id: int, limit: int = 20) -> list:
    """获取积分历史"""
    with get_db() as conn:
        rows = conn.execute(
            "SELECT points, reason, reference_id, created_at FROM point_history WHERE user_id = ? ORDER BY created_at DESC LIMIT ?",
            (user_id, limit)
        ).fetchall()
        return [dict(r) for r in rows]


def get_streak(user_id: int) -> dict:
    """获取学习连续天数"""
    with get_db() as conn:
        row = conn.execute(
            "SELECT current_streak, longest_streak, last_study_date FROM study_streaks WHERE user_id = ?",
            (user_id,)
        ).fetchone()

        if not row:
            return {"current_streak": 0, "longest_streak": 0, "last_study_date": None}

        return {
            "current_streak": row["current_streak"],
            "longest_streak": row["longest_streak"],
            "last_study_date": row["last_study_date"]
        }


def get_all_achievements() -> list:
    """获取所有成就定义"""
    with get_db() as conn:
        rows = conn.execute("SELECT * FROM achievements ORDER BY criteria_type, criteria_value").fetchall()
        return [dict(r) for r in rows]


def get_user_achievements(user_id: int) -> list:
    """获取用户已获得的成就"""
    with get_db() as conn:
        rows = conn.execute(
            """SELECT a.*, ua.earned_at
               FROM user_achievements ua
               JOIN achievements a ON ua.achievement_id = a.id
               WHERE ua.user_id = ?
               ORDER BY ua.earned_at DESC""",
            (user_id,)
        ).fetchall()
        return [dict(r) for r in rows]


def check_and_award_achievements(user_id: int) -> list:
    """检查并授予成就，返回新获得的成就列表"""
    new_achievements = []

    with get_db() as conn:
        # 获取用户统计
        stats = _get_user_stats(conn, user_id)

        # 获取所有成就定义
        achievements = conn.execute("SELECT * FROM achievements").fetchall()

        # 获取用户已获得的成就
        earned = conn.execute(
            "SELECT achievement_id FROM user_achievements WHERE user_id = ?",
            (user_id,)
        ).fetchall()
        earned_ids = {r["achievement_id"] for r in earned}

        for a in achievements:
            if a["id"] in earned_ids:
                continue

            achieved = False
            value = stats.get(a["criteria_type"], 0)

            if a["criteria_type"] == "streak":
                achieved = value >= a["criteria_value"]
            elif a["criteria_type"] == "points":
                achieved = value >= a["criteria_value"]
            elif a["criteria_type"] in ["lessons_completed", "quizzes_taken", "perfect_score"]:
                achieved = value >= a["criteria_value"]
            elif a["criteria_type"] == "notes_count":
                achieved = value >= a["criteria_value"]
            elif a["criteria_type"] == "favorites_count":
                achieved = value >= a["criteria_value"]

            if achieved:
                conn.execute(
                    "INSERT OR IGNORE INTO user_achievements (user_id, achievement_id) VALUES (?, ?)",
                    (user_id, a["id"])
                )
                new_achievements.append(dict(a))

        return new_achievements


def get_leaderboard(limit: int = 10) -> list:
    """获取排行榜"""
    with get_db() as conn:
        rows = conn.execute(
            """SELECT u.username, up.total_points,
                      COALESCE(ss.current_streak, 0) as streak
               FROM user_points up
               JOIN users u ON up.user_id = u.id
               LEFT JOIN study_streaks ss ON up.user_id = ss.user_id
               ORDER BY up.total_points DESC
               LIMIT ?""",
            (limit,)
        ).fetchall()
        return [dict(r) for r in rows]


def _get_user_stats(conn, user_id: int) -> dict:
    """获取用户统计数据用于成就检查"""
    # 课程完成数
    lessons = conn.execute(
        "SELECT COUNT(*) as count FROM progress WHERE user_id = ? AND stars >= 2",
        (user_id,)
    ).fetchone()["count"]

    # 测验次数
    quizzes = conn.execute(
        "SELECT COALESCE(SUM(tests_taken), 0) as count FROM progress WHERE user_id = ?",
        (user_id,)
    ).fetchone()["count"]

    # 满分次数
    perfect = conn.execute(
        "SELECT COUNT(*) as count FROM progress WHERE user_id = ? AND best_score >= 3",
        (user_id,)
    ).fetchone()["count"]

    # 连续天数
    streak = conn.execute(
        "SELECT current_streak FROM study_streaks WHERE user_id = ?",
        (user_id,)
    ).fetchone()
    streak_count = streak["current_streak"] if streak else 0

    # 总积分
    points = conn.execute(
        "SELECT total_points FROM user_points WHERE user_id = ?",
        (user_id,)
    ).fetchone()
    total_points = points["total_points"] if points else 0

    # 笔记数
    notes = conn.execute(
        "SELECT COUNT(*) as count FROM notes WHERE user_id = ?",
        (user_id,)
    ).fetchone()["count"]

    # 收藏数
    favorites = conn.execute(
        "SELECT COUNT(*) as count FROM favorites WHERE user_id = ?",
        (user_id,)
    ).fetchone()["count"]

    return {
        "lessons_completed": lessons,
        "quizzes_taken": quizzes,
        "perfect_score": perfect,
        "streak": streak_count,
        "points": total_points,
        "notes_count": notes,
        "favorites_count": favorites,
    }


def _check_points_achievements(conn, user_id: int, total_points: int):
    """检查积分相关成就"""
    achievements = conn.execute(
        "SELECT * FROM achievements WHERE criteria_type = 'points'"
    ).fetchall()

    earned = conn.execute(
        "SELECT achievement_id FROM user_achievements WHERE user_id = ?",
        (user_id,)
    ).fetchall()
    earned_ids = {r["achievement_id"] for r in earned}

    for a in achievements:
        if a["id"] not in earned_ids and total_points >= a["criteria_value"]:
            conn.execute(
                "INSERT OR IGNORE INTO user_achievements (user_id, achievement_id) VALUES (?, ?)",
                (user_id, a["id"])
            )
