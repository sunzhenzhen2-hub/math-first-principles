"""定位测试 API — Flask Blueprint"""
import json
from flask import Blueprint, request, jsonify, g
from database import get_db
from auth import login_required

placement_bp = Blueprint("placement", __name__, url_prefix="/api/placement")

STAGES = [
    "数的起源", "代数语言", "几何直觉", "函数世界",
    "变化的科学", "抽象与推理", "高等数学"
]


@placement_bp.route("/questions", methods=["GET"])
def get_questions():
    """获取所有定位测试题（不包含答案）"""
    with get_db() as conn:
        rows = conn.execute(
            "SELECT * FROM placement_questions ORDER BY sort_order"
        ).fetchall()
        return jsonify([{
            "id": r["id"],
            "stage_index": r["stage_index"],
            "difficulty": r["difficulty"],
            "question": r["question"],
            "options": json.loads(r["options"]),
            "explanation": r["explanation"]
        } for r in rows])


@placement_bp.route("/submit", methods=["POST"])
@login_required
def submit():
    """提交定位测试答案，返回推荐阶段"""
    data = request.get_json()
    if not data:
        return jsonify({"detail": "请求体为空"}), 400

    answers = data.get("answers", [])
    if not answers:
        return jsonify({"detail": "没有提交任何答案"}), 400

    with get_db() as conn:
        question_ids = [a["question_id"] for a in answers]
        placeholders = ",".join(["?"] * len(question_ids))
        rows = conn.execute(
            f"SELECT id, stage_index, answer FROM placement_questions WHERE id IN ({placeholders})",
            question_ids
        ).fetchall()
        answer_map = {r["id"]: (r["stage_index"], r["answer"]) for r in rows}

        stage_correct = {i: 0 for i in range(len(STAGES))}
        stage_total = {i: 0 for i in range(len(STAGES))}

        for a in answers:
            qid = a["question_id"]
            if qid not in answer_map:
                continue
            stage_idx, correct_ans = answer_map[qid]
            stage_total[stage_idx] = stage_total.get(stage_idx, 0) + 1
            if a["selected"] == correct_ans:
                stage_correct[stage_idx] = stage_correct.get(stage_idx, 0) + 1

        recommended = 0
        for i in range(len(STAGES)):
            if stage_total.get(i, 0) > 0 and stage_correct.get(i, 0) == stage_total.get(i, 0):
                recommended = i + 1
            elif stage_total.get(i, 0) > 0 and stage_correct.get(i, 0) > 0:
                recommended = i
                break
            elif stage_total.get(i, 0) > 0 and stage_correct.get(i, 0) == 0:
                recommended = i
                break

        recommended = min(recommended, len(STAGES) - 1)

        details = []
        for i in range(len(STAGES)):
            if stage_total.get(i, 0) > 0:
                details.append({
                    "stage": STAGES[i],
                    "correct": stage_correct[i],
                    "total": stage_total[i],
                    "passed": stage_correct[i] == stage_total[i]
                })

        total_correct = sum(stage_correct.values())
        total_answered = sum(stage_total.values())

        return jsonify({
            "recommended_stage": recommended,
            "stage_name": STAGES[recommended],
            "correct_count": total_correct,
            "total_answered": total_answered,
            "stage_details": details
        })
