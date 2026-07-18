"""学习进度 API"""
from fastapi import APIRouter, Depends
from database import get_db
from auth import get_current_user
from models import ProgressUpdate, ProgressResponse, WrongAnswerResponse

router = APIRouter(prefix="/api", tags=["progress"])


@router.get("/progress", response_model=list[ProgressResponse])
def get_progress(user=Depends(get_current_user)):
    with get_db() as conn:
        rows = conn.execute(
            "SELECT topic_id, stars, tests_taken, tests_passed, best_score, completed_at FROM progress WHERE user_id = ?",
            (user["sub"],)
        ).fetchall()
        return [ProgressResponse(
            topic_id=r["topic_id"], stars=r["stars"],
            tests_taken=r["tests_taken"], tests_passed=r["tests_passed"],
            best_score=r["best_score"], completed_at=str(r["completed_at"]) if r["completed_at"] else None
        ) for r in rows]


@router.post("/progress")
def update_progress(data: ProgressUpdate, user=Depends(get_current_user)):
    with get_db() as conn:
        existing = conn.execute(
            "SELECT id, stars, best_score FROM progress WHERE user_id = ? AND topic_id = ?",
            (user["sub"], data.topic_id)
        ).fetchone()

        passed = data.score >= data.total * 0.4
        if existing:
            new_stars = max(existing["stars"], data.stars)
            new_best = max(existing["best_score"], data.score)
            conn.execute(
                """UPDATE progress SET stars = ?, tests_taken = tests_taken + 1,
                   tests_passed = tests_passed + ?, best_score = ?,
                   completed_at = CASE WHEN ? >= 2 THEN CURRENT_TIMESTAMP ELSE completed_at END
                   WHERE id = ?""",
                (new_stars, 1 if passed else 0, new_best, data.stars, existing["id"])
            )
        else:
            conn.execute(
                """INSERT INTO progress (user_id, topic_id, stars, tests_taken, tests_passed, best_score, completed_at)
                   VALUES (?, ?, ?, 1, ?, ?, CASE WHEN ? >= 2 THEN CURRENT_TIMESTAMP ELSE NULL END)""",
                (user["sub"], data.topic_id, data.stars, 1 if passed else 0, data.score, data.stars)
            )
        return {"ok": True}


@router.get("/wrong-answers", response_model=list[WrongAnswerResponse])
def get_wrong_answers(user=Depends(get_current_user)):
    with get_db() as conn:
        rows = conn.execute(
            "SELECT * FROM wrong_answers WHERE user_id = ? ORDER BY created_at DESC",
            (user["sub"],)
        ).fetchall()
        return [WrongAnswerResponse(
            id=r["id"], topic_id=r["topic_id"], question=r["question"],
            user_answer=r["user_answer"], correct_answer=r["correct_answer"],
            explanation=r["explanation"], created_at=str(r["created_at"])
        ) for r in rows]


@router.post("/wrong-answers")
def add_wrong_answer(data: dict, user=Depends(get_current_user)):
    with get_db() as conn:
        conn.execute(
            "INSERT INTO wrong_answers (user_id, topic_id, question, user_answer, correct_answer, explanation) VALUES (?, ?, ?, ?, ?, ?)",
            (user["sub"], data["topic_id"], data["question"], data["user_answer"], data["correct_answer"], data.get("explanation"))
        )
    return {"ok": True}


@router.delete("/wrong-answers/{item_id}")
def delete_wrong_answer(item_id: int, user=Depends(get_current_user)):
    with get_db() as conn:
        conn.execute("DELETE FROM wrong_answers WHERE id = ? AND user_id = ?", (item_id, user["sub"]))
    return {"ok": True}
