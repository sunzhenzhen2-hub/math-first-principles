"""学习统计服务"""
from datetime import datetime, timedelta
from database import get_db


def start_study_session(user_id: int, topic_id: str) -> int:
    """开始学习会话，返回会话 ID"""
    with get_db() as conn:
        cursor = conn.execute(
            "INSERT INTO study_sessions (user_id, topic_id, started_at) VALUES (?, ?, ?)",
            (user_id, topic_id, datetime.now().isoformat())
        )
        return cursor.lastrowid


def end_study_session(user_id: int, session_id: int) -> dict:
    """结束学习会话，返回统计信息"""
    with get_db() as conn:
        conn.execute(
            "UPDATE study_sessions SET completed_at = ? WHERE id = ? AND user_id = ?",
            (datetime.now().isoformat(), session_id, user_id)
        )
        row = conn.execute(
            "SELECT * FROM study_sessions WHERE id = ?", (session_id,)
        ).fetchone()

        if row and row["started_at"] and row["completed_at"]:
            started = datetime.fromisoformat(row["started_at"])
            completed = datetime.fromisoformat(row["completed_at"])
            duration = int((completed - started).total_seconds())
            conn.execute(
                "UPDATE study_sessions SET duration_seconds = ? WHERE id = ?",
                (duration, session_id)
            )

            # 更新每日统计
            today = datetime.now().strftime("%Y-%m-%d")
            conn.execute(
                """INSERT INTO daily_stats (user_id, date, study_minutes)
                   VALUES (?, ?, ?)
                   ON CONFLICT(user_id, date) DO UPDATE SET
                   study_minutes = study_minutes + ?""",
                (user_id, today, duration // 60, duration // 60)
            )

            # 更新学习连续天数
            _update_streak(conn, user_id)

            return {"duration_seconds": duration, "topic_id": row["topic_id"]}

    return {"duration_seconds": 0, "topic_id": None}


def _update_streak(conn, user_id: int):
    """更新学习连续天数"""
    today = datetime.now().strftime("%Y-%m-%d")
    yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")

    streak = conn.execute(
        "SELECT * FROM study_streaks WHERE user_id = ?", (user_id,)
    ).fetchone()

    if not streak:
        conn.execute(
            "INSERT INTO study_streaks (user_id, current_streak, longest_streak, last_study_date) VALUES (?, 1, 1, ?)",
            (user_id, today)
        )
        return

    if streak["last_study_date"] == today:
        return  # 今天已经记录过了

    if streak["last_study_date"] == yesterday:
        new_streak = streak["current_streak"] + 1
    else:
        new_streak = 1

    new_longest = max(streak["longest_streak"], new_streak)

    conn.execute(
        "UPDATE study_streaks SET current_streak = ?, longest_streak = ?, last_study_date = ? WHERE user_id = ?",
        (new_streak, new_longest, today, user_id)
    )


def record_quiz_attempt(user_id: int, correct: bool):
    """记录测验尝试"""
    today = datetime.now().strftime("%Y-%m-%d")
    with get_db() as conn:
        conn.execute(
            """INSERT INTO daily_stats (user_id, date, questions_attempted, questions_correct)
               VALUES (?, ?, 1, ?)
               ON CONFLICT(user_id, date) DO UPDATE SET
               questions_attempted = questions_attempted + 1,
               questions_correct = questions_correct + ?""",
            (user_id, today, 1 if correct else 0, 1 if correct else 0)
        )


def get_summary(user_id: int) -> dict:
    """获取用户学习统计摘要"""
    with get_db() as conn:
        # 总学习时长
        total_time = conn.execute(
            "SELECT COALESCE(SUM(duration_seconds), 0) as total FROM study_sessions WHERE user_id = ?",
            (user_id,)
        ).fetchone()["total"]

        # 总做题数
        total_quizzes = conn.execute(
            "SELECT COALESCE(SUM(tests_taken), 0) as total FROM progress WHERE user_id = ?",
            (user_id,)
        ).fetchone()["total"]

        # 总正确数
        total_correct = conn.execute(
            "SELECT COALESCE(SUM(tests_passed), 0) as total FROM progress WHERE user_id = ?",
            (user_id,)
        ).fetchone()["total"]

        # 已完成主题数
        completed_topics = conn.execute(
            "SELECT COUNT(*) as total FROM progress WHERE user_id = ? AND stars >= 2",
            (user_id,)
        ).fetchone()["total"]

        # 连续天数
        streak = conn.execute(
            "SELECT current_streak FROM study_streaks WHERE user_id = ?",
            (user_id,)
        ).fetchone()
        current_streak = streak["current_streak"] if streak else 0

        # 总积分
        points = conn.execute(
            "SELECT total_points FROM user_points WHERE user_id = ?",
            (user_id,)
        ).fetchone()
        total_points = points["total_points"] if points else 0

        return {
            "total_study_seconds": total_time,
            "total_study_hours": round(total_time / 3600, 1),
            "total_quizzes": total_quizzes,
            "total_correct": total_correct,
            "accuracy": round(total_correct / total_quizzes * 100, 1) if total_quizzes > 0 else 0,
            "completed_topics": completed_topics,
            "current_streak": current_streak,
            "total_points": total_points
        }


def get_daily_stats(user_id: int, days: int = 7) -> list:
    """获取每日统计"""
    with get_db() as conn:
        rows = conn.execute(
            """SELECT date, study_minutes, questions_attempted, questions_correct, topics_completed
               FROM daily_stats WHERE user_id = ? AND date >= date('now', ?)
               ORDER BY date ASC""",
            (user_id, f'-{days} days')
        ).fetchall()
        return [dict(r) for r in rows]


def get_weekly_stats(user_id: int) -> dict:
    """获取每周统计"""
    with get_db() as conn:
        # 本周
        this_week = conn.execute(
            """SELECT COALESCE(SUM(study_minutes), 0) as minutes,
                      COALESCE(SUM(questions_attempted), 0) as attempted,
                      COALESCE(SUM(questions_correct), 0) as correct
               FROM daily_stats WHERE user_id = ? AND date >= date('now', 'weekday 0', '-7 days')""",
            (user_id,)
        ).fetchone()

        # 上周
        last_week = conn.execute(
            """SELECT COALESCE(SUM(study_minutes), 0) as minutes,
                      COALESCE(SUM(questions_attempted), 0) as attempted,
                      COALESCE(SUM(questions_correct), 0) as correct
               FROM daily_stats WHERE user_id = ?
               AND date >= date('now', 'weekday 0', '-14 days')
               AND date < date('now', 'weekday 0', '-7 days')""",
            (user_id,)
        ).fetchone()

        return {
            "this_week": dict(this_week),
            "last_week": dict(last_week),
            "trend": {
                "minutes_change": this_week["minutes"] - last_week["minutes"],
                "accuracy_change": (
                    round(this_week["correct"] / this_week["attempted"] * 100, 1) if this_week["attempted"] > 0 else 0
                ) - (
                    round(last_week["correct"] / last_week["attempted"] * 100, 1) if last_week["attempted"] > 0 else 0
                )
            }
        }


def get_topic_mastery(user_id: int) -> list:
    """获取主题掌握度"""
    with get_db() as conn:
        rows = conn.execute(
            """SELECT p.topic_id, p.stars, p.tests_taken, p.tests_passed, p.best_score,
                      t.title, t.stage, t.stage_index
               FROM progress p
               JOIN topics t ON p.topic_id = t.id
               WHERE p.user_id = ?
               ORDER BY t.stage_index, t.sort_order""",
            (user_id,)
        ).fetchall()
        return [dict(r) for r in rows]
