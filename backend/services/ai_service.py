"""AI 内容生成服务 — 增强版（含图形）"""
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

    prompt = f"""你是一位资深数学教育专家，擅长用第一性原理解释数学概念。

请为「{topic_title}」生成一个详细的推导式学习内容。

要求：
1. 从最基本的事实出发，一步步推导出核心概念
2. 每一步都要解释"为什么"，不只是"是什么"
3. 结合数形结合思想，描述对应的图形/可视化
4. 使用中文，数学术语附英文
5. 包含具体例子和公式推导
6. 每个步骤内容要详细（至少100字），不能过于简短
7. 在适当步骤添加图形说明

输出 JSON 格式：
{{"steps": [{{"title": "步骤标题", "content": "详细推导内容（至少100字）", "formula": "公式（可选）", "hint": "直觉提示（可选）", "example": "具体例子（可选）", "graph": {{"expressions": [{{"latex": "y=x^2", "color": "#c87832"}}], "bounds": {{"left": -5, "right": 5, "bottom": -2, "top": 10}}, "description": "图形说明（可选）"}}（可选）}}]}}

主题描述：{topic_description}
{f'补充信息：{extra_context}' if extra_context else ''}"""

    response = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"},
        temperature=0.7,
        max_tokens=3000
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
    """无 API key 时的详细回退内容（含图形）"""
    derivations = {
        "自然数与计数": {
            "steps": [
                {
                    "title": "从「数」的需求开始",
                    "content": "想象你是一个远古人类，面前有一堆苹果。你不知道「3」是什么，但你能感受到「多」和「少」。这就是数学的起点——人类对数量的直觉感知。当我们说「这里有苹果」时，我们其实在做一件最基本的事：区分「有」和「没有」。",
                    "formula": "有 vs 没有 → 0 vs 1",
                    "hint": "数学起源于人类最基本的感知需求"
                },
                {
                    "title": "一一对应：计数的本质",
                    "content": "如何知道有多少个苹果？最原始的方法是「一一对应」：拿一个苹果，放一块石头；再拿一个，再放一块。最后数石头就知道苹果数量。这就是计数的本质——建立两个集合之间的双射（bijection）。不需要知道「3+2=5」，只需要能一一配对。",
                    "formula": "苹果 ↔ 石头（一一对应）",
                    "hint": "计数不是记忆数字，而是建立对应关系"
                },
                {
                    "title": "自然数的诞生：后继函数",
                    "content": "从1开始，每次加1，就能得到所有自然数。这就是皮亚诺公理（Peano Axioms）的核心思想：自然数是从1开始，每个数都有唯一的「后继」。1的后继是2，2的后继是3，以此类推。这告诉我们：自然数是无穷的，但每一个都是确定的。",
                    "formula": "1, S(1)=2, S(2)=3, S(3)=4, ...",
                    "hint": "自然数的本质是「一个接一个」的无穷过程"
                },
                {
                    "title": "加法：合并计数",
                    "content": "当你有3个苹果，又得到2个，总数是多少？加法就是「接着数」：从3开始，再数2个——4、5。所以3+2=5。加法的本质是两个计数过程的连接。这也解释了为什么加法满足交换律：先数A再数B，和先数B再数A，结果一样。",
                    "formula": "3 + 2 = S(S(3)) = 5",
                    "hint": "加法就是「接着数」"
                },
                {
                    "title": "数形结合：数轴",
                    "content": "把自然数画在一条直线上：0在原点，1在右边一个单位，2在两个单位...这就形成了数轴。数轴让我们「看见」数字的大小关系：右边的数总比左边的大。这也为负数、分数、实数的引入埋下伏笔。",
                    "formula": "0 → 1 → 2 → 3 → ...（向右无限延伸）",
                    "hint": "数轴是数字的「家」，所有数都住在这里",
                    "graph": {
                        "expressions": [
                            {"latex": "y=0", "color": "#888888", "lineStyle": "DASHED"},
                            {"latex": "(0,0)", "color": "#c87832", "pointStyle": "POINT", "pointSize": "12"},
                            {"latex": "(1,0)", "color": "#c87832", "pointStyle": "POINT", "pointSize": "12"},
                            {"latex": "(2,0)", "color": "#c87832", "pointStyle": "POINT", "pointSize": "12"},
                            {"latex": "(3,0)", "color": "#c87832", "pointStyle": "POINT", "pointSize": "12"},
                            {"latex": "(4,0)", "color": "#c87832", "pointStyle": "POINT", "pointSize": "12"},
                            {"latex": "(5,0)", "color": "#c87832", "pointStyle": "POINT", "pointSize": "12"}
                        ],
                        "bounds": {"left": -1, "right": 6, "bottom": -1, "top": 1},
                        "description": "数轴上的自然数点"
                    }
                },
                {
                    "title": "总结：从感知到抽象",
                    "content": "自然数的诞生经历了三个阶段：①感知「有/没有」→ ②建立「一一对应」→ ③抽象出「后继」概念。这就是第一性原理思维：从最基本的事实出发，一步步构建出复杂的数学体系。理解了这个过程，你就理解了数学的本质——它是人类从具体到抽象的思维工具。",
                    "formula": "感知 → 对应 → 抽象 → 公理化",
                    "hint": "数学不是凭空发明的，而是从现实中「长」出来的"
                }
            ]
        },
        "加法与减法": {
            "steps": [
                {
                    "title": "从合并需求开始",
                    "content": "你有3个苹果，朋友给你2个，一共有多少？这是人类最基本的数学需求：合并两组物品。加法就是为解决这个问题而生的运算。它的本质是「计数的延续」——从一个数开始，再数若干个。",
                    "formula": "3 + 2 = ?",
                    "hint": "加法是计数过程的自然延伸"
                },
                {
                    "title": "加法的几何意义",
                    "content": "在数轴上，3+2意味着从3出发，向右移动2个单位，到达5。这告诉我们：加法等价于数轴上的「向右移动」。向右移动越多，结果越大——这就是为什么加法让数变大。",
                    "formula": "3 →(右移2)→ 5",
                    "hint": "加法 = 向右移动",
                    "graph": {
                        "expressions": [
                            {"latex": "y=0", "color": "#888888", "lineStyle": "DASHED"},
                            {"latex": "(3,0)", "color": "#1a6a6a", "pointStyle": "POINT", "pointSize": "12", "label": "起点3"},
                            {"latex": "(5,0)", "color": "#c87832", "pointStyle": "POINT", "pointSize": "12", "label": "终点5"},
                            {"latex": "y=0\\left\\{3\\le x\\le5\\right\\}", "color": "#c87832", "lineWidth": "3"}
                        ],
                        "bounds": {"left": -1, "right": 7, "bottom": -1, "top": 1},
                        "description": "数轴上3+2=5：从3向右移动2个单位到5"
                    }
                },
                {
                    "title": "减法：加法的逆运算",
                    "content": "如果加法是「合并」，减法就是「拿走」。你有5个苹果，拿走2个，还剩多少？在数轴上，5-2意味着从5出发，向左移动2个单位，到达3。减法是加法的逆运算：如果3+2=5，那么5-2=3。",
                    "formula": "5 →(左移2)→ 3",
                    "hint": "减法 = 向左移动",
                    "graph": {
                        "expressions": [
                            {"latex": "y=0", "color": "#888888", "lineStyle": "DASHED"},
                            {"latex": "(5,0)", "color": "#b84040", "pointStyle": "POINT", "pointSize": "12", "label": "起点5"},
                            {"latex": "(3,0)", "color": "#2a7a4a", "pointStyle": "POINT", "pointSize": "12", "label": "终点3"},
                            {"latex": "y=0\\left\\{3\\le x\\le5\\right\\}", "color": "#b84040", "lineWidth": "3"}
                        ],
                        "bounds": {"left": -1, "right": 7, "bottom": -1, "top": 1},
                        "description": "数轴上5-2=3：从5向左移动2个单位到3"
                    }
                },
                {
                    "title": "从自然数到整数",
                    "content": "当你用小的数减大的数（如3-5），在自然数范围内无解。但现实中，欠债2元就是-2。引入负数后，减法永远有解。整数集 {..., -2, -1, 0, 1, 2, ...} 就这样诞生了。",
                    "formula": "3 - 5 = -2",
                    "hint": "负数的发明让减法变得「完美」",
                    "graph": {
                        "expressions": [
                            {"latex": "y=0", "color": "#888888", "lineStyle": "DASHED"},
                            {"latex": "(-3,0)", "color": "#b84040", "pointStyle": "POINT", "pointSize": "10", "label": "-3"},
                            {"latex": "(-2,0)", "color": "#b84040", "pointStyle": "POINT", "pointSize": "10", "label": "-2"},
                            {"latex": "(-1,0)", "color": "#b84040", "pointStyle": "POINT", "pointSize": "10", "label": "-1"},
                            {"latex": "(0,0)", "color": "#1a6a6a", "pointStyle": "POINT", "pointSize": "12", "label": "0"},
                            {"latex": "(1,0)", "color": "#2a7a4a", "pointStyle": "POINT", "pointSize": "10", "label": "1"},
                            {"latex": "(2,0)", "color": "#2a7a4a", "pointStyle": "POINT", "pointSize": "10", "label": "2"},
                            {"latex": "(3,0)", "color": "#2a7a4a", "pointStyle": "POINT", "pointSize": "10", "label": "3"}
                        ],
                        "bounds": {"left": -4, "right": 4, "bottom": -1, "top": 1},
                        "description": "整数数轴：负数在0左边，正数在0右边"
                    }
                },
                {
                    "title": "运算律：加法的本质属性",
                    "content": "加法满足三个重要定律：①交换律：3+5=5+3（先数谁无所谓）②结合律：(2+3)+4=2+(3+4)（分组方式不影响结果）③零元：a+0=a（加什么都不变）。这些不是人为规定的，而是从计数的本质自然导出的。",
                    "formula": "a+b=b+a, (a+b)+c=a+(b+c), a+0=a",
                    "hint": "运算律是数学的「游戏规则」"
                },
                {
                    "title": "数形结合：温度计模型",
                    "content": "温度计是理解正负数加减法的最佳模型：零上5度加3度等于零上8度（5+3=8），零上2度减5度等于零下3度（2-5=-3）。温度计就是竖着的数轴，上升是加，下降是减。",
                    "formula": "↑ 加法（上升），↓ 减法（下降）",
                    "hint": "温度计是活生生的数轴",
                    "graph": {
                        "expressions": [
                            {"latex": "x=0", "color": "#888888", "lineStyle": "DASHED"},
                            {"latex": "(0,-5)", "color": "#b84040", "pointStyle": "POINT", "pointSize": "10", "label": "-5°"},
                            {"latex": "(0,0)", "color": "#1a6a6a", "pointStyle": "POINT", "pointSize": "12", "label": "0°"},
                            {"latex": "(0,5)", "color": "#2a7a4a", "pointStyle": "POINT", "pointSize": "10", "label": "5°"},
                            {"latex": "(0,8)", "color": "#c87832", "pointStyle": "POINT", "pointSize": "10", "label": "8°"},
                            {"latex": "x=0\\left\\{-5\\le y\\le8\\right\\}", "color": "#c87832", "lineWidth": "4"}
                        ],
                        "bounds": {"left": -2, "right": 2, "bottom": -6, "top": 10},
                        "description": "竖直数轴（温度计）：5+3=8"
                    }
                }
            ]
        },
        "一次函数": {
            "steps": [
                {
                    "title": "从「匀速变化」开始",
                    "content": "你以每小时5公里的速度走路，走了3小时，走了多少公里？答案是15公里。如果用t表示时间，s表示路程，那么s=5t。这就是最简单的一次函数：一个变量随另一个变量匀速变化。",
                    "formula": "s = 5t （路程 = 速度 × 时间）",
                    "hint": "一次函数描述「匀速变化」"
                },
                {
                    "title": "一般形式：y = kx + b",
                    "content": "一次函数的一般形式是y=kx+b。其中k是斜率（slope），表示变化的快慢；b是截距（intercept），表示起点。k>0时函数递增，k<0时递减，k=0时是常数。这就是直线的代数表达。",
                    "formula": "y = kx + b （k≠0）",
                    "hint": "斜率决定倾斜方向，截距决定高度",
                    "graph": {
                        "expressions": [
                            {"latex": "y=2x+1", "color": "#c87832"},
                            {"latex": "y=-x+3", "color": "#1a6a6a"},
                            {"latex": "y=0.5x-1", "color": "#2a7a4a"}
                        ],
                        "bounds": {"left": -5, "right": 5, "bottom": -5, "top": 8},
                        "description": "不同斜率和截距的直线"
                    }
                },
                {
                    "title": "斜率的几何意义",
                    "content": "在坐标系中，斜率k就是直线的「陡峭程度」。k=2意味着x每增加1，y增加2。k=-1意味着x每增加1，y减少1。斜率越大，直线越陡。斜率相同，直线平行。这就是「变化率」的可视化。",
                    "formula": "k = Δy/Δx = (y₂-y₁)/(x₂-x₁)",
                    "hint": "斜率 = 变化的速率",
                    "graph": {
                        "expressions": [
                            {"latex": "y=2x", "color": "#c87832", "label": "k=2 (陡)"},
                            {"latex": "y=x", "color": "#1a6a6a", "label": "k=1"},
                            {"latex": "y=0.5x", "color": "#2a7a4a", "label": "k=0.5 (缓)"},
                            {"latex": "y=-x", "color": "#b84040", "label": "k=-1 (下降)"}
                        ],
                        "bounds": {"left": -5, "right": 5, "bottom": -5, "top": 5},
                        "description": "斜率k决定直线的倾斜程度和方向"
                    }
                },
                {
                    "title": "截距的物理意义",
                    "content": "当x=0时，y=b。截距就是函数的「起点」。比如出租车费：起步价10元（截距），每公里2元（斜率）。总费用y=2x+10。截距是「固定成本」，斜率是「变动成本」。",
                    "formula": "y = 2x + 10 （出租车费）",
                    "hint": "截距是x=0时y的值",
                    "graph": {
                        "expressions": [
                            {"latex": "y=2x+10", "color": "#c87832"},
                            {"latex": "(0,10)", "color": "#b84040", "pointStyle": "POINT", "pointSize": "12", "label": "截距b=10"},
                            {"latex": "y=10\\left\\{0\\le x\\le5\\right\\}", "color": "#888888", "lineStyle": "DASHED"}
                        ],
                        "bounds": {"left": -2, "right": 8, "bottom": -2, "top": 25},
                        "description": "出租车费 y=2x+10：截距10是起步价"
                    }
                },
                {
                    "title": "数形结合：直线图象",
                    "content": "一次函数的图象是一条直线。给定两个点，就能确定一条直线。画图步骤：①找两个x值，算出对应的y值 ②在坐标系中描点 ③用直线连接。直线向两端无限延伸——一次函数的定义域和值域都是全体实数。",
                    "formula": "两点确定一条直线",
                    "hint": "一次函数 = 直线",
                    "graph": {
                        "expressions": [
                            {"latex": "y=1.5x-1", "color": "#c87832"},
                            {"latex": "(0,-1)", "color": "#b84040", "pointStyle": "POINT", "pointSize": "10", "label": "(0,-1)"},
                            {"latex": "(2,2)", "color": "#b84040", "pointStyle": "POINT", "pointSize": "10", "label": "(2,2)"}
                        ],
                        "bounds": {"left": -3, "right": 5, "bottom": -4, "top": 6},
                        "description": "通过两点画直线：y=1.5x-1"
                    }
                },
                {
                    "title": "实际应用：线性建模",
                    "content": "很多现实问题可以用一次函数建模：①匀速运动 s=vt ②温度转换 F=1.8C+32 ③手机套餐费 y=ax+b。关键是识别「固定量」（截距）和「变化率」（斜率）。学会建模，就学会了用数学描述世界。",
                    "formula": "固定量 + 变化率 × 变量 = 结果",
                    "hint": "一次函数是数学建模的起点",
                    "graph": {
                        "expressions": [
                            {"latex": "y=1.8x+32", "color": "#c87832", "label": "F=1.8C+32"},
                            {"latex": "(0,32)", "color": "#b84040", "pointStyle": "POINT", "pointSize": "10", "label": "0°C=32°F"},
                            {"latex": "(10,50)", "color": "#2a7a4a", "pointStyle": "POINT", "pointSize": "10", "label": "10°C=50°F"}
                        ],
                        "bounds": {"left": -5, "right": 30, "bottom": 10, "top": 100},
                        "description": "温度转换：华氏度 vs 摄氏度"
                    }
                }
            ]
        },
        "二次函数": {
            "steps": [
                {
                    "title": "从「加速变化」开始",
                    "content": "一次函数描述匀速变化，但现实中很多变化是「加速」的。比如自由落体：物体下落的距离与时间的平方成正比。这就是二次函数的起源——描述「变化率本身也在变化」的现象。",
                    "formula": "s = ½gt² （自由落体）",
                    "hint": "二次函数描述「加速运动」"
                },
                {
                    "title": "一般形式：y = ax² + bx + c",
                    "content": "二次函数的一般形式是y=ax²+bx+c（a≠0）。其中a决定开口方向和大小，b影响对称轴位置，c是y轴截距。当a>0时开口向上（有最小值），a<0时开口向下（有最大值）。",
                    "formula": "y = ax² + bx + c （a≠0）",
                    "hint": "a的正负决定开口方向",
                    "graph": {
                        "expressions": [
                            {"latex": "y=x^2", "color": "#c87832", "label": "a=1 (开口向上)"},
                            {"latex": "y=-x^2", "color": "#b84040", "label": "a=-1 (开口向下)"},
                            {"latex": "y=2x^2", "color": "#1a6a6a", "label": "a=2 (更窄)"}
                        ],
                        "bounds": {"left": -4, "right": 4, "bottom": -5, "top": 8},
                        "description": "不同a值的抛物线"
                    }
                },
                {
                    "title": "抛物线：图象的形状",
                    "content": "二次函数的图象是抛物线（parabola）。它关于对称轴对称，顶点是最高点或最低点。对称轴公式 x=-b/(2a) 可以通过配方法推导。抛物线在自然界中随处可见：喷泉的水柱、投篮的轨迹、卫星天线的形状。",
                    "formula": "对称轴：x = -b/(2a)，顶点：(-b/2a, (4ac-b²)/4a)",
                    "hint": "抛物线是对称的「U形」曲线",
                    "graph": {
                        "expressions": [
                            {"latex": "y=x^2-4x+3", "color": "#c87832"},
                            {"latex": "x=2", "color": "#1a6a6a", "lineStyle": "DASHED", "label": "对称轴x=2"},
                            {"latex": "(2,-1)", "color": "#b84040", "pointStyle": "POINT", "pointSize": "12", "label": "顶点(2,-1)"},
                            {"latex": "(0,3)", "color": "#888888", "pointStyle": "POINT", "pointSize": "8", "label": "y截距"},
                            {"latex": "(1,0)", "color": "#888888", "pointStyle": "POINT", "pointSize": "8", "label": "x截距"},
                            {"latex": "(3,0)", "color": "#888888", "pointStyle": "POINT", "pointSize": "8", "label": "x截距"}
                        ],
                        "bounds": {"left": -1, "right": 5, "bottom": -3, "top": 6},
                        "description": "y=x²-4x+3的抛物线及关键点"
                    }
                },
                {
                    "title": "判别式：根的个数",
                    "content": "方程ax²+bx+c=0的解的个数由判别式Δ=b²-4ac决定：Δ>0有两个不等实根，Δ=0有两个相等实根，Δ<0无实根。判别式是「预判」方程解的工具，不需要真的去解方程。",
                    "formula": "Δ = b² - 4ac",
                    "hint": "判别式是方程解的「预告片」",
                    "graph": {
                        "expressions": [
                            {"latex": "y=x^2-4x+3", "color": "#2a7a4a", "label": "Δ>0 (两个根)"},
                            {"latex": "y=x^2-4x+4", "color": "#c87832", "label": "Δ=0 (一个根)"},
                            {"latex": "y=x^2-4x+5", "color": "#b84040", "label": "Δ<0 (无实根)"},
                            {"latex": "y=0", "color": "#888888", "lineStyle": "DASHED"}
                        ],
                        "bounds": {"left": -1, "right": 5, "bottom": -2, "top": 6},
                        "description": "判别式Δ决定抛物线与x轴的交点数"
                    }
                },
                {
                    "title": "顶点式：最值问题",
                    "content": "将y=ax²+bx+c配方为y=a(x-h)²+k的形式，其中(h,k)是顶点。这让我们能直接看出函数的最大值或最小值。很多优化问题（如最大利润、最小成本）都转化为求二次函数的顶点。",
                    "formula": "y = a(x-h)² + k",
                    "hint": "顶点式让最值一目了然",
                    "graph": {
                        "expressions": [
                            {"latex": "y=(x-2)^2-1", "color": "#c87832", "label": "顶点式"},
                            {"latex": "y=x^2-4x+3", "color": "#1a6a6a", "label": "一般式"},
                            {"latex": "(2,-1)", "color": "#b84040", "pointStyle": "POINT", "pointSize": "14", "label": "顶点(2,-1) 最小值=-1"}
                        ],
                        "bounds": {"left": -1, "right": 5, "bottom": -3, "top": 6},
                        "description": "顶点式与一般式表示同一条抛物线"
                    }
                },
                {
                    "title": "数形结合：抛物线应用",
                    "content": "抛物线有独特的光学性质：从焦点发出的光经抛物线反射后平行射出。这就是卫星天线、汽车前灯的工作原理。反过来，平行光入射会聚于焦点——太阳能灶就是这个原理。数学与物理的完美结合！",
                    "formula": "焦点性质：入射角 = 反射角",
                    "hint": "抛物线不只是数学，还是工程学的基础"
                }
            ]
        },
        "导数": {
            "steps": [
                {
                    "title": "从「瞬时速度」开始",
                    "content": "一辆车从A开到B，100公里用了2小时，平均速度是50km/h。但在某一瞬间，车速表显示的是60km/h。这个「瞬时速度」是怎么算出来的？平均速度是整体的，瞬时速度是局部的——这就是导数要解决的问题。",
                    "formula": "平均速度 = 路程/时间，瞬时速度 = ?",
                    "hint": "导数的起源是「瞬时变化率」"
                },
                {
                    "title": "极限：从平均到瞬时",
                    "content": "要算瞬时速度，我们取越来越短的时间间隔：Δt=1小时→0.1小时→0.01小时→...当Δt趋近于0时，平均速度的极限就是瞬时速度。这就是导数的定义：极限过程让「平均」变成了「瞬时」。",
                    "formula": "f'(x) = lim[Δx→0] (f(x+Δx) - f(x))/Δx",
                    "hint": "导数 = 极限下的平均变化率"
                },
                {
                    "title": "导数的几何意义：切线斜率",
                    "content": "在函数图象上，导数f'(x)就是该点切线的斜率。切线是「刚好碰到曲线」的直线，它反映了函数在该点的变化趋势。斜率为正，函数递增；斜率为负，函数递减；斜率为零，可能是极值点。",
                    "formula": "f'(x) > 0 → 递增，f'(x) < 0 → 递减",
                    "hint": "导数是函数的「趋势指示器」",
                    "graph": {
                        "expressions": [
                            {"latex": "y=x^2", "color": "#c87832"},
                            {"latex": "y=2x-1", "color": "#1a6a6a", "label": "x=1处的切线"},
                            {"latex": "(1,1)", "color": "#b84040", "pointStyle": "POINT", "pointSize": "12", "label": "切点(1,1)"},
                            {"latex": "y=0", "color": "#888888", "lineStyle": "DASHED"}
                        ],
                        "bounds": {"left": -2, "right": 4, "bottom": -2, "top": 8},
                        "description": "y=x²在x=1处的切线：斜率=2"
                    }
                },
                {
                    "title": "求导法则：从定义到公式",
                    "content": "用极限定义求导太麻烦，数学家总结了求导法则：①(xⁿ)' = nxⁿ⁻¹（幂法则）②(sinx)' = cosx（三角函数）③(eˣ)' = eˣ（指数函数）④(fg)' = f'g + fg'（乘法法则）。掌握这些法则，就能快速求导。",
                    "formula": "(xⁿ)' = nxⁿ⁻¹, (sinx)' = cosx, (eˣ)' = eˣ",
                    "hint": "求导法则是「计算捷径」",
                    "graph": {
                        "expressions": [
                            {"latex": "y=x^2", "color": "#c87832", "label": "原函数 y=x²"},
                            {"latex": "y=2x", "color": "#1a6a6a", "label": "导函数 y'=2x"},
                            {"latex": "y=0", "color": "#888888", "lineStyle": "DASHED"}
                        ],
                        "bounds": {"left": -4, "right": 4, "bottom": -4, "top": 8},
                        "description": "原函数y=x²与导函数y'=2x"
                    }
                },
                {
                    "title": "导数的应用：最优化",
                    "content": "导数最强大的应用是求最值。当f'(x)=0时，x可能是极大值或极小值。判断方法：看f''(x)的符号。实际应用：①求最大利润 ②求最小成本 ③求最佳设计参数。这就是微积分改变世界的方式。",
                    "formula": "f'(x)=0 → 极值点",
                    "hint": "导数是优化问题的「金钥匙」",
                    "graph": {
                        "expressions": [
                            {"latex": "y=x^3-3x", "color": "#c87832"},
                            {"latex": "y=3x^2-3", "color": "#1a6a6a", "label": "导函数"},
                            {"latex": "(-1,2)", "color": "#2a7a4a", "pointStyle": "POINT", "pointSize": "12", "label": "极大值"},
                            {"latex": "(1,-2)", "color": "#b84040", "pointStyle": "POINT", "pointSize": "12", "label": "极小值"},
                            {"latex": "y=0", "color": "#888888", "lineStyle": "DASHED"}
                        ],
                        "bounds": {"left": -3, "right": 3, "bottom": -5, "top": 5},
                        "description": "原函数与导函数：导数为0的点是极值点"
                    }
                },
                {
                    "title": "数形结合：导数图象",
                    "content": "原函数f(x)的图象是曲线，导函数f'(x)的图象反映曲线的「陡峭程度」。f(x)递增时f'(x)>0（图象在x轴上方），f(x)递减时f'(x)<0（图象在x轴下方）。两个图象对照看，理解更深刻。",
                    "formula": "f(x)↗ → f'(x)>0, f(x)↘ → f'(x)<0",
                    "hint": "原函数和导函数是「一对」"
                }
            ]
        },
        "积分": {
            "steps": [
                {
                    "title": "从「求面积」开始",
                    "content": "如何计算不规则图形的面积？矩形可以用长×宽，但曲线围成的面积怎么办？积分就是为解决这个问题而生的。它的思想是：把不规则图形切成无数个细长条，每个近似为矩形，再求和。",
                    "formula": "面积 ≈ Σ(小矩形面积)",
                    "hint": "积分的本质是「化整为零，积零为整」"
                },
                {
                    "title": "定积分：极限下的求和",
                    "content": "把区间[a,b]分成n等份，每份宽度Δx=(b-a)/n。当n→∞时，这些小矩形面积之和的极限就是定积分∫ₐᵇf(x)dx。这就是黎曼和（Riemann Sum）的思想：用无限多个无限小的矩形精确计算面积。",
                    "formula": "∫ₐᵇf(x)dx = lim[n→∞] Σf(xᵢ)Δx",
                    "hint": "定积分 = 曲线下面积",
                    "graph": {
                        "expressions": [
                            {"latex": "y=x^2/4", "color": "#c87832"},
                            {"latex": "y=0\\left\\{0\\le x\\le4\\right\\}", "color": "#888888", "lineStyle": "DASHED"},
                            {"latex": "x=0", "color": "#888888", "lineStyle": "DASHED"},
                            {"latex": "x=4", "color": "#888888", "lineStyle": "DASHED"}
                        ],
                        "bounds": {"left": -1, "right": 5, "bottom": -1, "top": 5},
                        "description": "定积分∫₀⁴(x²/4)dx表示曲线下的面积"
                    }
                },
                {
                    "title": "不定积分：导数的逆运算",
                    "content": "如果导数是「求变化率」，不定积分就是「从变化率恢复原函数」。已知速度函数v(t)，积分得到位移函数s(t)。不定积分∫f(x)dx = F(x) + C，其中F'(x)=f(x)，C是任意常数。",
                    "formula": "∫f(x)dx = F(x) + C, 其中 F'(x) = f(x)",
                    "hint": "积分是导数的「逆操作」"
                },
                {
                    "title": "牛顿-莱布尼茨公式",
                    "content": "微积分基本定理告诉我们：∫ₐᵇf(x)dx = F(b) - F(a)。这个公式把「求面积」这个几何问题转化为「求原函数」这个代数问题。它连接了微分和积分，是整个微积分的核心。",
                    "formula": "∫ₐᵇf(x)dx = F(b) - F(a)",
                    "hint": "这是微积分最伟大的公式之一"
                },
                {
                    "title": "积分的应用",
                    "content": "积分的应用极其广泛：①求面积和体积 ②求变力做功 ③求概率（概率密度函数的积分）④求函数平均值 ⑤求弧长。物理学中，位移是速度的积分，功是力的积分，热量是功率的积分。",
                    "formula": "W = ∫F·ds, P = ∫f(x)dx",
                    "hint": "积分是「累积」的数学表达",
                    "graph": {
                        "expressions": [
                            {"latex": "y=\\sin(x)", "color": "#c87832"},
                            {"latex": "y=0\\left\\{0\\le x\\le\\pi\\right\\}", "color": "#888888", "lineStyle": "DASHED"},
                            {"latex": "x=0", "color": "#888888", "lineStyle": "DASHED"},
                            {"latex": "x=\\pi", "color": "#888888", "lineStyle": "DASHED"}
                        ],
                        "bounds": {"left": -0.5, "right": 4, "bottom": -0.5, "top": 1.5},
                        "description": "∫₀^π sin(x)dx = 2（正弦曲线下的面积）"
                    }
                },
                {
                    "title": "数形结合：积分可视化",
                    "content": "在图象上，定积分就是曲线y=f(x)与x轴之间的面积。x轴上方的面积为正，下方为负。这就是为什么「面积」可以是负数——它实际上是「有向面积」。理解这一点，就理解了积分的几何本质。",
                    "formula": "∫f(x)dx = 上方面积 - 下方面积",
                    "hint": "积分面积有正负之分"
                }
            ]
        },
        "极限": {
            "steps": [
                {
                    "title": "从「无限逼近」开始",
                    "content": "一个数列：1, 1/2, 1/4, 1/8, ... 每次减半，越来越接近0，但永远不等于0。极限就是描述这种「无限逼近但不一定到达」的概念。极限不是数列的最后一项，而是它的「趋势」。",
                    "formula": "lim[n→∞] 1/2ⁿ = 0",
                    "hint": "极限是「趋势」，不是「终点」",
                    "graph": {
                        "expressions": [
                            {"latex": "y=1/2^x", "color": "#c87832"},
                            {"latex": "y=0", "color": "#1a6a6a", "lineStyle": "DASHED", "label": "极限y=0"},
                            {"latex": "(0,1)", "color": "#b84040", "pointStyle": "POINT", "pointSize": "10", "label": "1"},
                            {"latex": "(1,0.5)", "color": "#b84040", "pointStyle": "POINT", "pointSize": "10", "label": "1/2"},
                            {"latex": "(2,0.25)", "color": "#b84040", "pointStyle": "POINT", "pointSize": "10", "label": "1/4"},
                            {"latex": "(3,0.125)", "color": "#b84040", "pointStyle": "POINT", "pointSize": "10", "label": "1/8"}
                        ],
                        "bounds": {"left": -1, "right": 8, "bottom": -0.2, "top": 1.2},
                        "description": "数列1/2ⁿ无限逼近0"
                    }
                },
                {
                    "title": "ε-δ语言：严格定义",
                    "content": "如何严格说「无限逼近」？数学家用ε-δ语言：对任意小的ε>0，存在δ>0，当0<|x-a|<δ时，|f(x)-L|<ε。意思是：只要x足够接近a，f(x)就能任意接近L。这就是极限的严格定义。",
                    "formula": "lim[x→a] f(x) = L ⟺ ∀ε>0, ∃δ>0: 0<|x-a|<δ → |f(x)-L|<ε",
                    "hint": "ε-δ语言让「无限」变得精确"
                },
                {
                    "title": "极限运算法则",
                    "content": "极限可以「分配」到四则运算中：lim(f+g) = limf + limg，lim(f×g) = limf × limg。这让我们能通过已知极限推导复杂极限。但要注意：只有当各部分极限存在时才能这样分配。",
                    "formula": "lim(f±g) = limf ± limg, lim(fg) = limf · limg",
                    "hint": "极限运算像「拆括号」"
                },
                {
                    "title": "两个重要极限",
                    "content": "两个极限必须记住：①lim[x→0] sinx/x = 1（这是导出三角函数导数的基础）②lim[n→∞] (1+1/n)ⁿ = e ≈ 2.718（自然对数的底数，描述连续增长）。这两个极限是微积分的「基石」。",
                    "formula": "lim[x→0] sinx/x = 1, lim[n→∞] (1+1/n)ⁿ = e",
                    "hint": "这两个极限是微积分的「钥匙」",
                    "graph": {
                        "expressions": [
                            {"latex": "y=\\sin(x)/x", "color": "#c87832"},
                            {"latex": "y=1", "color": "#1a6a6a", "lineStyle": "DASHED", "label": "极限值1"},
                            {"latex": "(0,1)", "color": "#b84040", "pointStyle": "POINT", "pointSize": "12", "label": "空心点"}
                        ],
                        "bounds": {"left": -8, "right": 8, "bottom": -0.3, "top": 1.3},
                        "description": "lim[x→0] sinx/x = 1"
                    }
                },
                {
                    "title": "连续性：极限的特殊情况",
                    "content": "如果lim[x→a] f(x) = f(a)，则函数在a点连续。连续意味着：在a点附近，函数值没有「跳跃」。连续函数的图象可以一笔画出来。所有初等函数在其定义域内都是连续的。",
                    "formula": "连续 ⟺ lim[x→a] f(x) = f(a)",
                    "hint": "连续 = 没有断裂",
                    "graph": {
                        "expressions": [
                            {"latex": "y=x^2", "color": "#2a7a4a", "label": "连续"},
                            {"latex": "y=\\operatorname{floor}(x)", "color": "#b84040", "label": "不连续"}
                        ],
                        "bounds": {"left": -2, "right": 5, "bottom": -1, "top": 6},
                        "description": "连续函数（可一笔画）vs 不连续函数（有断裂）"
                    }
                },
                {
                    "title": "极限的意义：从有限到无限",
                    "content": "极限让我们能用「有限」的步骤处理「无限」的过程。它是微积分的基石：导数是极限（Δx→0），积分是极限（n→∞）。理解极限，就理解了微积分的「灵魂」。",
                    "formula": "微积分 = 极限的应用",
                    "hint": "极限是连接有限与无限的「桥梁」"
                }
            ]
        },
    }

    # 查找匹配的主题
    for key, derivation in derivations.items():
        if key in topic_title or topic_title in key:
            return json.dumps(derivation, ensure_ascii=False)

    # 通用回退内容
    return json.dumps({
        "steps": [
            {
                "title": f"从第一性原理理解「{topic_title}」",
                "content": f"每个数学概念都有其最基本的出发点。「{topic_title}」也不例外。要真正理解它，我们需要从最原始的问题或需求出发，一步步推导出它的定义、性质和应用。这不仅是学习数学的方法，更是理解任何复杂系统的通用思维框架。",
                "hint": "第一性原理思维：从最基本的事实出发"
            },
            {
                "title": "核心概念的诞生",
                "content": f"「{topic_title}」的诞生是为了解决某个具体问题。在数学发展的历史长河中，数学家们面对实际问题，创造了新的概念和工具。理解这个「为什么」比记住「是什么」更重要。当我们知道了一个概念的来龙去脉，它就不再是冰冷的公式，而是活生生的思想。",
                "formula": "问题 → 概念 → 定义 → 性质 → 应用",
                "hint": "理解「为什么」比记住「是什么」更重要"
            },
            {
                "title": "数形结合：可视化理解",
                "content": f"数形结合是理解「{topic_title}」的重要方法。代数表达式告诉我们「是什么」，几何图形告诉我们「为什么」。当我们能把抽象的公式转化为直观的图形，理解就会变得深刻而持久。尝试画图、动手操作，让数学变得可见。",
                "hint": "代数是「计算」，几何是「直觉」"
            },
            {
                "title": "从特殊到一般",
                "content": f"学习「{topic_title}」的最佳路径是：先看具体例子，再总结一般规律。比如学二次函数，先研究y=x²的具体图象，再推广到y=ax²+bx+c的一般形式。这种从特殊到一般的思维方式，是数学研究的核心方法。",
                "formula": "特殊 → 观察 → 归纳 → 证明 → 一般",
                "hint": "例子是最好的老师"
            },
            {
                "title": "总结与展望",
                "content": f"「{topic_title}」不是孤立的知识点，而是数学大厦的一块砖。它与前后知识有着紧密的联系：前面的概念是它的基础，后面的发展是它的延伸。理解这种联系，就能建立完整的知识网络，而不是零散的记忆碎片。",
                "hint": "数学是一个整体，每个概念都相互关联"
            }
        ]
    }, ensure_ascii=False)


def get_prompt_hash(topic_id: str, extra: str = "") -> str:
    return hashlib.md5(f"{topic_id}:{extra}".encode()).hexdigest()
