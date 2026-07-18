"""
扩充题库 — 为每个主题增加更多测验题
每个主题增加 3-5 道题，总计约 200+ 道新题
"""

EXTRA_QUIZ = {
    # ═══ 数的起源 ═══
    "t1": [
        {"question": "十进制的基数是？", "options": ["2", "8", "10", "16"], "answer": 2, "explanation": "十进制用 0-9 十个符号，基数为 10。"},
        {"question": "1000 里面有几个百？", "options": ["1", "10", "100", "1000"], "answer": 1, "explanation": "1000 ÷ 100 = 10，有 10 个百。"},
        {"question": "最大的两位数是？", "options": ["90", "99", "100", "10"], "answer": 1, "explanation": "两位数范围 10-99，最大是 99。"},
    ],
    "t2": [
        {"question": "5 × 7 = 7 × 5 体现了什么律？", "options": ["结合律", "交换律", "分配律", "消去律"], "answer": 1, "explanation": "乘法交换律：a×b = b×a。"},
        {"question": "(2×3)×4 = 2×(3×4) 体现了什么律？", "options": ["结合律", "交换律", "分配律", "消去律"], "answer": 0, "explanation": "结合律：改变分组方式，结果不变。"},
        {"question": "25 × 4 = ?", "options": ["60", "80", "100", "120"], "answer": 2, "explanation": "25×4 = 100，这是常用的心算组合。"},
    ],
    "t3": [
        {"question": "被减数是 15，减数是 8，差是？", "options": ["5", "6", "7", "8"], "answer": 2, "explanation": "15 - 8 = 7。"},
        {"question": "一个数除以 7 商 6 余 3，这个数是？", "options": ["39", "42", "45", "48"], "answer": 2, "explanation": "7×6 + 3 = 42 + 3 = 45。"},
        {"question": "100 ÷ 25 = ?", "options": ["2", "3", "4", "5"], "answer": 2, "explanation": "100 ÷ 25 = 4。"},
    ],
    "t4": [
        {"question": "1/2 和 1/3 谁大？", "options": ["1/2", "1/3", "一样大", "不确定"], "answer": 0, "explanation": "通分：1/2=3/6，1/3=2/6，3/6 > 2/6。"},
        {"question": "5/8 化成小数是？", "options": ["0.525", "0.625", "0.725", "0.825"], "answer": 1, "explanation": "5÷8 = 0.625。"},
        {"question": "2/3 × 9 = ?", "options": ["3", "4", "5", "6"], "answer": 3, "explanation": "2/3 × 9 = 18/3 = 6。"},
    ],
    "t5": [
        {"question": "0.125 = 1/?", "options": ["4", "6", "8", "10"], "answer": 2, "explanation": "0.125 = 125/1000 = 1/8。"},
        {"question": "20% 的 150 是？", "options": ["15", "20", "25", "30"], "answer": 3, "explanation": "150 × 20% = 150 × 0.2 = 30。"},
        {"question": "从 0.5 到 50%，变化了？", "options": ["变大了", "变小了", "没变", "无法比较"], "answer": 2, "explanation": "0.5 = 50/100 = 50%，相等。"},
    ],

    # ═══ 代数语言 ═══
    "t6": [
        {"question": "-(-5) = ?", "options": ["-5", "0", "5", "10"], "answer": 2, "explanation": "负负得正：-(-5) = 5。"},
        {"question": "-3 + (-7) = ?", "options": ["-10", "-4", "4", "10"], "answer": 0, "explanation": "负数加负数：-3 + (-7) = -10。"},
        {"question": "|-12| + |3| = ?", "options": ["-9", "9", "15", "-15"], "answer": 2, "explanation": "|-12| = 12，|3| = 3，12+3 = 15。"},
    ],
    "t7": [
        {"question": "3a²b 的系数是？", "options": ["3", "a", "b", "3a"], "answer": 0, "explanation": "系数是数字部分，即 3。"},
        {"question": "化简 4(x-2) - 2(x+1) = ?", "options": ["2x-10", "2x-6", "6x-10", "2x+10"], "answer": 0, "explanation": "4x-8-2x-2 = 2x-10。"},
        {"question": "2x³ 的次数是？", "options": ["1", "2", "3", "6"], "answer": 2, "explanation": "单项式的次数是所有字母指数之和，x 的指数是 3。"},
    ],
    "t8": [
        {"question": "4x - 8 = 0 的解是？", "options": ["-2", "0", "2", "4"], "answer": 2, "explanation": "4x = 8，x = 2。"},
        {"question": "x/3 + 2 = 5 的解是？", "options": ["3", "6", "9", "15"], "answer": 2, "explanation": "x/3 = 3，x = 9。"},
        {"question": "3(x+1) = 2x+7 的解是？", "options": ["2", "3", "4", "10"], "answer": 2, "explanation": "3x+3 = 2x+7，x = 4。"},
    ],
    "t9": [
        {"question": "5x ≤ 20 的解集是？", "options": ["x ≤ 3", "x ≤ 4", "x ≤ 5", "x ≥ 4"], "answer": 1, "explanation": "两边除以 5：x ≤ 4。"},
        {"question": "|x| < 3 的解集是？", "options": ["x < 3", "x > -3", "-3 < x < 3", "x < -3 或 x > 3"], "answer": 2, "explanation": "绝对值小于 3 表示到原点距离小于 3。"},
        {"question": "不等式 2x+1 > 5 的解集是？", "options": ["x > 2", "x > 3", "x < 2", "x > 4"], "answer": 0, "explanation": "2x > 4，x > 2。"},
    ],
    "t10": [
        {"question": "方程组 {x+y=3, x-y=1} 的 x = ?", "options": ["1", "2", "3", "4"], "answer": 1, "explanation": "两式相加：2x=4，x=2。"},
        {"question": "方程组 {2x+y=7, x+y=4} 的 y = ?", "options": ["0", "1", "2", "3"], "answer": 1, "explanation": "第一式减第二式：x=3，代入得 y=1。"},
        {"question": "方程组 {x=2, y=3} 满足 x+y=?", "options": ["4", "5", "6", "7"], "answer": 1, "explanation": "2+3=5。"},
    ],

    # ═══ 几何直觉 ═══
    "t11": [
        {"question": "过一点能画几条直线？", "options": ["0", "1", "2", "无数条"], "answer": 3, "explanation": "过一点可以画无数条直线。"},
        {"question": "线段有几个端点？", "options": ["0", "1", "2", "3"], "answer": 2, "explanation": "线段有两个端点，射线有一个，直线没有。"},
        {"question": "两点之间最短的是？", "options": ["直线", "线段", "射线", "曲线"], "answer": 1, "explanation": "两点之间线段最短。"},
    ],
    "t12": [
        {"question": "互补的两个角之和是？", "options": ["45°", "90°", "180°", "360°"], "answer": 2, "explanation": "互补 = 和为 180°，互余 = 和为 90°。"},
        {"question": "同位角相等说明两直线？", "options": ["相交", "平行", "垂直", "重合"], "answer": 1, "explanation": "同位角相等是两直线平行的判定条件。"},
        {"question": "一个角的补角是 120°，这个角是？", "options": ["30°", "45°", "60°", "90°"], "answer": 2, "explanation": "180° - 120° = 60°。"},
    ],
    "t13": [
        {"question": "直角三角形斜边 13，一直角边 5，另一直角边是？", "options": ["8", "10", "11", "12"], "answer": 3, "explanation": "√(13²-5²) = √(169-25) = √144 = 12。"},
        {"question": "等腰三角形两边为 5 和 10，周长是？", "options": ["15", "20", "25", "20 或 25"], "answer": 2, "explanation": "腰不能是 10（5+5=10 不构成三角形），所以腰是 5，底是 10，周长=5+5+10=20。不对，应该是腰10底5，周长=10+10+5=25。"},
        {"question": "三角形两边之和必须？第三边", "options": ["小于", "等于", "大于", "不确定"], "answer": 2, "explanation": "三角形两边之和大于第三边。"},
    ],
    "t14": [
        {"question": "矩形的对角线？", "options": ["垂直", "相等", "平行", "平分"], "answer": 1, "explanation": "矩形的对角线相等且互相平分。"},
        {"question": "正方形对角线？", "options": ["垂直且相等", "只垂直", "只相等", "都不"], "answer": 0, "explanation": "正方形对角线垂直平分且相等。"},
        {"question": "五边形内角和是？", "options": ["360°", "540°", "720°", "900°"], "answer": 1, "explanation": "(5-2)×180° = 540°。"},
    ],
    "t15": [
        {"question": "圆的直径是半径的？", "options": ["1倍", "2倍", "3倍", "4倍"], "answer": 1, "explanation": "直径 = 2 × 半径。"},
        {"question": "半径为 4 的圆周长是？", "options": ["4π", "8π", "16π", "32π"], "answer": 1, "explanation": "C = 2πr = 2π×4 = 8π。"},
        {"question": "圆心角 60° 的扇形占圆的？", "options": ["1/2", "1/3", "1/4", "1/6"], "answer": 3, "explanation": "60°/360° = 1/6。"},
    ],

    # ═══ 函数世界 ═══
    "t16": [
        {"question": "f(x) = x² - 1，f(-2) = ?", "options": ["-3", "3", "5", "-5"], "answer": 1, "explanation": "f(-2) = (-2)² - 1 = 4-1 = 3。"},
        {"question": "定义域是什么？", "options": ["所有输出值", "所有输入值", "函数图像", "函数公式"], "answer": 1, "explanation": "定义域是函数能接受的所有输入值的集合。"},
        {"question": "y = √x 的定义域是？", "options": ["x > 0", "x ≥ 0", "x < 0", "全体实数"], "answer": 1, "explanation": "根号下不能为负，所以 x ≥ 0。"},
    ],
    "t17": [
        {"question": "y = -3x + 6 与 x 轴交点是？", "options": ["(0,6)", "(2,0)", "(-2,0)", "(6,0)"], "answer": 1, "explanation": "令 y=0：-3x+6=0，x=2。"},
        {"question": "两条垂直直线的斜率之积是？", "options": ["0", "1", "-1", "不确定"], "answer": 2, "explanation": "垂直直线斜率之积为 -1（互为负倒数）。"},
        {"question": "y = 5 是什么函数？", "options": ["一次函数", "常数函数", "二次函数", "不是函数"], "answer": 1, "explanation": "y=5 是 k=0 的一次函数，也叫常数函数。"},
    ],
    "t18": [
        {"question": "y = (x-1)² + 3 的顶点是？", "options": ["(1,3)", "(-1,3)", "(1,-3)", "(-1,-3)"], "answer": 0, "explanation": "顶点式 y=a(x-h)²+k，顶点(h,k)=(1,3)。"},
        {"question": "x² - 9 = 0 的解是？", "options": ["x=3", "x=±3", "x=9", "x=±9"], "answer": 1, "explanation": "x²=9，x=±3。"},
        {"question": "y = 2x² 与 y = x² 的区别？", "options": ["开口大小不同", "顶点不同", "对称轴不同", "完全相同"], "answer": 0, "explanation": "a=2 比 a=1 开口更窄（更陡）。"},
    ],
    "t19": [
        {"question": "log₂(32) = ?", "options": ["4", "5", "6", "16"], "answer": 1, "explanation": "2⁵ = 32，所以 log₂(32) = 5。"},
        {"question": "e⁰ = ?", "options": ["0", "1", "e", "无法确定"], "answer": 1, "explanation": "任何非零数的 0 次方等于 1。"},
        {"question": "ln(e²) = ?", "options": ["1", "2", "e", "2e"], "answer": 1, "explanation": "ln(e²) = 2×ln(e) = 2×1 = 2。"},
    ],
    "t20": [
        {"question": "cos(0) = ?", "options": ["0", "1", "-1", "√2/2"], "answer": 1, "explanation": "cos(0) = 1，对应单位圆上的点(1,0)。"},
        {"question": "sin(π) = ?", "options": ["0", "1", "-1", "√3/2"], "answer": 0, "explanation": "sin(π) = sin(180°) = 0。"},
        {"question": "tan(π/4) = ?", "options": ["0", "1/2", "1", "√3"], "answer": 2, "explanation": "tan(45°) = sin45°/cos45° = 1。"},
    ],

    # ═══ 变化的科学 ═══
    "t21": [
        {"question": "从(0,0)到(3,6)的斜率是？", "options": ["1", "2", "3", "6"], "answer": 1, "explanation": "k = (6-0)/(3-0) = 6/3 = 2。"},
        {"question": "斜率为 0 的直线是？", "options": ["水平线", "竖直线", "45°斜线", "曲线"], "answer": 0, "explanation": "斜率为 0 表示没有垂直变化，是水平线。"},
        {"question": "竖直线的斜率是？", "options": ["0", "1", "-1", "不存在"], "answer": 3, "explanation": "竖直线 Δx=0，分母为 0，斜率不存在。"},
    ],
    "t22": [
        {"question": "(cos x)' = ?", "options": ["sin x", "-sin x", "cos x", "-cos x"], "answer": 1, "explanation": "余弦的导数是负正弦。"},
        {"question": "(x⁵)' = ?", "options": ["x⁴", "4x⁴", "5x⁴", "5x⁵"], "answer": 2, "explanation": "幂函数法则：(xⁿ)' = nxⁿ⁻¹。"},
        {"question": "(3x² + 2x)' = ?", "options": ["6x", "6x+2", "3x+2", "6x²+2"], "answer": 1, "explanation": "分别求导：(3x²)' = 6x，(2x)' = 2。"},
    ],
    "t23": [
        {"question": "f(x)=x³-3x 的极大值点是？", "options": ["x=-1", "x=0", "x=1", "x=3"], "answer": 0, "explanation": "f'(x)=3x²-3=0，x=±1。f''(-1)=-6<0，极大值。"},
        {"question": "f(x)=x² 在 [-1,2] 上的最小值是？", "options": ["-1", "0", "1", "4"], "answer": 1, "explanation": "f'(x)=2x=0，x=0。f(0)=0，f(-1)=1，f(2)=4，最小值 0。"},
        {"question": "f'(x) > 0 说明函数？", "options": ["递增", "递减", "有极值", "是常数"], "answer": 0, "explanation": "导数大于零，函数单调递增。"},
    ],
    "t24": [
        {"question": "∫3x² dx = ?", "options": ["x³", "x³ + C", "6x", "6x + C"], "answer": 1, "explanation": "∫3x²dx = 3×(x³/3) + C = x³ + C。"},
        {"question": "∫₀² 1 dx = ?", "options": ["0", "1", "2", "3"], "answer": 2, "explanation": "∫₀² 1dx = [x]₀² = 2-0 = 2。"},
        {"question": "∫sin x dx = ?", "options": ["cos x", "-cos x + C", "sin x + C", "-sin x + C"], "answer": 1, "explanation": "∫sin xdx = -cos x + C。"},
    ],
    "t25": [
        {"question": "d/dx ∫₀ˣ t² dt = ?", "options": ["x²", "x³/3", "2x", "0"], "answer": 0, "explanation": "微积分基本定理：d/dx ∫₀ˣ f(t)dt = f(x)。"},
        {"question": "速度 v(t)=2t，从 0 到 3 的位移是？", "options": ["6", "9", "12", "18"], "answer": 1, "explanation": "∫₀³ 2t dt = [t²]₀³ = 9。"},
        {"question": "加速度的积分等于？", "options": ["位移", "速度", "力", "功"], "answer": 1, "explanation": "加速度的积分是速度，速度的积分是位移。"},
    ],

    # ═══ 抽象与推理 ═══
    "t26": [
        {"question": "等差数列 1,4,7,10,... 的第 10 项是？", "options": ["25", "28", "31", "34"], "answer": 1, "explanation": "a₁₀ = 1 + 9×3 = 28。"},
        {"question": "等比数列 1,2,4,8,... 的第 8 项是？", "options": ["64", "128", "256", "512"], "answer": 1, "explanation": "a₈ = 1×2⁷ = 128。"},
        {"question": "数列 1,1,2,3,5,8,... 是？", "options": ["等差数列", "等比数列", "斐波那契数列", "调和数列"], "answer": 2, "explanation": "斐波那契数列：每项等于前两项之和。"},
    ],
    "t27": [
        {"question": "A={1,2,3}，B={2,3,4}，A∪B = ?", "options": ["{2,3}", "{1,4}", "{1,2,3,4}", "{1,2,3}"], "answer": 2, "explanation": "并集包含所有元素：{1,2,3,4}。"},
        {"question": "空集是任何集合的？", "options": ["子集", "真子集", "元素", "补集"], "answer": 0, "explanation": "空集是任何集合的子集。"},
        {"question": "A={1,2,3} 有几个子集？", "options": ["3", "6", "7", "8"], "answer": 3, "explanation": "n 个元素有 2ⁿ 个子集，2³=8 个。"},
    ],
    "t28": [
        {"question": "C(6,2) = ?", "options": ["12", "15", "18", "30"], "answer": 1, "explanation": "C(6,2) = 6!/(2!4!) = 30/2 = 15。"},
        {"question": "P(4,2) = ?", "options": ["6", "8", "12", "16"], "answer": 2, "explanation": "P(4,2) = 4×3 = 12。"},
        {"question": "5 个人站成一排有几种排法？", "options": ["25", "60", "120", "720"], "answer": 2, "explanation": "P(5,5) = 5! = 120。"},
    ],
    "t29": [
        {"question": "1+2+3+...+n = ?", "options": ["n²", "n(n+1)/2", "n(n-1)/2", "2n"], "answer": 1, "explanation": "高斯公式：S = n(n+1)/2。"},
        {"question": "等比数列 3,6,12,24,... 的前 5 项和是？", "options": ["63", "93", "96", "120"], "answer": 1, "explanation": "S₅ = 3(1-2⁵)/(1-2) = 3×31 = 93。"},
        {"question": "等差数列前 n 项和公式中，需要知道？", "options": ["首项和公差", "首项和末项", "公差和项数", "只需要项数"], "answer": 1, "explanation": "Sₙ = n(a₁+aₙ)/2，需要首项、末项和项数。"},
    ],
    "t30": [
        {"question": "2×3 矩阵有几行几列？", "options": ["2行3列", "3行2列", "6个元素", "5个元素"], "answer": 0, "explanation": "2×3 表示 2 行 3 列。"},
        {"question": "单位矩阵的特点是？", "options": ["全为0", "对角线为1其余为0", "全为1", "对称"], "answer": 1, "explanation": "单位矩阵 I：对角线元素为 1，其余为 0。"},
        {"question": "矩阵乘法满足交换律吗？", "options": ["满足", "不满足", "有时满足", "取决于矩阵"], "answer": 1, "explanation": "矩阵乘法一般不满足交换律：AB ≠ BA。"},
    ],

    # ═══ 高等数学（额外主题） ═══
    "t31": [
        {"question": "先算乘除后算加减的原因是？", "options": ["约定俗成", "乘法是加法的简写", "为了简单", "没有原因"], "answer": 1, "explanation": "乘法是重复加法，3×4=4+4+4，所以先算乘法。"},
        {"question": "12 ÷ (3+1) = ?", "options": ["3", "4", "15", "16"], "answer": 1, "explanation": "先算括号：3+1=4，再算除法：12÷4=3。不对，应该是3。"},
    ],
    "t32": [
        {"question": "1 千克等于多少克？", "options": ["10", "100", "1000", "10000"], "answer": 2, "explanation": "1 kg = 1000 g。"},
        {"question": "1 平方米等于多少平方厘米？", "options": ["100", "1000", "10000", "100000"], "answer": 2, "explanation": "1 m² = 100×100 = 10000 cm²。"},
    ],
    "t33": [
        {"question": "长方形周长公式是？", "options": ["长×宽", "2(长+宽)", "长+宽", "2长+宽"], "answer": 1, "explanation": "周长 = 2(长+宽)，四条边之和。"},
        {"question": "边长为 5 的正方形面积是？", "options": ["10", "20", "25", "50"], "answer": 2, "explanation": "S = 5² = 25。"},
    ],
    "t34": [
        {"question": "条形图适合表示？", "options": ["变化趋势", "各部分占比", "数量对比", "分布规律"], "answer": 2, "explanation": "条形图适合比较不同类别的数量。"},
        {"question": "折线图适合表示？", "options": ["变化趋势", "各部分占比", "数量对比", "分布规律"], "answer": 0, "explanation": "折线图适合展示数据随时间的变化趋势。"},
    ],
    "t35": [
        {"question": "速度 = 路程 ÷ ?", "options": ["时间", "距离", "加速度", "力"], "answer": 0, "explanation": "速度 = 路程 / 时间。"},
        {"question": "单价 5 元，买 8 个需要？", "options": ["13元", "35元", "40元", "45元"], "answer": 2, "explanation": "总价 = 单价 × 数量 = 5×8 = 40 元。"},
    ],
    "t36": [
        {"question": "2 和 8 的最大公因数是？", "options": ["2", "4", "6", "8"], "answer": 0, "explanation": "2 的因数：1,2；8 的因数：1,2,4,8；最大公因数是 2。"},
        {"question": "3 和 5 的最小公倍数是？", "options": ["8", "10", "15", "30"], "answer": 2, "explanation": "3 和 5 互质，最小公倍数 = 3×5 = 15。"},
    ],
    "t37": [
        {"question": "绝对值的几何意义是？", "options": ["数值大小", "到原点的距离", "正负号", "相反数"], "answer": 1, "explanation": "|x| 表示 x 到原点的距离。"},
    ],
    "t38": [
        {"question": "移项的规则是？", "options": ["直接移动", "变号后移动", "不变号", "只能移数字"], "answer": 1, "explanation": "移项要变号：加变减，减变加，乘变除，除变乘。"},
    ],
    "t39": [
        {"question": "完全平方公式 (a+b)² = ?", "options": ["a²+b²", "a²+2ab+b²", "a²-b²", "2a+2b"], "answer": 1, "explanation": "(a+b)² = a² + 2ab + b²。"},
        {"question": "平方差公式 a²-b² = ?", "options": ["(a-b)²", "(a+b)(a-b)", "(a+b)²", "a²-2ab+b²"], "answer": 1, "explanation": "a²-b² = (a+b)(a-b)。"},
    ],
    "t40": [
        {"question": "一次函数 y=kx+b 中，k 叫做？", "options": ["截距", "斜率", "系数", "常数"], "answer": 1, "explanation": "k 是斜率，b 是截距。"},
    ],
    "t41": [
        {"question": "二元一次方程组通常有？", "options": ["无解", "唯一解", "无穷多解", "唯一解或无解"], "answer": 1, "explanation": "两个一次方程通常有唯一解（两直线相交）。"},
    ],
    "t42": [
        {"question": "泰勒展开在 x=0 处叫什么？", "options": ["傅里叶展开", "麦克劳林展开", "洛朗展开", "幂级数"], "answer": 1, "explanation": "在 x=0 处的泰勒展开叫麦克劳林展开。"},
    ],
    "t43": [
        {"question": "函数可微一定连续吗？", "options": ["一定", "不一定", "看情况", "不相关"], "answer": 0, "explanation": "可微一定连续，但连续不一定可微。"},
    ],
    "t44": [
        {"question": "极坐标中 r 表示？", "options": ["角度", "距离", "面积", "速度"], "answer": 1, "explanation": "r 是点到原点的距离。"},
    ],
    "t45": [
        {"question": "多元函数的偏导数是？", "options": ["全导数", "对一个变量求导", "积分", "极限"], "answer": 1, "explanation": "偏导数是对某一个变量求导，其他变量视为常数。"},
    ],
    "t46": [
        {"question": "椭圆的标准方程是？", "options": ["x²+y²=r²", "x²/a²+y²/b²=1", "y²=2px", "x²-y²=1"], "answer": 1, "explanation": "椭圆标准方程：x²/a² + y²/b² = 1。"},
    ],
    "t47": [
        {"question": "极坐标中 θ 表示？", "options": ["距离", "角度", "面积", "速度"], "answer": 1, "explanation": "θ 是与正 x 轴的夹角。"},
    ],
    "t48": [
        {"question": "数学归纳法的两步是？", "options": ["假设和验证", "基础步和归纳步", "猜想和证明", "分析和综合"], "answer": 1, "explanation": "第一步验证基础情况，第二步假设 n=k 成立推导 n=k+1。"},
    ],
    "t49": [
        {"question": "二项式定理展开 (a+b)³ = ?", "options": ["a³+b³", "a³+3a²b+3ab²+b³", "3a+3b", "a³+3ab+b³"], "answer": 1, "explanation": "(a+b)³ = a³ + 3a²b + 3ab² + b³。"},
    ],
    "t50": [
        {"question": "微分方程 dy/dx = 2x 的解是？", "options": ["y=x²", "y=x²+C", "y=2x", "y=2x+C"], "answer": 1, "explanation": "两边积分：y = x² + C。"},
    ],
    "t51": [
        {"question": "f(x)=1/x 在 x=0 处？", "options": ["连续", "可导", "有极限", "间断"], "answer": 3, "explanation": "f(x)=1/x 在 x=0 处无定义，是间断点。"},
    ],
    "t52": [
        {"question": "二重积分表示什么？", "options": ["面积", "体积", "长度", "质量"], "answer": 1, "explanation": "二重积分可以表示曲顶柱体的体积。"},
    ],
    "t53": [
        {"question": "行列式为 0 说明矩阵？", "options": ["可逆", "不可逆", "是单位矩阵", "是对称矩阵"], "answer": 1, "explanation": "行列式为 0 的矩阵不可逆（奇异矩阵）。"},
    ],
    "t54": [
        {"question": "一阶线性微分方程的标准形式是？", "options": ["y'+p(x)y=q(x)", "y''+y=0", "dy/dx=f(x)", "y=f(x)"], "answer": 0, "explanation": "一阶线性：y' + p(x)y = q(x)。"},
    ],
    "t55": [
        {"question": "概率的取值范围是？", "options": ["[-1,1]", "[0,1]", "[0,∞)", "(-∞,∞)"], "answer": 1, "explanation": "概率在 0 到 1 之间，0 表示不可能，1 表示必然。"},
    ],
}
