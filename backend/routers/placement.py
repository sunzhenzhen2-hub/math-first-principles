"""定位测试 API"""
import json
from fastapi import APIRouter, HTTPException, Depends
from database import get_db
from auth import get_current_user
from models import PlacementQuestion, PlacementSubmit, PlacementResult

router = APIRouter(prefix="/api/placement", tags=["placement"])

STAGES = [
    "数的起源", "代数语言", "几何直觉", "函数世界",
    "变化的科学", "抽象与推理", "高等数学"
]


@router.get("/questions", response_model=list[PlacementQuestion])
def get_questions():
    """获取所有定位测试题（不包含答案）"""
    with get_db() as conn:
        rows = conn.execute(
            "SELECT * FROM placement_questions ORDER BY sort_order"
        ).fetchall()
        return [PlacementQuestion(
            id=r["id"],
            stage_index=r["stage_index"],
            difficulty=r["difficulty"],
            question=r["question"],
            options=json.loads(r["options"]),
            explanation=r["explanation"]
        ) for r in rows]


@router.post("/submit", response_model=PlacementResult)
def submit(data: PlacementSubmit, user=Depends(get_current_user)):
    """提交定位测试答案，返回推荐阶段"""
    with get_db() as conn:
        # 获取正确答案
        question_ids = [a.question_id for a in data.answers]
        if not question_ids:
            raise HTTPException(400, "没有提交任何答案")

        placeholders = ",".join(["?"] * len(question_ids))
        rows = conn.execute(
            f"SELECT id, stage_index, answer FROM placement_questions WHERE id IN ({placeholders})",
            question_ids
        ).fetchall()
        answer_map = {r["id"]: (r["stage_index"], r["answer"]) for r in rows}

        # 统计每个阶段的正确数
        stage_correct = {i: 0 for i in range(len(STAGES))}
        stage_total = {i: 0 for i in range(len(STAGES))}

        for a in data.answers:
            if a.question_id not in answer_map:
                continue
            stage_idx, correct_ans = answer_map[a.question_id]
            stage_total[stage_idx] = stage_total.get(stage_idx, 0) + 1
            if a.selected == correct_ans:
                stage_correct[stage_idx] = stage_correct.get(stage_idx, 0) + 1

        # 推荐逻辑：找到最后一个全部答对的阶段，推荐下一阶段
        recommended = 0
        for i in range(len(STAGES)):
            if stage_total.get(i, 0) > 0 and stage_correct.get(i, 0) == stage_total.get(i, 0):
                recommended = i + 1  # 全对，可以跳到下一阶段
            elif stage_total.get(i, 0) > 0 and stage_correct.get(i, 0) > 0:
                recommended = i  # 部分对，从当前阶段开始
                break
            elif stage_total.get(i, 0) > 0 and stage_correct.get(i, 0) == 0:
                recommended = i  # 全错，从当前阶段开始
                break

        # 不能超过最大阶段
        recommended = min(recommended, len(STAGES) - 1)

        # 构建阶段详情
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

        return PlacementResult(
            recommended_stage=recommended,
            stage_name=STAGES[recommended],
            correct_count=total_correct,
            total_answered=total_answered,
            stage_details=details
        )
