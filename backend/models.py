"""Pydantic 数据模型"""
from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime


# ── 认证 ──

class UserRegister(BaseModel):
    username: str
    email: str
    password: str


class UserLogin(BaseModel):
    username: str
    password: str


class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    created_at: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


# ── 主题 ──

class TopicResponse(BaseModel):
    id: str
    stage: str
    stage_index: int
    title: str
    description: Optional[str]
    icon: Optional[str]
    sort_order: int


class LessonSection(BaseModel):
    type: str  # title, text, highlight, formula, ex, hint
    content: str


class QuizQuestion(BaseModel):
    question: str
    options: List[str]
    answer: int
    explanation: str


class TopicDetail(TopicResponse):
    lesson: List[LessonSection]
    quiz: List[QuizQuestion]


# ── 进度 ──

class ProgressUpdate(BaseModel):
    topic_id: str
    stars: int
    score: int
    total: int


class ProgressResponse(BaseModel):
    topic_id: str
    stars: int
    tests_taken: int
    tests_passed: int
    best_score: int
    completed_at: Optional[str]


# ── 错题 ──

class WrongAnswerResponse(BaseModel):
    id: int
    topic_id: str
    question: str
    user_answer: str
    correct_answer: str
    explanation: Optional[str]
    created_at: str


# ── AI ──

class AIDeriveRequest(BaseModel):
    topic_id: str
    extra_context: Optional[str] = None


class AIExplainRequest(BaseModel):
    question: str
    user_answer: str
    correct_answer: str
    topic_title: Optional[str] = None


class AIResponse(BaseModel):
    content: str
    cached: bool = False


# ── 定位测试 ──

class PlacementQuestion(BaseModel):
    id: int
    stage_index: int
    difficulty: int
    question: str
    options: List[str]
    explanation: str  # 答错后显示


class PlacementAnswer(BaseModel):
    question_id: int
    selected: int  # 用户选择的选项索引


class PlacementSubmit(BaseModel):
    answers: List[PlacementAnswer]


class PlacementResult(BaseModel):
    recommended_stage: int
    stage_name: str
    correct_count: int
    total_answered: int
    stage_details: List[dict]  # 每个阶段的答题情况
