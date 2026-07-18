"""AI 内容生成 API"""
import json
from fastapi import APIRouter, Depends
from database import get_db
from auth import get_current_user
from models import AIDeriveRequest, AIExplainRequest, AIResponse
from services.ai_service import generate_derivation, generate_quiz, explain_wrong_answer, get_prompt_hash

router = APIRouter(prefix="/api/ai", tags=["ai"])


@router.post("/derive", response_model=AIResponse)
def ai_derive(data: AIDeriveRequest, user=Depends(get_current_user)):
    prompt_hash = get_prompt_hash(data.topic_id, data.extra_context or "")

    # 检查缓存
    with get_db() as conn:
        cached = conn.execute(
            "SELECT content FROM ai_content_cache WHERE topic_id = ? AND prompt_hash = ?",
            (data.topic_id, prompt_hash)
        ).fetchone()
        if cached:
            return AIResponse(content=cached["content"], cached=True)

        # 获取主题信息
        topic = conn.execute("SELECT title, description FROM topics WHERE id = ?", (data.topic_id,)).fetchone()
        if not topic:
            return AIResponse(content=json.dumps({"error": "主题不存在"}))

    # 生成内容
    content = generate_derivation(topic["title"], topic["description"], data.extra_context)

    # 缓存
    with get_db() as conn:
        conn.execute(
            "INSERT OR IGNORE INTO ai_content_cache (topic_id, prompt_hash, content) VALUES (?, ?, ?)",
            (data.topic_id, prompt_hash, content)
        )

    return AIResponse(content=content, cached=False)


@router.post("/quiz")
def ai_quiz(data: AIDeriveRequest, user=Depends(get_current_user)):
    with get_db() as conn:
        topic = conn.execute("SELECT title, description FROM topics WHERE id = ?", (data.topic_id,)).fetchone()
        if not topic:
            return {"questions": []}

    content = generate_quiz(topic["title"], topic["description"])
    return json.loads(content)


@router.post("/explain", response_model=AIResponse)
def ai_explain(data: AIExplainRequest, user=Depends(get_current_user)):
    content = explain_wrong_answer(
        data.question, data.user_answer, data.correct_answer, data.topic_title or ""
    )
    return AIResponse(content=content, cached=False)
