"""定位测试种子数据 — 7 阶段 × 3 题 = 21 道定位题"""

PLACEMENT_QUESTIONS = [
    # ── 阶段 0：数的起源 ──
    {
        "stage_index": 0, "difficulty": 1,
        "question": "345 中的「4」代表什么？",
        "options": ["4", "40", "400", "4000"], "answer": 1,
        "explanation": "十位上的 4 代表 4×10 = 40。"
    },
    {
        "stage_index": 0, "difficulty": 2,
        "question": "3 × (4+5) = ?",
        "options": ["7", "12", "15", "27"], "answer": 3,
        "explanation": "分配律：3×(4+5) = 3×4 + 3×5 = 12+15 = 27。"
    },
    {
        "stage_index": 0, "difficulty": 3,
        "question": "2/3 + 1/6 = ?",
        "options": ["3/9", "1/2", "5/6", "3/6"], "answer": 2,
        "explanation": "通分：2/3 = 4/6，4/6 + 1/6 = 5/6。"
    },
    # ── 阶段 1：代数语言 ──
    {
        "stage_index": 1, "difficulty": 1,
        "question": "如果 2x = 10，那么 x = ?",
        "options": ["2", "5", "8", "12"], "answer": 1,
        "explanation": "两边同时除以 2：x = 10 ÷ 2 = 5。"
    },
    {
        "stage_index": 1, "difficulty": 2,
        "question": "3x + 5 = 20，求 x",
        "options": ["3", "5", "7", "15"], "answer": 1,
        "explanation": "3x = 20 - 5 = 15，x = 15 ÷ 3 = 5。"
    },
    {
        "stage_index": 1, "difficulty": 3,
        "question": "不等式 2x - 3 > 5 的解集是？",
        "options": ["x > 1", "x > 4", "x > 2", "x > 8"], "answer": 1,
        "explanation": "2x > 5 + 3 = 8，x > 4。"
    },
    # ── 阶段 2：几何直觉 ──
    {
        "stage_index": 2, "difficulty": 1,
        "question": "三角形内角和等于？",
        "options": ["90°", "180°", "270°", "360°"], "answer": 1,
        "explanation": "三角形三个内角之和等于 180°。"
    },
    {
        "stage_index": 2, "difficulty": 2,
        "question": "直角三角形两直角边为 3 和 4，斜边为？",
        "options": ["5", "6", "7", "12"], "answer": 0,
        "explanation": "勾股定理：c² = 3² + 4² = 9 + 16 = 25，c = 5。"
    },
    {
        "stage_index": 2, "difficulty": 3,
        "question": "圆的面积公式是？",
        "options": ["2πr", "πr²", "πd", "4πr²"], "answer": 1,
        "explanation": "圆面积 = πr²，其中 r 是半径。"
    },
    # ── 阶段 3：函数世界 ──
    {
        "stage_index": 3, "difficulty": 1,
        "question": "f(x) = 2x + 1，f(3) = ?",
        "options": ["5", "6", "7", "8"], "answer": 2,
        "explanation": "f(3) = 2×3 + 1 = 7。"
    },
    {
        "stage_index": 3, "difficulty": 2,
        "question": "y = x² 的图像是什么形状？",
        "options": ["直线", "抛物线", "圆", "双曲线"], "answer": 1,
        "explanation": "二次函数 y = x² 的图像是开口向上的抛物线。"
    },
    {
        "stage_index": 3, "difficulty": 3,
        "question": "y = x² - 4x + 3 的顶点坐标是？",
        "options": ["(2, -1)", "(-2, -1)", "(2, 1)", "(4, 3)"], "answer": 0,
        "explanation": "配方：y = (x-2)² - 1，顶点为 (2, -1)。"
    },
    # ── 阶段 4：变化的科学 ──
    {
        "stage_index": 4, "difficulty": 1,
        "question": "f(x) = x² 的导数 f'(x) = ?",
        "options": ["x", "2x", "x²", "2x²"], "answer": 1,
        "explanation": "幂函数求导：(xⁿ)' = nxⁿ⁻¹，所以 (x²)' = 2x。"
    },
    {
        "stage_index": 4, "difficulty": 2,
        "question": "f(x) = 3x² + 2x 在 x=1 处的导数值是？",
        "options": ["5", "6", "8", "11"], "answer": 2,
        "explanation": "f'(x) = 6x + 2，f'(1) = 6 + 2 = 8。"
    },
    {
        "stage_index": 4, "difficulty": 3,
        "question": "∫₀¹ 2x dx = ?",
        "options": ["0", "1", "2", "x²"], "answer": 1,
        "explanation": "∫2x dx = x²，从 0 到 1：1² - 0² = 1。"
    },
    # ── 阶段 5：抽象与推理 ──
    {
        "stage_index": 5, "difficulty": 1,
        "question": "集合 A={1,2,3}，B={2,3,4}，A∩B = ?",
        "options": ["{1,4}", "{2,3}", "{1,2,3,4}", "{∅}"], "answer": 1,
        "explanation": "交集是两个集合共有的元素：{2,3}。"
    },
    {
        "stage_index": 5, "difficulty": 2,
        "question": "等差数列 2, 5, 8, 11, ... 的公差是？",
        "options": ["2", "3", "4", "5"], "answer": 1,
        "explanation": "公差 = 后项 - 前项 = 5 - 2 = 3。"
    },
    {
        "stage_index": 5, "difficulty": 3,
        "question": "等比数列 3, 6, 12, 24, ... 的第 6 项是？",
        "options": ["48", "72", "96", "192"], "answer": 2,
        "explanation": "公比为 2，第 n 项 = 3×2^(n-1)，第 6 项 = 3×2⁵ = 96。"
    },
    # ── 阶段 6：高等数学 ──
    {
        "stage_index": 6, "difficulty": 1,
        "question": "lim(x→0) sin(x)/x = ?",
        "options": ["0", "1", "∞", "不存在"], "answer": 1,
        "explanation": "重要极限：lim(x→0) sin(x)/x = 1。"
    },
    {
        "stage_index": 6, "difficulty": 2,
        "question": "f(x,y) = x² + y² 对 x 的偏导数是？",
        "options": ["2x + 2y", "2x", "2y", "x²"], "answer": 1,
        "explanation": "对 x 求偏导时，y 视为常数，∂f/∂x = 2x。"
    },
    {
        "stage_index": 6, "difficulty": 3,
        "question": "∫ e^x dx = ?",
        "options": ["e^x + C", "xe^x + C", "e^(x+1)/ (x+1) + C", "ln|x| + C"], "answer": 0,
        "explanation": "e^x 的不定积分就是 e^x + C，因为 (e^x)' = e^x。"
    },
]
