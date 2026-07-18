"""AI 内容生成服务"""
import hashlib
import json
from config import OPENAI_API_KEY, OPENAI_MODEL


def _get_client():
    if not OPENAI_API_KEY:
        return None
    try:
        from openai import OpenAI
        return OpenAI(api_key=OPENAI_API_KEY)
    except ImportError:
        return None


def generate_derivation(topic_title: str, topic_description: str, extra_context: str = None) -> str:
    """生成第一性原理推导过程"""
    client = _get_client()
    if not client:
        return _fallback_derivation(topic_title, topic_description)

    prompt = f"""你是一位数学教育专家，擅长用第一性原理解释数学概念。

请为「{topic_title}」生成一个推导式学习内容。

要求：
1. 从最基本的事实出发，一步步推导出核心概念
2. 每一步都要解释"为什么"，不只是"是什么"
3. 结合数形结合思想，描述对应的图形/可视化
4. 使用中文，数学术语附英文
5. 包含具体例子

输出 JSON 格式：
{{"steps": [{{"title": "步骤标题", "content": "推导内容", "formula": "公式（可选）", "hint": "直觉提示（可选）"}}]}}

主题描述：{topic_description}
{f'补充信息：{extra_context}' if extra_context else ''}"""

    response = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"},
        temperature=0.7
    )
    return response.choices[0].message.content


def generate_quiz(topic_title: str, topic_description: str, count: int = 3) -> str:
    """生成练习题"""
    client = _get_client()
    if not client:
        return json.dumps({"questions": []})

    prompt = f"""为「{topic_title}」生成 {count} 道选择题。

要求：
- 每题 4 个选项，1 个正确答案
- 难度适中，考察理解而非死记
- 包含详细解析

输出 JSON：{{"questions": [{{"question": "...", "options": ["A","B","C","D"], "answer": 0, "explanation": "..."}}]}}

主题描述：{topic_description}"""

    response = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"},
        temperature=0.7
    )
    return response.choices[0].message.content


def explain_wrong_answer(question: str, user_answer: str, correct_answer: str, topic_title: str = "") -> str:
    """解释错题"""
    client = _get_client()
    if not client:
        return f"正确答案是 {correct_answer}。你的答案 {user_answer} 不正确。"

    prompt = f"""学生做错了一道数学题，请用第一性原理解释为什么正确答案是 {correct_answer}。

题目：{question}
学生答案：{user_answer}
正确答案：{correct_answer}
相关主题：{topic_title}

要求：
1. 先指出错误所在
2. 从基本原理出发解释正确解法
3. 给出记忆/直觉提示
4. 简洁明了，200 字以内"""

    response = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.5
    )
    return response.choices[0].message.content


def _fallback_derivation(topic_title: str, topic_description: str) -> str:
    """无 API key 时的回退内容"""
    return json.dumps({
        "steps": [
            {"title": "什么是" + topic_title, "content": topic_description or "这是一个重要的数学概念。"},
            {"title": "核心思想", "content": "从第一性原理出发，我们需要理解最基本的事实。"},
            {"title": "数形结合", "content": "结合图形可以更好地理解这个概念。"},
            {"title": "总结", "content": f"{topic_title}是数学中重要的基础概念，理解它需要从本质出发。"}
        ]
    })


def get_prompt_hash(topic_id: str, extra: str = "") -> str:
    return hashlib.md5(f"{topic_id}:{extra}".encode()).hexdigest()
