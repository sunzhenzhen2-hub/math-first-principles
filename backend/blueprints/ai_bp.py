"""AI 内容生成 API — Flask Blueprint"""
import json
from flask import Blueprint, request, jsonify, g
from database import get_db
from auth import login_required
from services.ai_service import generate_derivation, generate_quiz, explain_wrong_answer, get_prompt_hash

ai_bp = Blueprint("ai", __name__, url_prefix="/api/ai")


@ai_bp.route("/derive", methods=["POST"])
@login_required
def ai_derive():
    data = request.get_json()
    if not data:
        return jsonify({"detail": "请求体为空"}), 400

    topic_id = data.get("topic_id")
    extra_context = data.get("extra_context", "")

    if not topic_id:
        return jsonify({"detail": "topic_id 不能为空"}), 400

    prompt_hash = get_prompt_hash(topic_id, extra_context or "")

    with get_db() as conn:
        cached = conn.execute(
            "SELECT content FROM ai_content_cache WHERE topic_id = ? AND prompt_hash = ?",
            (topic_id, prompt_hash)
        ).fetchone()
        if cached:
            return jsonify({"content": cached["content"], "cached": True})

        topic = conn.execute("SELECT title, description FROM topics WHERE id = ?", (topic_id,)).fetchone()
        if not topic:
            return jsonify({"content": json.dumps({"error": "主题不存在"})})

    content = generate_derivation(topic["title"], topic["description"], extra_context)

    with get_db() as conn:
        conn.execute(
            "INSERT OR IGNORE INTO ai_content_cache (topic_id, prompt_hash, content) VALUES (?, ?, ?)",
            (topic_id, prompt_hash, content)
        )

    return jsonify({"content": content, "cached": False})


@ai_bp.route("/quiz", methods=["POST"])
@login_required
def ai_quiz():
    data = request.get_json()
    if not data:
        return jsonify({"detail": "请求体为空"}), 400

    topic_id = data.get("topic_id")
    if not topic_id:
        return jsonify({"detail": "topic_id 不能为空"}), 400

    with get_db() as conn:
        topic = conn.execute("SELECT title, description FROM topics WHERE id = ?", (topic_id,)).fetchone()
        if not topic:
            return jsonify({"questions": []})

    content = generate_quiz(topic["title"], topic["description"])
    return jsonify(json.loads(content))


@ai_bp.route("/explain", methods=["POST"])
@login_required
def ai_explain():
    data = request.get_json()
    if not data:
        return jsonify({"detail": "请求体为空"}), 400

    question = data.get("question")
    user_answer = data.get("user_answer")
    correct_answer = data.get("correct_answer")
    topic_title = data.get("topic_title", "")

    if not all([question, user_answer, correct_answer]):
        return jsonify({"detail": "缺少必填字段"}), 400

    content = explain_wrong_answer(question, user_answer, correct_answer, topic_title or "")
    return jsonify({"content": content, "cached": False})
