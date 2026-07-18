"""课程内容 API — Flask Blueprint"""
import json
from flask import Blueprint, jsonify
from database import get_db

content_bp = Blueprint("content", __name__, url_prefix="/api/topics")


@content_bp.route("", methods=["GET"])
def list_topics():
    with get_db() as conn:
        rows = conn.execute("SELECT * FROM topics ORDER BY sort_order").fetchall()
        return jsonify([dict(r) for r in rows])


@content_bp.route("/<topic_id>", methods=["GET"])
def get_topic(topic_id):
    with get_db() as conn:
        topic = conn.execute("SELECT * FROM topics WHERE id = ?", (topic_id,)).fetchone()
        if not topic:
            return jsonify({"detail": "主题不存在"}), 404

        lesson_rows = conn.execute(
            "SELECT section_type, content FROM lesson_sections WHERE topic_id = ? ORDER BY sort_order",
            (topic_id,)
        ).fetchall()
        lesson = [{"type": r["section_type"], "content": r["content"]} for r in lesson_rows]

        quiz_rows = conn.execute(
            "SELECT question, options, answer, explanation FROM quiz_questions WHERE topic_id = ? ORDER BY sort_order",
            (topic_id,)
        ).fetchall()
        quiz = [{
            "question": r["question"],
            "options": json.loads(r["options"]),
            "answer": r["answer"],
            "explanation": r["explanation"]
        } for r in quiz_rows]

        result = dict(topic)
        result["lesson"] = lesson
        result["quiz"] = quiz
        return jsonify(result)
