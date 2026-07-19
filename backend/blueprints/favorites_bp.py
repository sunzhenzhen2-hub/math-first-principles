"""收藏与笔记 API — Flask Blueprint"""
from flask import Blueprint, request, jsonify, g
from database import get_db
from auth import login_required
from services import achievements_service

favorites_bp = Blueprint("favorites", __name__, url_prefix="/api")


# ========== 收藏 ==========

@favorites_bp.route("/favorites", methods=["GET"])
@login_required
def get_favorites():
    """获取收藏列表"""
    with get_db() as conn:
        rows = conn.execute(
            """SELECT f.id, f.topic_id, f.created_at, t.title, t.icon, t.stage
               FROM favorites f
               JOIN topics t ON f.topic_id = t.id
               WHERE f.user_id = ?
               ORDER BY f.created_at DESC""",
            (g.user["sub"],)
        ).fetchall()
        return jsonify([dict(r) for r in rows])


@favorites_bp.route("/favorites", methods=["POST"])
@login_required
def add_favorite():
    """添加收藏"""
    data = request.get_json()
    if not data or not data.get("topic_id"):
        return jsonify({"detail": "topic_id 不能为空"}), 400

    topic_id = data["topic_id"]

    with get_db() as conn:
        # 检查是否已存在
        existing = conn.execute(
            "SELECT id FROM favorites WHERE user_id = ? AND topic_id = ?",
            (g.user["sub"], topic_id)
        ).fetchone()

        if existing:
            return jsonify({"detail": "已收藏"}), 400

        conn.execute(
            "INSERT INTO favorites (user_id, topic_id) VALUES (?, ?)",
            (g.user["sub"], topic_id)
        )

    # 添加积分
    achievements_service.add_points(g.user["sub"], 2, "favorite", topic_id)

    # 检查成就
    achievements_service.check_and_award_achievements(g.user["sub"])

    return jsonify({"ok": True})


@favorites_bp.route("/favorites/<topic_id>", methods=["DELETE"])
@login_required
def remove_favorite(topic_id):
    """取消收藏"""
    with get_db() as conn:
        conn.execute(
            "DELETE FROM favorites WHERE user_id = ? AND topic_id = ?",
            (g.user["sub"], topic_id)
        )
    return jsonify({"ok": True})


@favorites_bp.route("/favorites/check/<topic_id>", methods=["GET"])
@login_required
def check_favorite(topic_id):
    """检查是否已收藏"""
    with get_db() as conn:
        existing = conn.execute(
            "SELECT id FROM favorites WHERE user_id = ? AND topic_id = ?",
            (g.user["sub"], topic_id)
        ).fetchone()
        return jsonify({"is_favorited": existing is not None})


# ========== 笔记 ==========

@favorites_bp.route("/notes", methods=["GET"])
@login_required
def get_notes():
    """获取笔记列表"""
    topic_id = request.args.get("topic_id")

    with get_db() as conn:
        if topic_id:
            rows = conn.execute(
                """SELECT * FROM notes WHERE user_id = ? AND topic_id = ?
                   ORDER BY updated_at DESC""",
                (g.user["sub"], topic_id)
            ).fetchall()
        else:
            rows = conn.execute(
                """SELECT n.*, t.title as topic_title, t.icon as topic_icon
                   FROM notes n
                   JOIN topics t ON n.topic_id = t.id
                   WHERE n.user_id = ?
                   ORDER BY n.updated_at DESC""",
                (g.user["sub"],)
            ).fetchall()
        return jsonify([dict(r) for r in rows])


@favorites_bp.route("/notes", methods=["POST"])
@login_required
def add_note():
    """添加笔记"""
    data = request.get_json()
    if not data or not data.get("topic_id") or not data.get("content"):
        return jsonify({"detail": "topic_id 和 content 不能为空"}), 400

    with get_db() as conn:
        cursor = conn.execute(
            """INSERT INTO notes (user_id, topic_id, section_id, content)
               VALUES (?, ?, ?, ?)""",
            (g.user["sub"], data["topic_id"], data.get("section_id"), data["content"])
        )
        note_id = cursor.lastrowid

    # 添加积分
    achievements_service.add_points(g.user["sub"], 3, "note", str(note_id))

    # 检查成就
    achievements_service.check_and_award_achievements(g.user["sub"])

    return jsonify({"ok": True, "id": note_id})


@favorites_bp.route("/notes/<int:note_id>", methods=["PUT"])
@login_required
def update_note(note_id):
    """更新笔记"""
    data = request.get_json()
    if not data or not data.get("content"):
        return jsonify({"detail": "content 不能为空"}), 400

    with get_db() as conn:
        conn.execute(
            """UPDATE notes SET content = ?, updated_at = CURRENT_TIMESTAMP
               WHERE id = ? AND user_id = ?""",
            (data["content"], note_id, g.user["sub"])
        )
    return jsonify({"ok": True})


@favorites_bp.route("/notes/<int:note_id>", methods=["DELETE"])
@login_required
def delete_note(note_id):
    """删除笔记"""
    with get_db() as conn:
        conn.execute(
            "DELETE FROM notes WHERE id = ? AND user_id = ?",
            (note_id, g.user["sub"])
        )
    return jsonify({"ok": True})
