"""
重要定理/概念的推导过程补充
为关键主题添加从第一性原理出发的推导步骤

主题 ID 映射（seed_data.py）：
t1:自然数  t2:加法乘法  t3:减法除法  t4:分数  t5:小数百分数
t6:负数  t7:整式多项式  t8:一元一次方程  t9:不等式  t10:方程组
t11:点线面  t12:角与平行  t13:三角形  t14:四边形多边形  t15:圆
t16:变量与函数  t17:一次函数  t18:二次函数  t19:指数对数  t20:三角函数
t21:斜率  t22:导数  t23:导数应用  t24:积分  t25:微积分基本定理
t26:数列  t27:集合  t28:排列组合  t29:数列求和  t30:矩阵
"""

DERIVE_SECTIONS = {
    # ═══ 数的起源 ═══
    "t4": [  # 分数
        {"type": "title", "content": "推导：为什么 1/2 = 2/4 = 3/6？"},
        {"type": "text", "content": "等价分数的原理来自乘法的本质。让我们从头推导："},
        {"type": "formula", "content": "1/2 表示：把 1 分成 2 份，取 1 份"},
        {"type": "text", "content": "现在把每一份再分成 2 份，总共分成 4 份。原来取的 1 份也变成 2 份："},
        {"type": "formula", "content": "1/2 = (1×2)/(2×2) = 2/4"},
        {"type": "text", "content": "一般地，分子分母同乘一个非零数，分数值不变："},
        {"type": "formula", "content": "a/b = (a×n)/(b×n)，其中 n ≠ 0"},
        {"type": "highlight", "content": "本质：分子分母同乘同除，相当于乘以 1（因为 n/n = 1），值不变。"},
        {"type": "ex", "content": "<b>应用：</b>通分就是利用这个原理。计算 1/3 + 1/4：\n1/3 = 4/12，1/4 = 3/12\n4/12 + 3/12 = 7/12"}
    ],
    "t5": [  # 小数与百分数
        {"type": "title", "content": "推导：小数与分数的关系"},
        {"type": "text", "content": "小数本质上是分母为 10 的幂的分数。让我们推导："},
        {"type": "formula", "content": "0.1 = 1/10\n0.01 = 1/100\n0.001 = 1/1000"},
        {"type": "text", "content": "所以 0.375 = 375/1000。化简这个分数："},
        {"type": "formula", "content": "375/1000 = (375÷125)/(1000÷125) = 3/8"},
        {"type": "highlight", "content": "有限小数一定能化成分数（分母是 10 的幂的因数）。\n无限循环小数也能化成分数，如 0.333... = 1/3。"},
        {"type": "ex", "content": "<b>推导 0.999... = 1：</b>\n设 x = 0.999...\n则 10x = 9.999...\n10x - x = 9.999... - 0.999...\n9x = 9\nx = 1"}
    ],

    # ═══ 代数语言 ═══
    "t7": [  # 整式与多项式 — 分配律推导
        {"type": "title", "content": "推导：分配律为什么成立？"},
        {"type": "text", "content": "分配律 a×(b+c) = a×b + a×c 不是规定，而是可以证明的。"},
        {"type": "text", "content": "用面积模型来推导。想象一个矩形，长为 a，宽为 (b+c)："},
        {"type": "formula", "content": "整个矩形面积 = a × (b+c)"},
        {"type": "text", "content": "把它切成两块：一块宽 b，一块宽 c："},
        {"type": "formula", "content": "第一块面积 = a × b\n第二块面积 = a × c\n总面积 = a×b + a×c"},
        {"type": "highlight", "content": "因为切开前后的总面积不变，所以 a×(b+c) = a×b + a×c"},
        {"type": "ex", "content": "<b>例：</b>7 × 12 = 7 × (10+2) = 70 + 14 = 84\n这就是心算的数学原理！"}
    ],
    "t8": [  # 一元一次方程 — 等式性质推导
        {"type": "title", "content": "推导：等式的基本性质"},
        {"type": "text", "content": "解方程的依据是等式的两条基本性质。让我们从天平模型推导："},
        {"type": "highlight", "content": "天平原理：两边同时加减相同重量，天平仍然平衡"},
        {"type": "text", "content": "性质 1：等式两边同时加减同一个数，等式仍然成立"},
        {"type": "formula", "content": "如果 a = b，那么 a + c = b + c，a - c = b - c"},
        {"type": "text", "content": "性质 2：等式两边同时乘除同一个非零数，等式仍然成立"},
        {"type": "formula", "content": "如果 a = b，那么 a×c = b×c，a/c = b/c（c ≠ 0）"},
        {"type": "ex", "content": "<b>推导解方程 2x + 3 = 7：</b>\n2x + 3 = 7\n2x + 3 - 3 = 7 - 3（性质1：两边减3）\n2x = 4\n2x/2 = 4/2（性质2：两边除以2）\nx = 2"}
    ],
    "t9": [  # 不等式 — 不等式运算规则推导
        {"type": "title", "content": "推导：不等式的运算规则"},
        {"type": "text", "content": "不等式和等式类似，但有一个关键区别。让我们推导："},
        {"type": "formula", "content": "如果 a > b，那么：\n① a + c > b + c（两边加相同数，方向不变）\n② a - c > b - c（两边减相同数，方向不变）"},
        {"type": "text", "content": "乘法的情况需要注意："},
        {"type": "formula", "content": "如果 a > b 且 c > 0：a×c > b×c（方向不变）\n如果 a > b 且 c < 0：a×c < b×c（方向反转！）"},
        {"type": "highlight", "content": "关键：乘以负数时，不等号方向反转。\n因为负数在数轴上是「反方向」的。"},
        {"type": "ex", "content": "<b>推导：</b>3 > 2，两边乘以 -1：\n3×(-1) = -3，2×(-1) = -2\n-3 < -2，方向反转了！"}
    ],

    # ═══ 几何直觉 ═══
    "t13": [  # 三角形 — 勾股定理证明
        {"type": "title", "content": "推导：勾股定理的证明"},
        {"type": "text", "content": "勾股定理：直角三角形中，a² + b² = c²。这不是规定，是可以证明的！"},
        {"type": "text", "content": "用「面积法」证明。构造一个大正方形，边长为 (a+b)："},
        {"type": "formula", "content": "大正方形面积 = (a+b)² = a² + 2ab + b²"},
        {"type": "text", "content": "大正方形内部有 4 个直角三角形和 1 个小正方形："},
        {"type": "formula", "content": "4 个三角形面积 = 4 × (ab/2) = 2ab\n小正方形面积 = c²"},
        {"type": "text", "content": "两种方式计算的面积应该相等："},
        {"type": "formula", "content": "a² + 2ab + b² = 2ab + c²\na² + b² = c²"},
        {"type": "highlight", "content": "证毕！这就是为什么 3² + 4² = 5²：9 + 16 = 25 ✓"},
        {"type": "ex", "content": "<b>应用：</b>两点距离公式就是勾股定理的直接应用。\n点 (x₁,y₁) 到 (x₂,y₂) 的距离：\nd = √[(x₂-x₁)² + (y₂-y₁)²]"}
    ],
    "t15": [  # 圆 — 周长和面积公式推导
        {"type": "title", "content": "推导：圆的周长和面积公式"},
        {"type": "text", "content": "圆的周长 C = 2πr，面积 A = πr²。π 是怎么来的？"},
        {"type": "text", "content": "古人用「割圆术」推导：在圆内接正多边形，边数越多越接近圆。"},
        {"type": "formula", "content": "正六边形周长 = 6r（边长 = r）\n正十二边形周长 ≈ 6.21r\n正二十四边形周长 ≈ 6.27r\n...\n边数→∞ 时，周长→2πr"},
        {"type": "text", "content": "其中 π ≈ 3.14159... 是一个无理数，表示圆周长与直径的比值。"},
        {"type": "highlight", "content": "π = C/d = C/(2r)，所以 C = 2πr"},
        {"type": "ex", "content": "<b>面积推导（割圆术思想）：</b>\n把圆切成 n 个扇形，拼成近似长方形：\n长 ≈ 半个周长 = πr\n宽 ≈ 半径 = r\n面积 ≈ πr × r = πr²\nn→∞ 时精确相等。"}
    ],

    # ═══ 函数世界 ═══
    "t16": [  # 变量与函数 — 函数本质推导
        {"type": "title", "content": "推导：函数的本质"},
        {"type": "text", "content": "函数不是「神秘的规则」，而是一种对应关系。让我们从第一性原理理解："},
        {"type": "highlight", "content": "函数的本质：给定一个输入 x，有且只有一个输出 y"},
        {"type": "text", "content": "为什么 y = x² 是函数，而 x² + y² = 1 不是？"},
        {"type": "formula", "content": "y = x²：给定 x=2，y 只能是 4（唯一确定）\nx² + y² = 1：给定 x=0，y 可以是 1 或 -1（不唯一）"},
        {"type": "text", "content": "判断是否是函数的方法——垂直线检验："},
        {"type": "ex", "content": "<b>垂直线检验：</b>如果一条竖线与图像有多个交点，就不是函数。\n因为同一个 x 对应了多个 y，违反了函数的定义。"}
    ],
    "t18": [  # 二次函数 — 顶点公式推导
        {"type": "title", "content": "推导：二次函数顶点公式"},
        {"type": "text", "content": "y = ax² + bx + c 的顶点坐标公式怎么推导？用「配方法」："},
        {"type": "formula", "content": "y = ax² + bx + c"},
        {"type": "text", "content": "第一步：提取 a"},
        {"type": "formula", "content": "y = a(x² + b/a·x) + c"},
        {"type": "text", "content": "第二步：配方（凑完全平方）"},
        {"type": "formula", "content": "x² + b/a·x = (x + b/2a)² - b²/4a²"},
        {"type": "text", "content": "第三步：代入整理"},
        {"type": "formula", "content": "y = a(x + b/2a)² - b²/4a + c\ny = a(x + b/2a)² + (4ac-b²)/4a"},
        {"type": "highlight", "content": "顶点坐标：(-b/2a, (4ac-b²)/4a)\n简化记忆：x_顶点 = -b/2a"},
        {"type": "ex", "content": "<b>例：</b>y = x² - 4x + 3\nx_顶点 = -(-4)/(2×1) = 2\ny_顶点 = (4×1×3-16)/4 = -1\n顶点：(2, -1)"}
    ],
    "t19": [  # 指数与对数 — 对数法则推导
        {"type": "title", "content": "推导：对数的运算法则"},
        {"type": "text", "content": "对数是指数的逆运算。从指数法则推导对数法则："},
        {"type": "formula", "content": "指数法则：aᵐ × aⁿ = aᵐ⁺ⁿ"},
        {"type": "text", "content": "设 aᵐ = M，aⁿ = N，则 m = log_a(M)，n = log_a(N)："},
        {"type": "formula", "content": "M × N = aᵐ × aⁿ = aᵐ⁺ⁿ\nlog_a(M×N) = m + n = log_a(M) + log_a(N)"},
        {"type": "highlight", "content": "对数加法法则：log(M×N) = log(M) + log(N)\n对数减法法则：log(M/N) = log(M) - log(N)\n对数幂法则：log(Mⁿ) = n·log(M)"},
        {"type": "ex", "content": "<b>应用：</b>这就是计算尺的原理！\n乘法变加法，除法变减法，大大简化了计算。"}
    ],

    # ═══ 变化的科学 ═══
    "t21": [  # 斜率 — 斜率公式推导
        {"type": "title", "content": "推导：斜率公式"},
        {"type": "text", "content": "斜率描述直线的「陡峭程度」。怎么量化它？"},
        {"type": "text", "content": "从「变化率」的角度推导。取直线上两点 (x₁,y₁) 和 (x₂,y₂)："},
        {"type": "formula", "content": "水平变化量 = x₂ - x₁ = Δx\n垂直变化量 = y₂ - y₁ = Δy"},
        {"type": "text", "content": "斜率 = 垂直变化 ÷ 水平变化："},
        {"type": "formula", "content": "k = Δy/Δx = (y₂-y₁)/(x₂-x₁)"},
        {"type": "highlight", "content": "本质：斜率是「y 随 x 变化的速率」\nk > 0：向右上方倾斜\nk < 0：向右下方倾斜\nk = 0：水平线"},
        {"type": "ex", "content": "<b>推导直线方程：</b>\n已知斜率 k 和一个点 (x₀,y₀)：\n(y-y₀)/(x-x₀) = k\ny - y₀ = k(x-x₀)\ny = kx + (y₀-kx₀)\n这就是 y = kx + b 的来源！"}
    ],
    "t22": [  # 导数 — 导数定义推导
        {"type": "title", "content": "推导：导数的定义"},
        {"type": "text", "content": "导数回答的问题是：「在某一瞬间，变化有多快？」"},
        {"type": "text", "content": "从平均变化率出发推导。函数 f(x) 在区间 [x, x+h] 上的平均变化率："},
        {"type": "formula", "content": "平均变化率 = [f(x+h) - f(x)] / h"},
        {"type": "text", "content": "当 h 越来越小（趋于 0），平均变化率趋于瞬时变化率："},
        {"type": "formula", "content": "f'(x) = lim(h→0) [f(x+h) - f(x)] / h"},
        {"type": "text", "content": "用这个定义推导 f(x) = x² 的导数："},
        {"type": "formula", "content": "f'(x) = lim(h→0) [(x+h)² - x²] / h\n= lim(h→0) [x² + 2xh + h² - x²] / h\n= lim(h→0) [2xh + h²] / h\n= lim(h→0) (2x + h)\n= 2x"},
        {"type": "highlight", "content": "几何意义：f'(x) 是曲线 y=f(x) 在点 x 处的切线斜率。\n物理意义：如果 f(t) 是位移，f'(t) 就是速度。"},
        {"type": "ex", "content": "<b>用定义推导常用导数：</b>\n(x³)' = 3x²\n(xⁿ)' = nxⁿ⁻¹（幂函数求导公式）\n(sinx)' = cosx\n(eˣ)' = eˣ"}
    ],
    "t24": [  # 积分 — 定积分定义推导
        {"type": "title", "content": "推导：定积分的定义"},
        {"type": "text", "content": "定积分回答的问题是：「曲线下的面积是多少？」"},
        {"type": "text", "content": "用「分割-求和-取极限」的方法推导："},
        {"type": "formula", "content": "把 [a,b] 分成 n 个小区间，每个宽度 Δx = (b-a)/n"},
        {"type": "text", "content": "每个小区间上取一个点 xᵢ，用矩形近似："},
        {"type": "formula", "content": "第 i 个矩形面积 = f(xᵢ) × Δx\n总面积 ≈ Σ f(xᵢ) × Δx"},
        {"type": "text", "content": "当 n→∞ 时，近似变成精确："},
        {"type": "formula", "content": "∫ₐᵇ f(x)dx = lim(n→∞) Σ f(xᵢ) × Δx"},
        {"type": "text", "content": "牛顿-莱布尼茨公式（微积分基本定理）的推导："},
        {"type": "formula", "content": "如果 F'(x) = f(x)，那么：\n∫ₐᵇ f(x)dx = F(b) - F(a)"},
        {"type": "highlight", "content": "本质：积分和导数是互逆运算。\n导数：从整体求瞬间变化率\n积分：从瞬间变化率求整体"},
        {"type": "ex", "content": "<b>例：</b>∫₀¹ x² dx = [x³/3]₀¹ = 1/3 - 0 = 1/3\n几何意义：y=x² 在 [0,1] 下的面积是 1/3。"}
    ],

    # ═══ 抽象与推理 ═══
    "t26": [  # 数列 — 等差等比公式推导
        {"type": "title", "content": "推导：等差数列和等比数列公式"},
        {"type": "text", "content": "等差数列：每一项比前一项多一个固定值 d（公差）"},
        {"type": "formula", "content": "a₁, a₁+d, a₁+2d, ...\n通项公式：aₙ = a₁ + (n-1)d"},
        {"type": "text", "content": "推导前 n 项和 Sₙ。用「倒序相加法」："},
        {"type": "formula", "content": "Sₙ = a₁ + (a₁+d) + ... + aₙ\nSₙ = aₙ + (aₙ-d) + ... + a₁\n两式相加：2Sₙ = n(a₁+aₙ)\nSₙ = n(a₁+aₙ)/2"},
        {"type": "text", "content": "等比数列：每一项是前一项的 r 倍（公比）"},
        {"type": "formula", "content": "a₁, a₁r, a₁r², ...\n通项公式：aₙ = a₁ × rⁿ⁻¹"},
        {"type": "text", "content": "推导前 n 项和。用「错位相减法」："},
        {"type": "formula", "content": "Sₙ = a₁ + a₁r + a₁r² + ... + a₁rⁿ⁻¹\nrSₙ = a₁r + a₁r² + ... + a₁rⁿ\nSₙ - rSₙ = a₁ - a₁rⁿ\nSₙ(1-r) = a₁(1-rⁿ)\nSₙ = a₁(1-rⁿ)/(1-r)"},
        {"type": "ex", "content": "<b>例：</b>等比数列 2, 6, 18, 54, ...\na₁=2, r=3, S₅ = 2(1-3⁵)/(1-3) = 2×242/2 = 242"}
    ],
    "t28": [  # 排列组合 — 公式推导
        {"type": "title", "content": "推导：排列和组合公式"},
        {"type": "text", "content": "排列和组合的区别在于「顺序是否重要」。从乘法原理推导："},
        {"type": "formula", "content": "乘法原理：如果做一件事有 m 种方法，做另一件事有 n 种方法，\n那么两件事一起做有 m×n 种方法"},
        {"type": "text", "content": "推导排列数 P(n,r)——从 n 个中取 r 个排列："},
        {"type": "formula", "content": "第 1 个位置：n 种选择\n第 2 个位置：n-1 种选择\n...\n第 r 个位置：n-r+1 种选择\nP(n,r) = n×(n-1)×...×(n-r+1) = n!/(n-r)!"},
        {"type": "text", "content": "组合数 C(n,r)——从 n 个中取 r 个（不考虑顺序）："},
        {"type": "formula", "content": "每种组合有 r! 种排列方式\nC(n,r) = P(n,r) / r! = n! / [r!(n-r)!]"},
        {"type": "highlight", "content": "排列 = 先选再排序\n组合 = 只选不排序\n组合数 = 排列数 ÷ r!"},
        {"type": "ex", "content": "<b>例：</b>从 5 人中选 3 人\n排列（有序）：P(5,3) = 5×4×3 = 60\n组合（无序）：C(5,3) = 60/6 = 10"}
    ],

    # ═══ 高等数学（额外主题） ═══
    "t42": [  # 函数世界阶段 — 泰勒展开
        {"type": "title", "content": "推导：泰勒展开的原理"},
        {"type": "text", "content": "泰勒展开的核心思想：用多项式逼近任意函数。怎么做到的？"},
        {"type": "text", "content": "假设 f(x) 可以写成多项式形式："},
        {"type": "formula", "content": "f(x) = a₀ + a₁x + a₂x² + a₃x³ + ..."},
        {"type": "text", "content": "令 x=0，求各系数："},
        {"type": "formula", "content": "f(0) = a₀\nf'(0) = a₁\nf''(0) = 2a₂ → a₂ = f''(0)/2!\nf'''(0) = 6a₃ → a₃ = f'''(0)/3!\n一般地：aₙ = f⁽ⁿ⁾(0)/n!"},
        {"type": "text", "content": "所以泰勒展开（在 x=0 处，即麦克劳林展开）为："},
        {"type": "formula", "content": "f(x) = f(0) + f'(0)x + f''(0)x²/2! + f'''(0)x³/3! + ...\nf(x) = Σ f⁽ⁿ⁾(0) × xⁿ/n!"},
        {"type": "highlight", "content": "本质：泰勒展开用函数在某一点的所有导数信息，\n重建出整个函数。就像用 DNA 还原整个生物体。"},
        {"type": "ex", "content": "<b>推导 eˣ 的泰勒展开：</b>\nf(x)=eˣ，f⁽ⁿ⁾(0)=1 对所有 n\n所以 eˣ = 1 + x + x²/2! + x³/3! + ...\n代入 x=1：e = 1+1+1/2+1/6+1/24+... ≈ 2.718"}
    ],
    "t50": [  # 高等数学 — 微分方程分离变量法
        {"type": "title", "content": "推导：分离变量法"},
        {"type": "text", "content": "微分方程包含未知函数及其导数。最简单的类型是可以「分离变量」的："},
        {"type": "formula", "content": "一般形式：dy/dx = f(x) × g(y)"},
        {"type": "text", "content": "关键技巧：把 y 和 x 分到等式两边："},
        {"type": "formula", "content": "dy/g(y) = f(x)dx"},
        {"type": "text", "content": "两边同时积分："},
        {"type": "formula", "content": "∫ dy/g(y) = ∫ f(x)dx + C"},
        {"type": "ex", "content": "<b>例：解 dy/dx = xy</b>\ndy/y = x dx\n∫dy/y = ∫x dx\nln|y| = x²/2 + C\ny = Ae^(x²/2) （A = ±eᶜ）"}
    ],
}
