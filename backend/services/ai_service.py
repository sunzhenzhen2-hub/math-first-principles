"""AI 内容生成服务 — 公理 / 定理 / 证明（表述须严谨，禁止套话）"""
import hashlib
import json
import re
from config import AI_API_KEY, AI_BASE_URL, AI_MODEL
from services.axiom_theorem_bank import (
    lookup_bank,
    bank_as_prompt_context,
    bank_as_json,
    ensure_content_has_graph,
)

DERIVE_CACHE_VERSION = "derive-v6"

# 命中即视为套话，整段删除或回退到题库
PLATITUDE_MARKERS = [
    "不是孤立的知识点",
    "数学大厦",
    "一块砖",
    "知识网络",
    "记忆碎片",
    "从第一性原理理解",
    "活生生的思想",
    "通用思维框架",
    "总结与展望",
    "继续加油",
    "数学的灵魂",
    "金钥匙",
    "桥梁",
    "预告片",
    "游戏规则",
    "数字的「家」",
    "数字的家",
    "深刻而持久",
    "最伟大的公式",
    "伟大的公式",
]


def _get_client():
    if not AI_API_KEY:
        return None
    try:
        from openai import OpenAI
        return OpenAI(api_key=AI_API_KEY, base_url=AI_BASE_URL)
    except ImportError:
        return None


def _clean_json_content(raw: str) -> str:
    content = (raw or "").strip()
    if content.startswith("```"):
        lines = content.split("\n")
        if lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        content = "\n".join(lines).strip()
    return content


def _text_has_platitude(text: str) -> bool:
    if not text:
        return False
    return any(m in text for m in PLATITUDE_MARKERS)


def _scrub_text(text: str) -> str:
    """删除含套话的句子； scrub 后若过短则返回空串。"""
    if not text or not _text_has_platitude(text):
        return text or ""
    parts = re.split(r"(?<=[。！？；\n])", text)
    kept = [p for p in parts if p and not _text_has_platitude(p)]
    out = "".join(kept).strip()
    return out


def _scrub_proof_steps(steps: list) -> list:
    cleaned = []
    for step in steps or []:
        if not isinstance(step, dict):
            continue
        s = dict(step)
        for key in ("content", "hint", "example", "title", "reason"):
            if key in s and isinstance(s[key], str):
                s[key] = _scrub_text(s[key])
        # 套话 scrub 后正文被掏空 → 丢掉该步
        if not (s.get("content") or s.get("formula") or s.get("reason")):
            continue
        # 空 hint 删掉，避免前端显示空口号
        if not s.get("hint"):
            s.pop("hint", None)
        cleaned.append(s)
    return cleaned


def sanitize_derivation_payload(parsed: dict, bank_entry: dict = None) -> dict:
    """清洗 AI/回退 JSON：去套话；证明被掏空则用题库。"""
    if not isinstance(parsed, dict):
        return bank_entry or {"proof": [], "steps": []}

    out = dict(parsed)

    if isinstance(out.get("analogy"), str):
        out["analogy"] = _scrub_text(out["analogy"])
        if not out["analogy"]:
            out.pop("analogy", None)

    if isinstance(out.get("plain_summary"), str):
        out["plain_summary"] = _scrub_text(out["plain_summary"])
        if not out["plain_summary"] and bank_entry:
            out["plain_summary"] = bank_entry.get("plain_summary")

    th = out.get("theorem")
    if isinstance(th, dict):
        th = dict(th)
        for k in ("name", "statement", "plain"):
            if isinstance(th.get(k), str):
                th[k] = _scrub_text(th[k]) if _text_has_platitude(th[k]) else th[k]
        if not th.get("statement") and bank_entry and bank_entry.get("theorem"):
            th = bank_entry["theorem"]
        out["theorem"] = th

    axioms = []
    for ax in out.get("axioms") or []:
        if not isinstance(ax, dict):
            continue
        ax = dict(ax)
        for k in ("name", "statement", "plain"):
            if isinstance(ax.get(k), str) and _text_has_platitude(ax[k]):
                ax[k] = _scrub_text(ax[k])
        if ax.get("statement"):
            axioms.append(ax)
    if axioms:
        out["axioms"] = axioms
    elif bank_entry and bank_entry.get("axioms"):
        out["axioms"] = bank_entry["axioms"]

    proof = _scrub_proof_steps(out.get("proof") or out.get("steps") or [])
    if len(proof) < 2 and bank_entry and (bank_entry.get("proof") or bank_entry.get("steps")):
        proof = bank_entry.get("proof") or bank_entry.get("steps")
    out["proof"] = proof
    out["steps"] = proof
    return out


def generate_derivation(
    topic_title: str,
    topic_description: str,
    extra_context: str = None,
    topic_id: str = None,
) -> str:
    """生成公理、定理与证明。表述只允许数学内容，禁止套话。"""
    bank_entry = lookup_bank(topic_id=topic_id, topic_title=topic_title)
    client = _get_client()
    if not client:
        return _fallback_derivation(topic_title, topic_description, topic_id=topic_id)

    bank_block = bank_as_prompt_context(bank_entry) if bank_entry else ""

    prompt = f"""你是数学教师，只输出可检验的数学内容（定义、公理、定理、证明、公式、计算）。
读者是来做题与读证明的，不是来听励志演讲的。

主题：{topic_title}
描述：{topic_description}
{f'补充：{extra_context}' if extra_context else ''}

{bank_block}

输出合法 JSON（不要 markdown 围栏），字段：
{{
  "axioms": [{{"name":"名称","statement":"形式化陈述","plain":"一句精确释义（可省略空话）"}}],
  "theorem": {{"name":"...","statement":"形式化命题","plain":"精确释义"}},
  "given": "已知…",
  "to_prove": "求证…",
  "proof": [{{
    "title": "步骤标题（如：构造 / 归纳 / 化简）",
    "content": "证明正文（含推理）",
    "formula": "关键式子",
    "reason": "本步依据（公理名/定义/已证定理）",
    "example": "可选：具体数值验算",
    "graph": {{
      "expressions": [{{"latex":"y=x^2","color":"#c87832"}}],
      "bounds": {{"left":-5,"right":5,"bottom":-2,"top":10}},
      "description": "图中对象说明"
    }}
  }}],
  "steps": [],
  "plain_summary": "用两三句复述：定理内容 + 证明主线（必须含公式或命题，禁止口号）"
}}

规则：
1. proof 至少 3 步；steps 必须与 proof 相同。
2. 每步必须有 reason；禁止只有比喻没有推理。
3. 至少一步含 graph（坐标系：y=… / (x,y) / segment((x1,y1),(x2,y2))）。
4. analogy 字段不要输出（不要比喻段）。
5. 禁止出现：孤立的知识点、数学大厦、一块砖、知识网络、记忆碎片、第一性原理思维、活生生、通用思维框架、总结与展望、灵魂、金钥匙、桥梁（比喻义）、加油、预告片、游戏规则。
6. plain / plain_summary 只能解释数学对象，例如「n 边形内角和等于 (n-2)×180°」，禁止「理解联系」「建立网络」之类。
7. 全文中文。"""

    response = client.chat.completions.create(
        model=AI_MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
        max_tokens=4000,
    )
    content = _clean_json_content(response.choices[0].message.content)

    try:
        parsed = json.loads(content)
        if bank_entry:
            for key in ("axioms", "theorem", "plain_summary", "given", "to_prove"):
                if not parsed.get(key) and bank_entry.get(key):
                    parsed[key] = bank_entry.get(key)
            if not parsed.get("proof") and bank_entry.get("proof"):
                parsed["proof"] = bank_entry["proof"]
        if parsed.get("proof") and not parsed.get("steps"):
            parsed["steps"] = parsed["proof"]
        elif parsed.get("steps") and not parsed.get("proof"):
            parsed["proof"] = parsed["steps"]
        # 丢弃比喻段
        parsed.pop("analogy", None)
        if "proof" not in parsed and "steps" not in parsed:
            if bank_entry:
                return bank_as_json(bank_entry)
            parsed = {"steps": [{"title": "结果", "content": content}], "proof": []}
        parsed = sanitize_derivation_payload(parsed, bank_entry)
        if _text_has_platitude(json.dumps(parsed, ensure_ascii=False)) and bank_entry:
            return bank_as_json(bank_entry)
        parsed = ensure_content_has_graph(parsed, topic_id=topic_id, topic_title=topic_title)
        return json.dumps(parsed, ensure_ascii=False)
    except (json.JSONDecodeError, ValueError):
        if bank_entry:
            return bank_as_json(bank_entry)
        return json.dumps(
            {
                "proof": [{"title": "解析失败", "content": "模型未返回合法 JSON。", "reason": "输出格式错误"}],
                "steps": [{"title": "解析失败", "content": "模型未返回合法 JSON。", "reason": "输出格式错误"}],
            },
            ensure_ascii=False,
        )


def generate_quiz(topic_title: str, topic_description: str, count: int = 3) -> str:
    """生成练习题"""
    client = _get_client()
    if not client:
        return json.dumps({"questions": []})

    prompt = f"""为「{topic_title}」生成 {count} 道选择题。

要求：
- 每题 4 个选项，1 个正确答案（answer 为 0–3 的下标）
- 考查定义、计算或定理应用；解析写清推理，禁止套话
- 禁止：知识网络、数学大厦、第一性原理思维、加油 等空话

输出 JSON：{{"questions":[{{"question":"...","options":["A","B","C","D"],"answer":0,"explanation":"..."}}]}}

主题描述：{topic_description}"""

    response = client.chat.completions.create(
        model=AI_MODEL,
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"},
        temperature=0.5,
    )
    return response.choices[0].message.content


def explain_wrong_answer(question: str, user_answer: str, correct_answer: str, topic_title: str = "") -> str:
    """解释错题：只给错误点与正确推理"""
    client = _get_client()
    if not client:
        return f"正确答案是 {correct_answer}。你的答案是 {user_answer}。"

    prompt = f"""指出错因并给出正确解法（≤180字）。只写数学推理，不要励志或套话。

题目：{question}
学生答案：{user_answer}
正确答案：{correct_answer}
主题：{topic_title}

格式：
1) 错在哪里（对应哪一步/哪个概念）
2) 正确做法（含关键式子）
禁止：知识网络、数学大厦、第一性原理、加油、灵魂、金钥匙。"""

    response = client.chat.completions.create(
        model=AI_MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
    )
    text = response.choices[0].message.content or ""
    scrubbed = _scrub_text(text)
    return scrubbed or text


def _missing_bank_payload(topic_title: str, topic_description: str) -> dict:
    return {
        "axioms": [
            {
                "name": "待补充：基本定义或公理",
                "statement": f"需给出与「{topic_description or topic_title}」相关的形式化定义/公理。",
                "plain": "无具体陈述时不得用空话填充。",
            }
        ],
        "theorem": {
            "name": f"「{topic_title}」核心定理（待收录）",
            "statement": "此处应写可判定真伪的数学命题。",
            "plain": "例如内角和公式、判定定理、运算法则等。",
        },
        "given": "（依具体定理填写）",
        "to_prove": "（依具体定理填写）",
        "proof": [
            {
                "title": "题库未收录",
                "content": f"离线证明库尚无「{topic_title}」。请补充 axiom_theorem_bank，或配置 AI_API_KEY 生成证明。",
                "reason": "数据缺失提示",
            }
        ],
        "steps": [
            {
                "title": "题库未收录",
                "content": f"离线证明库尚无「{topic_title}」。请补充 axiom_theorem_bank，或配置 AI_API_KEY 生成证明。",
                "reason": "数据缺失提示",
            }
        ],
        "plain_summary": f"「{topic_title}」暂无内置证明；应提供定理陈述与逐步证明，而非概括性套话。",
    }


def _fallback_derivation(topic_title: str, topic_description: str, topic_id: str = None) -> str:
    """无 API 时：只用题库；无题库则明确「未收录」，绝不灌套话。"""
    bank_entry = lookup_bank(topic_id=topic_id, topic_title=topic_title)
    if bank_entry:
        payload = sanitize_derivation_payload(dict(bank_entry), bank_entry)
        payload.pop("analogy", None)
        return json.dumps(payload, ensure_ascii=False)
    return json.dumps(
        _missing_bank_payload(topic_title, topic_description or ""),
        ensure_ascii=False,
    )


def get_prompt_hash(topic_id: str, extra: str = "") -> str:
    return hashlib.md5(f"{topic_id}:{extra}:{DERIVE_CACHE_VERSION}".encode()).hexdigest()
