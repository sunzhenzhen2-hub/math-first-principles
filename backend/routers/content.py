"""课程内容 API"""
from fastapi import APIRouter, HTTPException
from database import get_db
from models import TopicResponse, TopicDetail

router = APIRouter(prefix="/api/topics", tags=["topics"])


@router.get("", response_model=list[TopicResponse])
def list_topics():
    with get_db() as conn:
        rows = conn.execute("SELECT * FROM topics ORDER BY sort_order").fetchall()
        return [TopicResponse(**dict(r)) for r in rows]


@router.get("/{topic_id}", response_model=TopicDetail)
def get_topic(topic_id: str):
    with get_db() as conn:
        topic = conn.execute("SELECT * FROM topics WHERE id = ?", (topic_id,)).fetchone()
        if not topic:
            raise HTTPException(404, "主题不存在")

        # 从课程内容表获取
        lesson_rows = conn.execute(
            "SELECT section_type, content FROM lesson_sections WHERE topic_id = ? ORDER BY sort_order",
            (topic_id,)
        ).fetchall()
        lesson = [{"type": r["section_type"], "content": r["content"]} for r in lesson_rows]

        quiz_rows = conn.execute(
            "SELECT question, options, answer, explanation FROM quiz_questions WHERE topic_id = ? ORDER BY sort_order",
            (topic_id,)
        ).fetchall()
        import json
        quiz = [{
            "question": r["question"],
            "options": json.loads(r["options"]),
            "answer": r["answer"],
            "explanation": r["explanation"]
        } for r in quiz_rows]

        return TopicDetail(
            id=topic["id"],
            stage=topic["stage"],
            stage_index=topic["stage_index"],
            title=topic["title"],
            description=topic["description"],
            icon=topic["icon"],
            sort_order=topic["sort_order"],
            lesson=lesson,
            quiz=quiz
        )
