"""种子数据 — 6 阶段 30 主题（从数学第一性原理学习系统.html 提取）"""
import json


STAGES = [
    {"name": "数的起源", "index": 0},
    {"name": "代数语言", "index": 1},
    {"name": "几何直觉", "index": 2},
    {"name": "函数世界", "index": 3},
    {"name": "变化的科学", "index": 4},
    {"name": "抽象与推理", "index": 5},
    {"name": "高等数学", "index": 6},
]

TOPICS = [
    # ── 数的起源 ──
    {
        "id": "t1", "stage": "数的起源", "stage_index": 0,
        "icon": "🔢", "title": "自然数与计数", "description": "从「一一对应」理解数的本质", "sort_order": 1,
        "lesson": [
            {"type": "title", "content": "从具体到抽象"},
            {"type": "text", "content": "人类最早学会的数学是「数数」——把具体物体和数建立一一对应关系。"},
            {"type": "highlight", "content": "1 个苹果对应 1，2 个苹果对应 2。这就是计数的本质：一一对应。"},
            {"type": "title", "content": "位值制——用少量符号表示任意大的数"},
            {"type": "text", "content": "我们用 0-9 十个符号，通过「位值」表示任意大的数。个位、十位、百位……每一位的权重是 10 的幂。"},
            {"type": "formula", "content": "123 = 1×100 + 2×10 + 3×1"},
            {"type": "ex", "content": "<b>例：</b>二进制只有 0 和 1，计算机用它表示一切。2¹⁰ = 1024 ≈ 10³。"}
        ],
        "quiz": [
            {"question": "自然数的起点是？", "options": ["0", "1", "-1", "任意数"], "answer": 0, "explanation": "现代数学定义自然数从 0 开始（N = {0,1,2,3,...}）。"},
            {"question": "345 中的「4」代表什么？", "options": ["4", "40", "400", "4000"], "answer": 1, "explanation": "十位上的 4 代表 4×10 = 40。"},
            {"question": "二进制 101 等于十进制多少？", "options": ["2", "3", "5", "6"], "answer": 2, "explanation": "101₂ = 1×4 + 0×2 + 1×1 = 5。"}
        ]
    },
    {
        "id": "t2", "stage": "数的起源", "stage_index": 0,
        "icon": "➕", "title": "加法与乘法", "description": "运算的本质是「合并」与「重复」", "sort_order": 2,
        "lesson": [
            {"type": "title", "content": "加法——合并两个量"},
            {"type": "text", "content": "加法是最基本的运算：把两个量合并成一个量。"},
            {"type": "formula", "content": "3 + 5 = 8"},
            {"type": "ex", "content": "<b>交换律：</b>a + b = b + a（顺序不影响结果）\n<b>结合律：</b>(a + b) + c = a + (b + c)（分组不影响结果）"},
            {"type": "title", "content": "乘法——重复的加法"},
            {"type": "text", "content": "乘法是加法的简写：3×5 = 5+5+5 = 15。"},
            {"type": "formula", "content": "a × (b + c) = a×b + a×c（分配律）"},
            {"type": "ex", "content": "<b>例：</b>12 × 5 = 12 × (10/2) = 120/2 = 60。分配律让心算变简单。"}
        ],
        "quiz": [
            {"question": "7 + 3 = 3 + 7 体现了什么律？", "options": ["结合律", "交换律", "分配律", "消去律"], "answer": 1, "explanation": "交换律：改变运算顺序，结果不变。"},
            {"question": "4 × 6 表示什么？", "options": ["4+6", "6个4相加", "4个6相加", "4×6"], "answer": 1, "explanation": "4×6 = 6+6+6+6 = 24。乘法是重复加法。"},
            {"question": "3 × (4+5) = ?", "options": ["7", "12", "15", "27"], "answer": 3, "explanation": "分配律：3×(4+5) = 3×4 + 3×5 = 12+15 = 27。"}
        ]
    },
    {
        "id": "t3", "stage": "数的起源", "stage_index": 0,
        "icon": "➖", "title": "减法与除法", "description": "逆运算——知道结果求原因", "sort_order": 3,
        "lesson": [
            {"type": "title", "content": "减法——加法的逆运算"},
            {"type": "text", "content": "减法回答的问题是：「加上多少能变成目标？」"},
            {"type": "formula", "content": "8 - 3 = ? 等价于 ? + 3 = 8"},
            {"type": "title", "content": "除法——乘法的逆运算"},
            {"type": "text", "content": "除法回答的问题是：「分成几份？」或「包含几个？」"},
            {"type": "formula", "content": "20 ÷ 4 = 5 等价于 5 × 4 = 20"},
            {"type": "highlight", "content": "「分」除法：20 个苹果分给 4 人，每人几个？→ 5\n「包含」除法：20 个苹果，每袋装 4 个，能装几袋？→ 5"},
            {"type": "ex", "content": "<b>为什么不能除以 0？</b>如果 6 ÷ 0 = x，则 x × 0 = 6。但任何数乘 0 都等于 0，不可能等于 6。矛盾！"}
        ],
        "quiz": [
            {"question": "12 - ? = 5，求 ?", "options": ["5", "6", "7", "8"], "answer": 2, "explanation": "12 - 7 = 5，所以 ? = 7。"},
            {"question": "0 ÷ 5 = ?", "options": ["0", "5", "无意义", "1"], "answer": 0, "explanation": "0 个苹果分给 5 人，每人 0 个。0 可以做被除数。"},
            {"question": "除以 0 为什么无意义？", "options": ["因为太小了", "因为找不到答案", "因为会得到无穷大", "因为计算机不支持"], "answer": 1, "explanation": "找不到一个数 x 使得 x×0 = 非零数。"}
        ]
    },
    {
        "id": "t4", "stage": "数的起源", "stage_index": 0,
        "icon": "🔢", "title": "分数", "description": "除法的另一种写法", "sort_order": 4,
        "lesson": [
            {"type": "title", "content": "分数的含义"},
            {"type": "text", "content": "分数 a/b 表示「把 1 平均分成 b 份，取 a 份」。"},
            {"type": "formula", "content": "3/4 表示把 1 分成 4 份，取 3 份"},
            {"type": "title", "content": "等价分数"},
            {"type": "text", "content": "分子分母同乘一个非零数，分数值不变。"},
            {"type": "formula", "content": "2/4 = 1/2 = 50/100"},
            {"type": "ex", "content": "<b>约分：</b>分子分母同除以最大公因数。12/18 = 2/3（同除 6）"},
            {"type": "title", "content": "分数运算"},
            {"type": "text", "content": "加减法需要通分，乘法直接乘。"},
            {"type": "formula", "content": "1/2 + 1/3 = 3/6 + 2/6 = 5/6"},
            {"type": "formula", "content": "2/3 × 3/4 = 6/12 = 1/2"},
            {"type": "ex", "content": "<b>除法：</b>除以一个分数 = 乘以它的倒数。3/4 ÷ 2/5 = 3/4 × 5/2 = 15/8"}
        ],
        "quiz": [
            {"question": "3/5 的含义是？", "options": ["3 除以 5", "把 3 平均分成 5 份", "把 1 平均分成 5 份，取 3 份", "5 除以 3"], "answer": 2, "explanation": "分数 a/b：把 1 分成 b 份取 a 份。"},
            {"question": "2/3 + 1/6 = ?", "options": ["3/9", "5/6", "1/2", "3/6"], "answer": 1, "explanation": "通分：4/6 + 1/6 = 5/6。"},
            {"question": "3/4 ÷ 1/2 = ?", "options": ["3/8", "3/2", "6/4", "2/3"], "answer": 1, "explanation": "除以 1/2 = 乘以 2/1，3/4 × 2 = 6/4 = 3/2。"}
        ]
    },
    {
        "id": "t5", "stage": "数的起源", "stage_index": 0,
        "icon": "📊", "title": "小数与百分数", "description": "分数的十进制表示", "sort_order": 5,
        "lesson": [
            {"type": "title", "content": "小数——分数的另一种写法"},
            {"type": "text", "content": "小数是分母为 10、100、1000… 的分数。"},
            {"type": "formula", "content": "0.5 = 5/10 = 1/2"},
            {"type": "formula", "content": "0.75 = 75/100 = 3/4"},
            {"type": "formula", "content": "0.333... = 1/3（无限循环小数）"},
            {"type": "title", "content": "百分数——分母为 100 的分数"},
            {"type": "text", "content": "百分数用 % 表示，方便比较大小。"},
            {"type": "formula", "content": "25% = 25/100 = 1/4 = 0.25"},
            {"type": "ex", "content": "<b>例：</b>打八折 = 80% = 0.8。原价 100 元，折后 100 × 0.8 = 80 元。"}
        ],
        "quiz": [
            {"question": "0.36 = ?%", "options": ["3.6%", "36%", "0.36%", "360%"], "answer": 1, "explanation": "0.36 = 36/100 = 36%。"},
            {"question": "3/8 写成小数是？", "options": ["0.38", "0.375", "0.333", "0.8"], "answer": 1, "explanation": "3 ÷ 8 = 0.375。"},
            {"question": "打七折是什么意思？", "options": ["原价的 7%", "原价的 70%", "原价的 30%", "减 7 元"], "answer": 1, "explanation": "打七折 = 70% = 0.7。"}
        ]
    },
    # ── 代数语言 ──
    {
        "id": "t6", "stage": "代数语言", "stage_index": 1,
        "icon": "➖", "title": "负数", "description": "数轴的另一半——方向", "sort_order": 6,
        "lesson": [
            {"type": "title", "content": "负数的产生"},
            {"type": "text", "content": "减法可能产生「不够减」的情况，于是引入负数。"},
            {"type": "formula", "content": "3 - 5 = -2"},
            {"type": "highlight", "content": "负数表示「相反方向」的量：温度零下、海拔低于海平面、欠债"},
            {"type": "title", "content": "数轴"},
            {"type": "text", "content": "数轴是数的「地图」：原点、正方向、单位长度。"},
            {"type": "highlight", "content": "左边的数 < 右边的数。-3 < -1 < 0 < 2 < 5"},
            {"type": "title", "content": "绝对值"},
            {"type": "text", "content": "绝对值是数到原点的距离，总是非负。"},
            {"type": "formula", "content": "|5| = 5，|-5| = 5，|0| = 0"}
        ],
        "quiz": [
            {"question": "-3 比 -5 大还是小？", "options": ["小", "大", "一样大", "无法比较"], "answer": 1, "explanation": "在数轴上 -3 在 -5 右边，所以 -3 > -5。"},
            {"question": "|-7| = ?", "options": ["7", "-7", "0", "14"], "answer": 0, "explanation": "绝对值是到原点的距离，|-7| = 7。"},
            {"question": "0 - (-3) = ?", "options": ["-3", "0", "3", "6"], "answer": 2, "explanation": "减去负数等于加上正数：0 - (-3) = 0 + 3 = 3。"}
        ]
    },
    {
        "id": "t7", "stage": "代数语言", "stage_index": 1,
        "icon": "📝", "title": "整式与多项式", "description": "用字母表示数", "sort_order": 7,
        "lesson": [
            {"type": "title", "content": "为什么要用字母"},
            {"type": "text", "content": "用字母可以写「通用公式」，一个式子描述无穷多种情况。"},
            {"type": "formula", "content": "面积 = 长 × 宽 → S = a × b"},
            {"type": "highlight", "content": "字母代表「变量」（可以变化的量）和「常量」（不变的量）"},
            {"type": "title", "content": "单项式与多项式"},
            {"type": "text", "content": "单项式：数字和字母的乘积。多项式：多个单项式的和。"},
            {"type": "formula", "content": "3x² 是单项式（系数 3，次数 2）"},
            {"type": "formula", "content": "2x + 3y - 5 是多项式（三项式）"},
            {"type": "highlight", "content": "合并同类项：3x + 5x = 8x，但 3x + 5y 不能合并"},
            {"type": "ex", "content": "<b>例：</b>化简 2(x+3) - 4(x-1)\n= 2x + 6 - 4x + 4\n= -2x + 10"}
        ],
        "quiz": [
            {"question": "3x² 的系数是？", "options": ["3", "x", "2", "6"], "answer": 0, "explanation": "系数是字母前面的数字，即 3。"},
            {"question": "2x + 3x = ?", "options": ["5x", "6x", "5x²", "x"], "answer": 0, "explanation": "同类项相加：2x + 3x = 5x。"},
            {"question": "化简 3(a+2) = ?", "options": ["3a+2", "3a+6", "a+6", "3a+5"], "answer": 1, "explanation": "分配律：3×a + 3×2 = 3a + 6。"}
        ]
    },
    {
        "id": "t8", "stage": "代数语言", "stage_index": 1,
        "icon": "❓", "title": "一元一次方程", "description": "求未知数——等式的性质", "sort_order": 8,
        "lesson": [
            {"type": "title", "content": "方程是什么"},
            {"type": "text", "content": "方程是含有未知数的等式。解方程就是找出使等式成立的未知数的值。"},
            {"type": "formula", "content": "2x + 3 = 7 → 解为 x = 2"},
            {"type": "title", "content": "等式的基本性质"},
            {"type": "text", "content": "等式两边同时做相同操作，等式仍然成立。"},
            {"type": "highlight", "content": "① 两边同加（减）同一个数\n② 两边同乘（除）同一个非零数"},
            {"type": "ex", "content": "<b>例：</b>2x + 3 = 7\n两边减 3：2x = 4\n两边除以 2：x = 2"},
            {"type": "title", "content": "解题步骤"},
            {"type": "text", "content": "移项 → 合并同类项 → 系数化为1。"},
            {"type": "ex", "content": "<b>例：</b>5x - 7 = 3x + 5\n移项：5x - 3x = 5 + 7\n合并：2x = 12\n解：x = 6"}
        ],
        "quiz": [
            {"question": "x + 5 = 12 的解是？", "options": ["5", "6", "7", "17"], "answer": 2, "explanation": "两边减 5：x = 12 - 5 = 7。"},
            {"question": "3x = 15 的解是？", "options": ["3", "5", "12", "45"], "answer": 1, "explanation": "两边除以 3：x = 15/3 = 5。"},
            {"question": "2x + 1 = x - 3 的解是？", "options": ["4", "-4", "2", "-2"], "answer": 1, "explanation": "移项：2x - x = -3 - 1，x = -4。"}
        ]
    },
    {
        "id": "t9", "stage": "代数语言", "stage_index": 1,
        "icon": "⚖️", "title": "不等式", "description": "比较大小的学问", "sort_order": 9,
        "lesson": [
            {"type": "title", "content": "不等式的性质"},
            {"type": "text", "content": "不等式和等式类似，但有一个关键区别：乘以负数要变号。"},
            {"type": "highlight", "content": "① 两边同加（减）：方向不变\n② 两边同乘（除）正数：方向不变\n③ 两边同乘（除）负数：方向反转"},
            {"type": "formula", "content": "3 > 1，两边乘 -1 得 -3 < -1"},
            {"type": "ex", "content": "<b>例：</b>解 -2x + 3 > 7\n移项：-2x > 4\n除以 -2（变号）：x < -2"}
        ],
        "quiz": [
            {"question": "x - 3 > 2 的解集是？", "options": ["x > 5", "x > 1", "x < 5", "x < 1"], "answer": 0, "explanation": "两边加 3：x > 5。"},
            {"question": "-3x < 9 的解集是？", "options": ["x < -3", "x > -3", "x < 3", "x > 3"], "answer": 1, "explanation": "除以 -3 要变号：x > -3。"},
            {"question": "不等式两边乘以负数会？", "options": ["不变号", "变号", "等式不成立", "无意义"], "answer": 1, "explanation": "乘以负数，不等号方向反转。"}
        ]
    },
    {
        "id": "t10", "stage": "代数语言", "stage_index": 1,
        "icon": "🔀", "title": "方程组", "description": "多个未知数——消元法", "sort_order": 10,
        "lesson": [
            {"type": "title", "content": "什么是方程组"},
            {"type": "text", "content": "两个（或多个）方程联立，求同时满足所有方程的解。"},
            {"type": "formula", "content": "2x + y = 5\nx - y = 1"},
            {"type": "title", "content": "消元法"},
            {"type": "text", "content": "把两个方程相加或相减，消去一个未知数。"},
            {"type": "ex", "content": "<b>例：</b>解 {2x + y = 5 ①\n       {x - y = 1 ②\n①+②：3x = 6 → x = 2\n代入②：2 - y = 1 → y = 1"},
            {"type": "title", "content": "验证"},
            {"type": "text", "content": "把解代回原方程检验。"},
            {"type": "ex", "content": "2×2 + 1 = 5 ✓，2 - 1 = 1 ✓"}
        ],
        "quiz": [
            {"question": "方程组 {x+y=5, x-y=1} 的 x = ?", "options": ["1", "2", "3", "4"], "answer": 2, "explanation": "两式相加：2x = 6，x = 3。"},
            {"question": "消元法的核心思想是？", "options": ["代入", "把两个方程相加减消去一个未知数", "画图", "猜测"], "answer": 1, "explanation": "通过加减消去一个未知数，化为一元一次方程。"},
            {"question": "方程组 {2x+y=7, x=3} 的解是？", "options": ["x=3,y=1", "x=3,y=2", "x=3,y=3", "x=3,y=7"], "answer": 0, "explanation": "x=3 代入第一式：6+y=7，y=1。"}
        ]
    },
    # ── 几何直觉 ──
    {
        "id": "t11", "stage": "几何直觉", "stage_index": 2,
        "icon": "📍", "title": "点线面", "description": "空间的基本构件", "sort_order": 11,
        "lesson": [
            {"type": "title", "content": "点——没有大小的位置"},
            {"type": "text", "content": "点只有位置，没有面积。用大写字母表示，如点 A。"},
            {"type": "highlight", "content": "线段有两个端点，射线有一个端点，直线没有端点"},
            {"type": "title", "content": "线——点的轨迹"},
            {"type": "text", "content": "两点确定一条直线。平行线永不相交，相交线有一个交点。"},
            {"type": "formula", "content": "两点之间的距离：d = √[(x₂-x₁)² + (y₂-y₁)²]"},
            {"type": "title", "content": "面——线的轨迹"},
            {"type": "text", "content": "平面是无限延伸的平坦面。平面图形有面积。"},
            {"type": "highlight", "content": "三角形是最简单的多边形（3条边）"}
        ],
        "quiz": [
            {"question": "两点确定几条直线？", "options": ["0", "1", "2", "无数条"], "answer": 1, "explanation": "过两点有且只有一条直线。"},
            {"question": "平行线的定义是？", "options": ["不相交的线", "在同一平面内不相交的两条直线", "垂直的线", "一样长的线"], "answer": 1, "explanation": "关键：在同一平面内，不相交的两条直线。"},
            {"question": "三角形有几条边？", "options": ["2", "3", "4", "5"], "answer": 1, "explanation": "三角形 = 三条边 + 三个角。"}
        ]
    },
    {
        "id": "t12", "stage": "几何直觉", "stage_index": 2,
        "icon": "📏", "title": "角与平行", "description": "方向的度量", "sort_order": 12,
        "lesson": [
            {"type": "title", "content": "角的定义"},
            {"type": "text", "content": "角是由两条有公共端点的射线组成的图形。用度数度量。"},
            {"type": "formula", "content": "直角 = 90°，平角 = 180°，周角 = 360°"},
            {"type": "title", "content": "平行线的性质"},
            {"type": "text", "content": "平行线被第三条直线所截，产生同位角、内错角、同旁内角。"},
            {"type": "highlight", "content": "① 同位角相等\n② 内错角相等\n③ 同旁内角互补（和为180°）"},
            {"type": "ex", "content": "<b>判定平行：</b>如果同位角相等，则两直线平行。"}
        ],
        "quiz": [
            {"question": "直角等于多少度？", "options": ["45°", "90°", "180°", "360°"], "answer": 1, "explanation": "直角 = 90°。"},
            {"question": "平行线被截，同位角？", "options": ["互补", "相等", "互余", "不确定"], "answer": 1, "explanation": "同位角相等是平行线的核心性质。"},
            {"question": "三角形内角和等于？", "options": ["90°", "180°", "270°", "360°"], "answer": 1, "explanation": "任意三角形的三个内角之和为 180°。"}
        ]
    },
    {
        "id": "t13", "stage": "几何直觉", "stage_index": 2,
        "icon": "🔺", "title": "三角形", "description": "最稳定的形状", "sort_order": 13,
        "lesson": [
            {"type": "title", "content": "分类"},
            {"type": "text", "content": "按角分：锐角、直角、钝角三角形。按边分：等腰、等边三角形。"},
            {"type": "highlight", "content": "等边三角形三边相等，三个角都是 60°"},
            {"type": "title", "content": "面积公式"},
            {"type": "text", "content": "三角形面积 = 底 × 高 ÷ 2。"},
            {"type": "formula", "content": "S = ½ × a × h"},
            {"type": "title", "content": "勾股定理"},
            {"type": "text", "content": "直角三角形中，斜边的平方等于两直角边的平方和。"},
            {"type": "formula", "content": "a² + b² = c²（c 为斜边）"},
            {"type": "ex", "content": "<b>例：</b>3² + 4² = 9 + 16 = 25 = 5² → 斜边 = 5"}
        ],
        "quiz": [
            {"question": "等边三角形的每个角是？", "options": ["30°", "45°", "60°", "90°"], "answer": 2, "explanation": "三个角相等，和为 180°，所以每个角 = 60°。"},
            {"question": "底 10 高 6 的三角形面积是？", "options": ["16", "30", "60", "120"], "answer": 1, "explanation": "S = ½×10×6 = 30。"},
            {"question": "直角三角形两直角边 5 和 12，斜边是？", "options": ["13", "14", "15", "17"], "answer": 0, "explanation": "5² + 12² = 25+144 = 169 = 13²。"}
        ]
    },
    {
        "id": "t14", "stage": "几何直觉", "stage_index": 2,
        "icon": "🔷", "title": "四边形与多边形", "description": "从三角形到任意形状", "sort_order": 14,
        "lesson": [
            {"type": "title", "content": "四边形的家族"},
            {"type": "text", "content": "正方形、矩形、平行四边形、梯形、菱形——都是四边形。"},
            {"type": "highlight", "content": "平行四边形：两组对边分别平行\n矩形：平行四边形 + 四个直角\n正方形：矩形 + 四边相等"},
            {"type": "title", "content": "多边形内角和"},
            {"type": "text", "content": "n 边形的内角和 = (n-2) × 180°。"},
            {"type": "formula", "content": "四边形：(4-2)×180° = 360°\n五边形：(5-2)×180° = 540°"},
            {"type": "title", "content": "面积计算"},
            {"type": "formula", "content": "矩形：S = 长 × 宽\n平行四边形：S = 底 × 高\n梯形：S = (上底+下底) × 高 ÷ 2"}
        ],
        "quiz": [
            {"question": "四边形内角和是？", "options": ["180°", "360°", "540°", "720°"], "answer": 1, "explanation": "(4-2)×180° = 360°。"},
            {"question": "正方形是特殊的？", "options": ["三角形", "平行四边形", "梯形", "圆"], "answer": 1, "explanation": "正方形是特殊的矩形，矩形是特殊的平行四边形。"},
            {"question": "梯形面积公式是？", "options": ["底×高", "(上底+下底)×高÷2", "对角线乘积÷2", "边长之和"], "answer": 1, "explanation": "梯形面积 = (上底+下底) × 高 ÷ 2。"}
        ]
    },
    {
        "id": "t15", "stage": "几何直觉", "stage_index": 2,
        "icon": "⭕", "title": "圆", "description": "完美的曲线", "sort_order": 15,
        "lesson": [
            {"type": "title", "content": "圆的定义"},
            {"type": "text", "content": "圆是到定点（圆心）距离等于定值（半径）的所有点的集合。"},
            {"type": "formula", "content": "周长 C = 2πr，面积 S = πr²"},
            {"type": "title", "content": "π 是什么"},
            {"type": "text", "content": "π ≈ 3.14159... 是圆的周长与直径的比值。它是无理数，不能用分数精确表示。"},
            {"type": "ex", "content": "<b>例：</b>r = 5 → C = 2×π×5 = 10π ≈ 31.4，S = π×25 ≈ 78.5"},
            {"type": "title", "content": "扇形与弧"},
            {"type": "text", "content": "扇形是圆的一部分，由两条半径和一段弧围成。"},
            {"type": "formula", "content": "扇形面积 = (θ/360°) × πr²"}
        ],
        "quiz": [
            {"question": "π 约等于？", "options": ["2.14", "3.14", "4.14", "6.28"], "answer": 1, "explanation": "π ≈ 3.14159..."},
            {"question": "半径为 3 的圆面积是？", "options": ["3π", "6π", "9π", "12π"], "answer": 2, "explanation": "S = πr² = π×9 = 9π。"},
            {"question": "直径为 10 的圆周长是？", "options": ["5π", "10π", "20π", "100π"], "answer": 1, "explanation": "C = πd = 10π。"}
        ]
    },
    # ── 函数世界 ──
    {
        "id": "t16", "stage": "函数世界", "stage_index": 3,
        "icon": "📈", "title": "变量与函数", "description": "变化之间的依赖关系", "sort_order": 16,
        "lesson": [
            {"type": "title", "content": "什么是函数"},
            {"type": "text", "content": "函数是一种映射：每个输入对应唯一输出。"},
            {"type": "formula", "content": "f: x ↦ y"},
            {"type": "highlight", "content": "三要素：定义域、值域、对应法则"},
            {"type": "title", "content": "函数的表示"},
            {"type": "text", "content": "数值表（精确）、解析式（通用）、图像（直观）。"},
            {"type": "ex", "content": "<b>例：</b>f(x) = x²\n数值表：(-2,4),(-1,1),(0,0),(1,1),(2,4)\n图像是抛物线"},
            {"type": "title", "content": "垂直线检验"},
            {"type": "text", "content": "任意垂直线与图像至多一个交点 → 是函数。"},
            {"type": "highlight", "content": "一个 x 对应多个 y → 不是函数（如圆 x²+y²=1）"}
        ],
        "quiz": [
            {"question": "函数的核心特征是？", "options": ["可以用公式表示", "每个输入对应唯一输出", "图像是连续的", "定义域是全体实数"], "answer": 1, "explanation": "唯一性：每个合法输入有且仅有一个输出。"},
            {"question": "y² = x 是函数吗？", "options": ["是", "不是", "取决于 x", "有时是"], "answer": 1, "explanation": "x=4 时 y=±2，一个输入对应两个输出，不是函数。"},
            {"question": "f(3) 在 f(x) = 2x+1 中等于？", "options": ["5", "6", "7", "8"], "answer": 2, "explanation": "f(3) = 2×3+1 = 7。"}
        ]
    },
    {
        "id": "t17", "stage": "函数世界", "stage_index": 3,
        "icon": "📏", "title": "一次函数", "description": "线性变化——恒定的变化率", "sort_order": 17,
        "lesson": [
            {"type": "title", "content": "y = kx + b"},
            {"type": "text", "content": "k 是斜率（变化率），b 是截距（起点）。"},
            {"type": "formula", "content": "k > 0 递增，k < 0 递减，k = 0 常数"},
            {"type": "highlight", "content": "斜率 = 上升/前进 = Δy/Δx"},
            {"type": "ex", "content": "<b>例：</b>y = 2x + 1\nk=2（每前进1，上升2），b=1（过点(0,1)）\n过点(1,3)和(2,5)"},
            {"type": "title", "content": "一次函数与方程"},
            {"type": "text", "content": "一次函数 f(x)=0 的解就是图像与 x 轴的交点。"},
            {"type": "formula", "content": "2x + 1 = 0 → x = -1/2 → 交点(-1/2, 0)"}
        ],
        "quiz": [
            {"question": "y = -2x + 4 的斜率是？", "options": ["2", "-2", "4", "-4"], "answer": 1, "explanation": "k = -2，图像从左到右下降。"},
            {"question": "y = 3x - 6 与 x 轴交点是？", "options": ["(0,-6)", "(2,0)", "(-2,0)", "(6,0)"], "answer": 1, "explanation": "令 y=0：3x-6=0 → x=2，交点(2,0)。"},
            {"question": "两条平行线的斜率关系？", "options": ["互为倒数", "相等", "互为相反数", "乘积为-1"], "answer": 1, "explanation": "平行线斜率相等。"}
        ]
    },
    {
        "id": "t18", "stage": "函数世界", "stage_index": 3,
        "icon": "📉", "title": "二次函数", "description": "加速变化——抛物线", "sort_order": 18,
        "lesson": [
            {"type": "title", "content": "y = ax² + bx + c"},
            {"type": "text", "content": "图像是抛物线。a 决定开口方向，顶点是极值点。"},
            {"type": "formula", "content": "顶点式：y = a(x-h)² + k，顶点(h,k)"},
            {"type": "highlight", "content": "a > 0 开口向上（有最小值），a < 0 开口向下（有最大值）"},
            {"type": "title", "content": "零点与判别式"},
            {"type": "text", "content": "零点是图像与 x 轴的交点。"},
            {"type": "formula", "content": "Δ = b² - 4ac\nΔ > 0：两个零点\nΔ = 0：一个零点\nΔ < 0：无零点"},
            {"type": "ex", "content": "<b>例：</b>y = x² - 4x + 3\n配方：y = (x-2)² - 1\n顶点(2,-1)，零点 x=1 和 x=3"}
        ],
        "quiz": [
            {"question": "y = x² 的顶点是？", "options": ["(0,1)", "(1,0)", "(0,0)", "(-1,0)"], "answer": 2, "explanation": "y=x² 的顶点在原点(0,0)。"},
            {"question": "x² - 5x + 6 = 0 的解是？", "options": ["x=1,6", "x=2,3", "x=-2,-3", "x=0,5"], "answer": 1, "explanation": "(x-2)(x-3)=0 → x=2 或 x=3。"},
            {"question": "y = -3x² 的抛物线开口？", "options": ["向上", "向下", "向左", "不确定"], "answer": 1, "explanation": "a=-3<0，开口向下。"}
        ]
    },
    {
        "id": "t19", "stage": "函数世界", "stage_index": 3,
        "icon": "🌱", "title": "指数与对数", "description": "增长与尺度", "sort_order": 19,
        "lesson": [
            {"type": "title", "content": "指数函数 y = aˣ"},
            {"type": "text", "content": "a>1 递增（爆炸增长），0<a<1 递减（衰减）。"},
            {"type": "formula", "content": "a⁰ = 1（所有指数函数过(0,1)）"},
            {"type": "formula", "content": "eˣ 的导数等于自身——自然增长"},
            {"type": "title", "content": "对数函数 y = logₐ(x)"},
            {"type": "text", "content": "对数是指数的逆运算。问「a 的几次方等于 x？」"},
            {"type": "formula", "content": "log₂(8) = 3 因为 2³ = 8"},
            {"type": "formula", "content": "ln(e) = 1，lg(100) = 2"},
            {"type": "title", "content": "对数运算法则"},
            {"type": "formula", "content": "log(MN) = log M + log N\nlog(M/N) = log M - log N\nlog(Mⁿ) = n·log M"}
        ],
        "quiz": [
            {"question": "2³ = ?，所以 log₂(8) = ?", "options": ["2", "3", "8", "16"], "answer": 1, "explanation": "2³=8，所以 log₂(8)=3。"},
            {"question": "eˣ 的导数是？", "options": ["xeˣ⁻¹", "eˣ", "ln(eˣ)", "eˣ⁺¹"], "answer": 1, "explanation": "(eˣ)' = eˣ，自然指数的导数等于自身。"},
            {"question": "lg(1000) = ?", "options": ["1", "2", "3", "10"], "answer": 2, "explanation": "10³=1000，所以 lg(1000)=3。"}
        ]
    },
    {
        "id": "t20", "stage": "函数世界", "stage_index": 3,
        "icon": "🌊", "title": "三角函数", "description": "周期运动的语言", "sort_order": 20,
        "lesson": [
            {"type": "title", "content": "正弦与余弦"},
            {"type": "text", "content": "在单位圆上，sin θ 是 y 坐标，cos θ 是 x 坐标。"},
            {"type": "formula", "content": "sin²θ + cos²θ = 1（勾股恒等式）"},
            {"type": "highlight", "content": "周期 2π，值域 [-1,1]"},
            {"type": "title", "content": "正切"},
            {"type": "text", "content": "tan θ = sin θ / cos θ，表示斜率。"},
            {"type": "formula", "content": "tan(π/4) = 1，tan(π/3) = √3"},
            {"type": "title", "content": "图像变换"},
            {"type": "formula", "content": "y = A·sin(ωx + φ)\nA=振幅，2π/ω=周期，φ=初相位"},
            {"type": "ex", "content": "<b>例：</b>y = 2sin(3x)：振幅2，周期 2π/3"}
        ],
        "quiz": [
            {"question": "sin(π/2) = ?", "options": ["0", "1", "-1", "√2/2"], "answer": 1, "explanation": "90° 对应单位圆上的(0,1)，sin=1。"},
            {"question": "sin²θ + cos²θ = ?", "options": ["0", "1", "2", "sin2θ"], "answer": 1, "explanation": "勾股恒等式，对任意 θ 成立。"},
            {"question": "y = 3sin(x) 的振幅是？", "options": ["1", "3", "6", "π"], "answer": 1, "explanation": "A=3，振幅为 3。"}
        ]
    },
    # ── 变化的科学 ──
    {
        "id": "t21", "stage": "变化的科学", "stage_index": 4,
        "icon": "📐", "title": "斜率", "description": "变化的快慢", "sort_order": 21,
        "lesson": [
            {"type": "title", "content": "平均变化率"},
            {"type": "text", "content": "从点 A 到点 B，y 的变化量除以 x 的变化量。"},
            {"type": "formula", "content": "平均变化率 = Δy/Δx = (y₂-y₁)/(x₂-x₁)"},
            {"type": "ex", "content": "<b>例：</b>从(1,3)到(4,15)：(15-3)/(4-1) = 12/3 = 4"},
            {"type": "title", "content": "瞬时变化率"},
            {"type": "text", "content": "当 Δx 趋近于 0 时，平均变化率趋近的值就是瞬时变化率（导数）。"},
            {"type": "highlight", "content": "这就是导数的直觉——「在某个点，变化有多快」"}
        ],
        "quiz": [
            {"question": "从(2,5)到(5,14)的平均变化率是？", "options": ["2", "3", "4", "5"], "answer": 1, "explanation": "(14-5)/(5-2) = 9/3 = 3。"},
            {"question": "瞬时变化率就是？", "options": ["平均变化率", "导数", "面积", "斜率"], "answer": 1, "explanation": "瞬时变化率就是导数——切线的斜率。"},
            {"question": "f(x)=x² 在 x=3 处的变化率约为？", "options": ["3", "6", "9", "12"], "answer": 1, "explanation": "f'(x)=2x，f'(3)=6。"}
        ]
    },
    {
        "id": "t22", "stage": "变化的科学", "stage_index": 4,
        "icon": "📐", "title": "导数", "description": "瞬时变化率——切线斜率", "sort_order": 22,
        "lesson": [
            {"type": "title", "content": "导数的定义"},
            {"type": "formula", "content": "f'(x) = lim[Δx→0] (f(x+Δx) - f(x)) / Δx"},
            {"type": "formula", "content": "(xⁿ)' = nxⁿ⁻¹\n(sin x)' = cos x\n(eˣ)' = eˣ\n(ln x)' = 1/x"},
            {"type": "title", "content": "导数的几何意义"},
            {"type": "text", "content": "导数是曲线在该点切线的斜率。"},
            {"type": "ex", "content": "<b>例：</b>f(x) = x³\nf'(x) = 3x²\n在 x=2 处，切线斜率 = 3×4 = 12"},
            {"type": "title", "content": "求导法则"},
            {"type": "text", "content": "四则运算 + 链式法则。"},
            {"type": "formula", "content": "(u+v)' = u' + v'\n(uv)' = u'v + uv'\n(f(g(x)))' = f'(g(x)) · g'(x)"}
        ],
        "quiz": [
            {"question": "(x³)' = ?", "options": ["x²", "3x²", "3x", "x³"], "answer": 1, "explanation": "幂函数法则：(xⁿ)' = nxⁿ⁻¹。"},
            {"question": "(sin x)' = ?", "options": ["sin x", "-sin x", "cos x", "-cos x"], "answer": 2, "explanation": "正弦的导数是余弦。"},
            {"question": "(eˣ)' = ?", "options": ["xeˣ⁻¹", "eˣ", "1", "eˣ⁺¹"], "answer": 1, "explanation": "自然指数的导数等于自身。"}
        ]
    },
    {
        "id": "t23", "stage": "变化的科学", "stage_index": 4,
        "icon": "⛰️", "title": "导数应用", "description": "最值与优化", "sort_order": 23,
        "lesson": [
            {"type": "title", "content": "单调性判定"},
            {"type": "text", "content": "f' > 0 → 递增，f' < 0 → 递减。"},
            {"type": "ex", "content": "<b>例：</b>f(x) = x³ - 3x\nf'(x) = 3x² - 3 = 3(x-1)(x+1)\nf' > 0 当 x < -1 或 x > 1 → 递增\nf' < 0 当 -1 < x < 1 → 递减"},
            {"type": "title", "content": "极值判定"},
            {"type": "text", "content": "f'(x₀) = 0 且 f' 从正变负 → 极大值\nf'(x₀) = 0 且 f' 从负变正 → 极小值"},
            {"type": "ex", "content": "<b>例：</b>极大值 f(-1) = 2，极小值 f(1) = -2"},
            {"type": "title", "content": "闭区间最值"},
            {"type": "text", "content": "比较端点值和极值点的函数值，取最大/最小。"},
            {"type": "highlight", "content": "闭区间上的连续函数一定能取到最大值和最小值"}
        ],
        "quiz": [
            {"question": "f'(x) > 0 意味着 f(x)？", "options": ["递减", "递增", "常数", "有极值"], "answer": 1, "explanation": "导数大于零 → 函数递增。"},
            {"question": "f(x)=x² 的最小值在？", "options": ["x=-1", "x=0", "x=1", "不存在"], "answer": 1, "explanation": "f'(x)=2x=0 → x=0，且 a>0 开口向上，最小值。"},
            {"question": "y = x² - 4x + 5 的最小值是？", "options": ["0", "1", "2", "5"], "answer": 1, "explanation": "y=(x-2)²+1，最小值在 x=2 时为 1。"}
        ]
    },
    {
        "id": "t24", "stage": "变化的科学", "stage_index": 4,
        "icon": "📊", "title": "积分", "description": "累积与面积", "sort_order": 24,
        "lesson": [
            {"type": "title", "content": "不定积分"},
            {"type": "text", "content": "积分是求导的逆运算。求原函数族。"},
            {"type": "formula", "content": "∫x²dx = x³/3 + C\n∫eˣdx = eˣ + C\n∫(1/x)dx = ln|x| + C"},
            {"type": "title", "content": "定积分"},
            {"type": "text", "content": "定积分表示曲线下的有向面积。"},
            {"type": "formula", "content": "∫ₐᵇ f(x)dx = F(b) - F(a)"},
            {"type": "ex", "content": "<b>例：</b>∫₀² x dx = [x²/2]₀² = 2 - 0 = 2"},
            {"type": "title", "content": "微积分基本定理"},
            {"type": "text", "content": "导数和积分互为逆运算——连接两个世界的桥梁。"},
            {"type": "formula", "content": "d/dx ∫ₐˣ f(t)dt = f(x)"}
        ],
        "quiz": [
            {"question": "∫2x dx = ?", "options": ["x²", "x² + C", "2", "2x + C"], "answer": 1, "explanation": "不定积分要加常数 C。"},
            {"question": "∫₀¹ x dx = ?", "options": ["0", "1/2", "1", "2"], "answer": 1, "explanation": "[x²/2]₀¹ = 1/2。"},
            {"question": "微积分基本定理连接了？", "options": ["极限与连续", "导数与积分", "函数与方程", "数列与级数"], "answer": 1, "explanation": "导数和积分互为逆运算。"}
        ]
    },
    {
        "id": "t25", "stage": "变化的科学", "stage_index": 4,
        "icon": "🌉", "title": "微积分基本定理", "description": "两个世界的桥梁", "sort_order": 25,
        "lesson": [
            {"type": "title", "content": "定理的内容"},
            {"type": "text", "content": "如果 F'(x) = f(x)，那么 ∫ₐᵇ f(x)dx = F(b) - F(a)。"},
            {"type": "highlight", "content": "这告诉我们：求面积（积分）可以转化为求原函数（导数的逆运算）"},
            {"type": "title", "content": "为什么这是桥梁"},
            {"type": "text", "content": "微分研究变化率，积分研究累积量。这个定理说明它们是同一枚硬币的两面。"},
            {"type": "ex", "content": "<b>例：</b>速度函数 v(t) 的积分 = 位移\n位移函数 s(t) 的导数 = 速度"},
            {"type": "title", "content": "应用"},
            {"type": "text", "content": "物理学中无处不在：速度↔位移，加速度↔速度，力↔功。"},
            {"type": "formula", "content": "∫₀ᵀ v(t)dt = s(T) - s(0)（位移）"}
        ],
        "quiz": [
            {"question": "F'(x) = f(x)，则 ∫ₐᵇ f(x)dx = ?", "options": ["F(a) - F(b)", "F(b) - F(a)", "F(a) + F(b)", "f(b) - f(a)"], "answer": 1, "explanation": "牛顿-莱布尼兹公式：F(b) - F(a)。"},
            {"question": "速度的积分等于？", "options": ["加速度", "位移", "力", "功"], "answer": 1, "explanation": "速度的积分是位移。"},
            {"question": "位移的导数等于？", "options": ["加速度", "速度", "力", "面积"], "answer": 1, "explanation": "位移的导数是速度。"}
        ]
    },
    # ── 抽象与推理 ──
    {
        "id": "t26", "stage": "抽象与推理", "stage_index": 5,
        "icon": "🔢", "title": "数列", "description": "有序的数——从规律到通项", "sort_order": 26,
        "lesson": [
            {"type": "title", "content": "什么是数列"},
            {"type": "text", "content": "按一定规律排列的一列数。每个数叫项，位置叫项数。"},
            {"type": "formula", "content": "1, 3, 5, 7, 9, ...（奇数列）\n1, 2, 4, 8, 16, ...（等比数列）"},
            {"type": "title", "content": "等差数列"},
            {"type": "text", "content": "每相邻两项的差相等（公差 d）。"},
            {"type": "formula", "content": "aₙ = a₁ + (n-1)d\n前n项和 Sₙ = n(a₁+aₙ)/2"},
            {"type": "ex", "content": "<b>例：</b>2, 5, 8, 11, ...\na₁=2, d=3\na₁₀ = 2 + 9×3 = 29"},
            {"type": "title", "content": "等比数列"},
            {"type": "text", "content": "每相邻两项的比相等（公比 q）。"},
            {"type": "formula", "content": "aₙ = a₁ · qⁿ⁻¹\n前n项和 Sₙ = a₁(1-qⁿ)/(1-q)"}
        ],
        "quiz": [
            {"question": "等差数列 3,7,11,15,... 的公差是？", "options": ["3", "4", "5", "7"], "answer": 1, "explanation": "7-3=4，11-7=4，公差 d=4。"},
            {"question": "等比数列 2,6,18,... 的公比是？", "options": ["2", "3", "6", "9"], "answer": 1, "explanation": "6/2=3，18/6=3，公比 q=3。"},
            {"question": "1+2+3+...+100 = ?", "options": ["5050", "5000", "10000", "500"], "answer": 0, "explanation": "S = 100×(1+100)/2 = 5050。"}
        ]
    },
    {
        "id": "t27", "stage": "抽象与推理", "stage_index": 5,
        "icon": "📚", "title": "集合", "description": "数学的语言——把东西归类", "sort_order": 27,
        "lesson": [
            {"type": "title", "content": "集合是什么"},
            {"type": "text", "content": "集合是一些确定的、互不相同的对象的整体。"},
            {"type": "formula", "content": "A = {1, 2, 3}，B = {x | x > 0}（所有正数）"},
            {"type": "title", "content": "集合的关系"},
            {"type": "text", "content": "子集、真子集、相等、空集。"},
            {"type": "highlight", "content": "A ⊆ B：A 的所有元素都在 B 中\nA ⊂ B：A ⊆ B 且 A ≠ B\n∅ ⊆ A（空集是任何集合的子集）"},
            {"type": "title", "content": "集合的运算"},
            {"type": "text", "content": "交集、并集、补集。"},
            {"type": "formula", "content": "A ∩ B = {x | x∈A 且 x∈B}（公共部分）\nA ∪ B = {x | x∈A 或 x∈B}（全部合并）"}
        ],
        "quiz": [
            {"question": "{1,2,3} 和 {2,3,4} 的交集是？", "options": ["{1,4}", "{2,3}", "{1,2,3,4}", "∅"], "answer": 1, "explanation": "交集是公共元素：{2,3}。"},
            {"question": "空集是什么的子集？", "options": ["空集", "自己", "任何集合", "非空集合"], "answer": 2, "explanation": "空集是任何集合的子集。"},
            {"question": "A={1,2}, B={2,3}，A∪B = ?", "options": ["{1,2,3}", "{2}", "{1,3}", "{1,2,2,3}"], "answer": 0, "explanation": "并集合并所有元素（去重）：{1,2,3}。"}
        ]
    },
    {
        "id": "t28", "stage": "抽象与推理", "stage_index": 5,
        "icon": "🧠", "title": "逻辑与证明", "description": "推理的规则——从已知到未知", "sort_order": 28,
        "lesson": [
            {"type": "title", "content": "命题与条件"},
            {"type": "text", "content": "命题是可以判断真假的陈述句。"},
            {"type": "formula", "content": "如果 P，那么 Q（P→Q）\nP 是条件，Q 是结论"},
            {"type": "title", "content": "充分与必要"},
            {"type": "text", "content": "P→Q：P 是 Q 的充分条件，Q 是 P 的必要条件。"},
            {"type": "ex", "content": "<b>例：</b>「x=2」是「x²=4」的充分条件（x=2 一定推出 x²=4）\n但不是必要条件（x=-2 也满足 x²=4）"},
            {"type": "title", "content": "反证法"},
            {"type": "text", "content": "假设结论不成立 → 推出矛盾 → 所以结论成立。"},
            {"type": "ex", "content": "<b>例：</b>证明 √2 是无理数\n假设 √2 = p/q（最简分数）\n则 2q² = p² → p 是偶数 → p=2k → 2q²=4k² → q²=2k² → q 也是偶数\n矛盾！p,q 都是偶数，不是最简分数。"}
        ],
        "quiz": [
            {"question": "「如果下雨，那么地湿」中，下雨是？", "options": ["必要条件", "充分条件", "充要条件", "无关条件"], "answer": 1, "explanation": "下雨一定能推出地湿，所以是充分条件。"},
            {"question": "反证法的第一步是？", "options": ["直接证明", "假设结论不成立", "画图", "代入验证"], "answer": 1, "explanation": "反证法：先假设结论的否定成立。"},
            {"question": "P→Q 的逆命题是？", "options": ["Q→P", "P→Q", "非P→非Q", "非Q→非P"], "answer": 0, "explanation": "逆命题：交换条件和结论，Q→P。"}
        ]
    },
    {
        "id": "t29", "stage": "抽象与推理", "stage_index": 5,
        "icon": "🎲", "title": "概率", "description": "不确定性——从直觉到计算", "sort_order": 29,
        "lesson": [
            {"type": "title", "content": "概率是什么"},
            {"type": "text", "content": "概率描述事件发生的可能性大小，范围 [0, 1]。"},
            {"type": "formula", "content": "P(事件) = 有利结果数 / 总结果数"},
            {"type": "highlight", "content": "P=0 不可能发生，P=1 一定发生"},
            {"type": "title", "content": "加法原理"},
            {"type": "text", "content": "互斥事件（不能同时发生）的概率可以直接相加。"},
            {"type": "formula", "content": "P(A 或 B) = P(A) + P(B)（A,B 互斥）"},
            {"type": "ex", "content": "<b>例：</b>掷骰子，P(偶数) = P(2)+P(4)+P(6) = 3/6 = 1/2"},
            {"type": "title", "content": "独立事件"},
            {"type": "text", "content": "一个事件的结果不影响另一个。"},
            {"type": "formula", "content": "P(A 且 B) = P(A) × P(B)（A,B 独立）"},
            {"type": "ex", "content": "<b>例：</b>两次掷硬币都正面：1/2 × 1/2 = 1/4"}
        ],
        "quiz": [
            {"question": "掷一个骰子，P(点数>4) = ?", "options": ["1/6", "2/6", "3/6", "4/6"], "answer": 1, "explanation": ">4 的有 5,6 两个，P = 2/6 = 1/3。"},
            {"question": "掷硬币两次都正面的概率？", "options": ["1/2", "1/3", "1/4", "1/8"], "answer": 2, "explanation": "1/2 × 1/2 = 1/4。"},
            {"question": "P(A)+P(非A) = ?", "options": ["0", "1", "2", "不确定"], "answer": 1, "explanation": "互补事件概率之和为 1。"}
        ]
    },
    {
        "id": "t30", "stage": "抽象与推理", "stage_index": 5,
        "icon": "📊", "title": "统计", "description": "从数据中发现规律", "sort_order": 30,
        "lesson": [
            {"type": "title", "content": "平均数、中位数、众数"},
            {"type": "text", "content": "三种「代表值」，各有适用场景。"},
            {"type": "highlight", "content": "平均数：所有数据之和 ÷ 个数\n中位数：排序后中间的数\n众数：出现次数最多的数"},
            {"type": "ex", "content": "<b>例：</b>数据 2,3,3,5,7\n平均数 = 20/5 = 4，中位数 = 3，众数 = 3"},
            {"type": "title", "content": "方差与标准差"},
            {"type": "text", "content": "描述数据的离散程度。"},
            {"type": "formula", "content": "方差 σ² = Σ(xᵢ - μ)² / n\n标准差 σ = √方差"},
            {"type": "highlight", "content": "方差大 → 数据分散，方差小 → 数据集中"},
            {"type": "title", "content": "正态分布"},
            {"type": "text", "content": "自然界最常见的分布——钟形曲线。"},
            {"type": "highlight", "content": "约 68% 的数据在 μ±σ 内\n约 95% 在 μ±2σ 内\n约 99.7% 在 μ±3σ 内"}
        ],
        "quiz": [
            {"question": "数据 1,3,5,7,9 的平均数是？", "options": ["3", "5", "7", "45"], "answer": 1, "explanation": "(1+3+5+7+9)/5 = 25/5 = 5。"},
            {"question": "方差描述的是？", "options": ["平均水平", "中间值", "离散程度", "最大值"], "answer": 2, "explanation": "方差描述数据偏离平均值的程度。"},
            {"question": "正态分布中约 68% 数据在？", "options": ["μ±σ 内", "μ±2σ 内", "μ±3σ 内", "全部在均值处"], "answer": 0, "explanation": "约 68% 数据在平均值一个标准差范围内。"}
        ]
    },
]


def seed_all(conn):
    """导入所有种子数据"""
    # 需要 lesson_sections 和 quiz_questions 表
    conn.execute("""
        CREATE TABLE IF NOT EXISTS lesson_sections (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            topic_id TEXT NOT NULL,
            section_type TEXT NOT NULL,
            content TEXT NOT NULL,
            sort_order INTEGER NOT NULL,
            FOREIGN KEY (topic_id) REFERENCES topics(id)
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS quiz_questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            topic_id TEXT NOT NULL,
            question TEXT NOT NULL,
            options TEXT NOT NULL,
            answer INTEGER NOT NULL,
            explanation TEXT,
            sort_order INTEGER NOT NULL,
            FOREIGN KEY (topic_id) REFERENCES topics(id)
        )
    """)

    seed_topics(conn, TOPICS)


def seed_topics(conn, topics):
    """导入指定的主题列表到数据库"""
    for topic in topics:
        conn.execute(
            "INSERT OR IGNORE INTO topics (id, stage, stage_index, title, description, icon, sort_order) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (topic["id"], topic["stage"], topic["stage_index"], topic["title"], topic["description"], topic["icon"], topic["sort_order"])
        )
        for i, section in enumerate(topic["lesson"]):
            conn.execute(
                "INSERT OR IGNORE INTO lesson_sections (topic_id, section_type, content, sort_order) VALUES (?, ?, ?, ?)",
                (topic["id"], section["type"], section["content"], i)
            )
        for i, q in enumerate(topic["quiz"]):
            conn.execute(
                "INSERT OR IGNORE INTO quiz_questions (topic_id, question, options, answer, explanation, sort_order) VALUES (?, ?, ?, ?, ?, ?)",
                (topic["id"], q["question"], json.dumps(q["options"], ensure_ascii=False), q["answer"], q["explanation"], i)
            )
