"""个性化学习路径服务"""
import json
from datetime import datetime
from database import get_db


def get_or_create_path(user_id: int) -> dict:
    """获取或创建用户学习路径"""
    with get_db() as conn:
        row = conn.execute(
            "SELECT path_data FROM learning_paths WHERE user_id = ?",
            (user_id,)
        ).fetchone()

        if row:
            return json.loads(row["path_data"])

        # 创建新路径
        path_data = _generate_default_path(conn, user_id)
        conn.execute(
            "INSERT INTO learning_paths (user_id, path_data) VALUES (?, ?)",
            (user_id, json.dumps(path_data))
        )
        return path_data


def generate_personalized_path(user_id: int) -> dict:
    """生成个性化学习路径"""
    with get_db() as conn:
        path_data = _analyze_and_generate(conn, user_id)

        # 更新或插入路径
        existing = conn.execute(
            "SELECT id FROM learning_paths WHERE user_id = ?",
            (user_id,)
        ).fetchone()

        if existing:
            conn.execute(
                "UPDATE learning_paths SET path_data = ?, updated_at = ? WHERE user_id = ?",
                (json.dumps(path_data), datetime.now().isoformat(), user_id)
            )
        else:
            conn.execute(
                "INSERT INTO learning_paths (user_id, path_data) VALUES (?, ?)",
                (user_id, json.dumps(path_data))
            )

        return path_data


def get_weak_areas(user_id: int) -> list:
    """分析薄弱环节"""
    with get_db() as conn:
        rows = conn.execute(
            """SELECT p.topic_id, p.tests_taken, p.tests_passed, p.best_score,
                      t.title, t.stage, t.stage_index
               FROM progress p
               JOIN topics t ON p.topic_id = t.id
               WHERE p.user_id = ? AND p.tests_taken > 0
               ORDER BY (CAST(p.tests_passed AS REAL) / p.tests_taken) ASC""",
            (user_id,)
        ).fetchall()

        weak_areas = []
        for r in rows:
            accuracy = r["tests_passed"] / r["tests_taken"] if r["tests_taken"] > 0 else 0
            if accuracy < 0.7:  # 正确率低于70%视为薄弱
                weak_areas.append({
                    "topic_id": r["topic_id"],
                    "title": r["title"],
                    "stage": r["stage"],
                    "stage_index": r["stage_index"],
                    "accuracy": round(accuracy * 100, 1),
                    "tests_taken": r["tests_taken"],
                    "suggestion": _get_suggestion(accuracy)
                })

        return weak_areas


def get_recommendations(user_id: int) -> list:
    """获取推荐学习顺序"""
    with get_db() as conn:
        # 获取所有主题
        all_topics = conn.execute(
            "SELECT * FROM topics ORDER BY stage_index, sort_order"
        ).fetchall()

        # 获取用户进度
        progress = conn.execute(
            "SELECT topic_id, stars, tests_taken, best_score FROM progress WHERE user_id = ?",
            (user_id,)
        ).fetchall()
        progress_map = {r["topic_id"]: dict(r) for r in progress}

        recommendations = []
        for topic in all_topics:
            topic_id = topic["id"]
            prog = progress_map.get(topic_id, {})

            # 确定状态
            if prog.get("stars", 0) >= 2:
                status = "completed"
            elif prog.get("tests_taken", 0) > 0:
                status = "in_progress"
            else:
                status = "not_started"

            # 确定是否推荐
            is_recommended = False
            if status == "not_started":
                # 检查前置主题是否完成
                topic_index = all_topics.index(topic)
                if topic_index == 0:
                    is_recommended = True
                else:
                    prev_topic = all_topics[topic_index - 1]
                    prev_prog = progress_map.get(prev_topic["id"], {})
                    if prev_prog.get("stars", 0) >= 1:
                        is_recommended = True

            recommendations.append({
                "topic_id": topic_id,
                "title": topic["title"],
                "icon": topic["icon"],
                "stage": topic["stage"],
                "stage_index": topic["stage_index"],
                "status": status,
                "is_recommended": is_recommended,
                "stars": prog.get("stars", 0),
                "accuracy": _calc_accuracy(prog)
            })

        return recommendations


def _generate_default_path(conn, user_id: int) -> dict:
    """生成默认学习路径"""
    topics = conn.execute(
        "SELECT id, title, stage_index FROM topics ORDER BY stage_index, sort_order"
    ).fetchall()

    progress = conn.execute(
        "SELECT topic_id, stars FROM progress WHERE user_id = ?",
        (user_id,)
    ).fetchall()
    completed = {r["topic_id"] for r in progress if r["stars"] >= 2}

    recommended = []
    for t in topics:
        if t["id"] not in completed:
            recommended.append(t["id"])

    return {
        "recommended": recommended[:5],  # 推荐前5个
        "completed": list(completed),
        "generated_at": datetime.now().isoformat()
    }


def _analyze_and_generate(conn, user_id: int) -> dict:
    """分析用户数据并生成个性化路径"""
    # 获取薄弱环节
    weak_areas = get_weak_areas(user_id)

    # 获取所有主题
    all_topics = conn.execute(
        "SELECT * FROM topics ORDER BY stage_index, sort_order"
    ).fetchall()

    # 获取用户进度
    progress = conn.execute(
        "SELECT topic_id, stars, tests_taken, tests_passed, best_score FROM progress WHERE user_id = ?",
        (user_id,)
    ).fetchall()
    progress_map = {r["topic_id"]: dict(r) for r in progress}

    # 分析推荐顺序
    recommended = []
    completed = []

    for topic in all_topics:
        topic_id = topic["id"]
        prog = progress_map.get(topic_id, {})

        if prog.get("stars", 0) >= 2:
            completed.append(topic_id)
        else:
            # 检查是否应该推荐
            topic_index = all_topics.index(topic)
            if topic_index == 0:
                recommended.append(topic_id)
            else:
                prev_topic = all_topics[topic_index - 1]
                prev_prog = progress_map.get(prev_topic["id"], {})
                if prev_prog.get("stars", 0) >= 1:
                    recommended.append(topic_id)

    # 优先推荐薄弱环节的强化练习
    weak_topic_ids = [w["topic_id"] for w in weak_areas]
    priority_recommended = [t for t in recommended if t in weak_topic_ids]
    other_recommended = [t for t in recommended if t not in weak_topic_ids]

    return {
        "recommended": priority_recommended + other_recommended[:5],
        "completed": completed,
        "weak_areas": weak_areas,
        "generated_at": datetime.now().isoformat(),
        "ai_suggestion": _generate_suggestion(weak_areas, len(completed), len(all_topics))
    }


def _get_suggestion(accuracy: float) -> str:
    """根据正确率生成建议"""
    if accuracy < 0.4:
        return "建议重新学习该主题的基础概念"
    elif accuracy < 0.6:
        return "建议复习关键公式和定理"
    elif accuracy < 0.7:
        return "多做几道练习题巩固"
    return ""


def _generate_suggestion(weak_areas: list, completed: int, total: int) -> str:
    """生成 AI 学习建议"""
    if not weak_areas:
        if completed == total:
            return "恭喜！你已完成所有主题的学习！"
        return "继续保持当前的学习节奏，按推荐顺序学习即可。"

    weak_titles = [w["title"] for w in weak_areas[:3]]
    progress_pct = round(completed / total * 100)

    suggestion = f"你目前已完成 {progress_pct}% 的课程。"
    if weak_titles:
        suggestion += f"建议先复习 {'、'.join(weak_titles)} 等薄弱环节，"
    suggestion += "再继续学习新内容。每天保持学习可以获得更多积分和成就！"

    return suggestion


def _calc_accuracy(prog: dict) -> float:
    """计算正确率"""
    if not prog or prog.get("tests_taken", 0) == 0:
        return 0
    return round(prog.get("tests_passed", 0) / prog["tests_taken"] * 100, 1)
