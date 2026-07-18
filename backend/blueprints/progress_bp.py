"""学习进度 API — Flask Blueprint"""
from flask import Blueprint, request, jsonify, g
from database import get_db
from auth import login_required

progress_bp = Blueprint("progress", __name__, url_prefix="/api")


@progress_bp.route("/progress", methods=["GET"])
@login_required
def get_progress():
    with get_db() as conn:
        rows = conn.execute(
            "SELECT topic_id, stars, tests_taken, tests_passed, best_score, completed_at FROM progress WHERE user_id = ?",
            (g.user["sub"],)
        ).fetchall()
        return jsonify([{
            "topic_id": r["topic_id"],
            "stars": r["stars"],
            "tests_taken": r["tests_taken"],
            "tests_passed": r["tests_passed"],
            "best_score": r["best_score"],
            "completed_at": str(r["completed_at"]) if r["completed_at"] else None
        } for r in rows])


@progress_bp.route("/progress", methods=["POST"])
@login_required
def update_progress():
    data = request.get_json()
    if not data:
        return jsonify({"detail": "请求体为空"}), 400

    topic_id = data.get("topic_id")
    stars = data.get("stars", 0)
    score = data.get("score", 0)
    total = data.get("total", 1)

    if not topic_id:
        return jsonify({"detail": "topic_id 不能为空"}), 400

    with get_db() as conn:
        existing = conn.execute(
            "SELECT id, stars, best_score FROM progress WHERE user_id = ? AND topic_id = ?",
            (g.user["sub"], topic_id)
        ).fetchone()

        passed = score >= total * 0.4
        if existing:
            new_stars = max(existing["stars"], stars)
            new_best = max(existing["best_score"], score)
            conn.execute(
                """UPDATE progress SET stars = ?, tests_taken = tests_taken + 1,
                   tests_passed = tests_passed + ?, best_score = ?,
                   completed_at = CASE WHEN ? >= 2 THEN CURRENT_TIMESTAMP ELSE completed_at END
                   WHERE id = ?""",
                (new_stars, 1 if passed else 0, new_best, stars, existing["id"])
            )
        else:
            conn.execute(
                """INSERT INTO progress (user_id, topic_id, stars, tests_taken, tests_passed, best_score, completed_at)
                   VALUES (?, ?, ?, 1, ?, ?, CASE WHEN ? >= 2 THEN CURRENT_TIMESTAMP ELSE NULL END)""",
                (g.user["sub"], topic_id, stars, 1 if passed else 0, score, stars)
            )
        return jsonify({"ok": True})


@progress_bp.route("/wrong-answers", methods=["GET"])
@login_required
def get_wrong_answers():
    with get_db() as conn:
        rows = conn.execute(
            "SELECT * FROM wrong_answers WHERE user_id = ? ORDER BY created_at DESC",
            (g.user["sub"],)
        ).fetchall()
        return jsonify([{
            "id": r["id"],
            "topic_id": r["topic_id"],
            "question": r["question"],
            "user_answer": r["user_answer"],
            "correct_answer": r["correct_answer"],
            "explanation": r["explanation"],
            "created_at": str(r["created_at"])
        } for r in rows])


@progress_bp.route("/wrong-answers", methods=["POST"])
@login_required
def add_wrong_answer():
    data = request.get_json()
    if not data:
        return jsonify({"detail": "请求体为空"}), 400

    topic_id = data.get("topic_id")
    question = data.get("question")
    user_answer = data.get("user_answer")
    correct_answer = data.get("correct_answer")

    if not all([topic_id, question, user_answer, correct_answer]):
        return jsonify({"detail": "缺少必填字段"}), 400

    with get_db() as conn:
        conn.execute(
            "INSERT INTO wrong_answers (user_id, topic_id, question, user_answer, correct_answer, explanation) VALUES (?, ?, ?, ?, ?, ?)",
            (g.user["sub"], topic_id, question, user_answer, correct_answer, data.get("explanation"))
        )
    return jsonify({"ok": True})


@progress_bp.route("/wrong-answers/<int:item_id>", methods=["DELETE"])
@login_required
def delete_wrong_answer(item_id):
    with get_db() as conn:
        conn.execute("DELETE FROM wrong_answers WHERE id = ? AND user_id = ?", (item_id, g.user["sub"]))
    return jsonify({"ok": True})
