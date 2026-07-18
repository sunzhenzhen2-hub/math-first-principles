"""新增 25 个主题种子数据 — 从小学到大学完整数学路径"""
import json

EXTRA_TOPICS = [
    # ═══════════════════════════════════════════
    # 小学补充（阶段0，+6 个）
    # ═══════════════════════════════════════════
    {
        "id": "t31", "stage": "数的起源", "stage_index": 0,
        "icon": "🔣", "title": "运算顺序", "description": "先乘除后加减，括号最优先", "sort_order": 31,
        "lesson": [
            {"type": "title", "content": "为什么需要运算顺序"},
            {"type": "text", "content": "同一个算式，不同的人可能算出不同的结果。比如 2 + 3 × 4，有人算 20，有人算 14。为了避免混乱，数学规定了统一的运算顺序。"},
            {"type": "highlight", "content": "运算顺序口诀：先乘除，后加减，有括号先算括号里面"},
            {"type": "title", "content": "运算顺序规则"},
            {"type": "text", "content": "第一级：括号（）内的运算最优先\n第二级：乘法和除法（从左到右）\n第三级：加法和减法（从左到右）"},
            {"type": "formula", "content": "2 + 3 × 4 = 2 + 12 = 14（先算乘法）\n(2 + 3) × 4 = 5 × 4 = 20（先算括号）"},
            {"type": "ex", "content": "<b>例：</b>计算 12 - 4 × 2 + 6 ÷ 3\n= 12 - 8 + 2（先算乘除）\n= 4 + 2（从左到右算加减）\n= 6"},
            {"type": "title", "content": "嵌套括号"},
            {"type": "text", "content": "当有多层括号时，从最内层开始算。"},
            {"type": "formula", "content": "小括号 () → 中括号 [] → 大括号 {}"},
            {"type": "ex", "content": "<b>例：</b>2 × [3 + (4 - 1)] = 2 × [3 + 3] = 2 × 6 = 12"}
        ],
        "quiz": [
            {"question": "8 + 2 × 5 = ?", "options": ["50", "18", "28", "10"], "answer": 1, "explanation": "先算乘法：2×5=10，再算加法：8+10=18。"},
            {"question": "(6 + 4) ÷ 2 = ?", "options": ["8", "7", "5", "14"], "answer": 2, "explanation": "先算括号：6+4=10，再算除法：10÷2=5。"},
            {"question": "12 ÷ 3 × 2 = ?", "options": ["2", "12", "8", "6"], "answer": 2, "explanation": "乘除同级，从左到右：12÷3=4，4×2=8。"}
        ]
    },
    {
        "id": "t32", "stage": "数的起源", "stage_index": 0,
        "icon": "📏", "title": "度量与单位", "description": "长度、面积、体积、时间的度量", "sort_order": 32,
        "lesson": [
            {"type": "title", "content": "为什么要度量"},
            {"type": "text", "content": "度量是用一个标准量去比较另一个量。没有度量，就无法精确描述「多长」「多重」「多久」。"},
            {"type": "highlight", "content": "度量的本质：选定一个单位，看目标量包含多少个单位"},
            {"type": "title", "content": "长度单位"},
            {"type": "text", "content": "千米(km) → 米(m) → 分米(dm) → 厘米(cm) → 毫米(mm)"},
            {"type": "formula", "content": "1 km = 1000 m\n1 m = 10 dm = 100 cm = 1000 mm\n1 cm = 10 mm"},
            {"type": "title", "content": "面积与体积"},
            {"type": "text", "content": "面积是二维空间的大小，体积是三维空间的大小。"},
            {"type": "formula", "content": "面积：1 m² = 10000 cm²\n体积：1 m³ = 1000000 cm³\n容积：1 L = 1000 mL，1 mL = 1 cm³"},
            {"type": "title", "content": "时间单位"},
            {"type": "formula", "content": "1 天 = 24 小时\n1 小时 = 60 分钟\n1 分钟 = 60 秒"},
            {"type": "ex", "content": "<b>例：</b>1.5 小时 = 1 小时 30 分钟 = 90 分钟 = 5400 秒"}
        ],
        "quiz": [
            {"question": "1 米等于多少厘米？", "options": ["10", "100", "1000", "10000"], "answer": 1, "explanation": "1 m = 100 cm。"},
            {"question": "1 升等于多少毫升？", "options": ["10", "100", "1000", "10000"], "answer": 2, "explanation": "1 L = 1000 mL。"},
            {"question": "2.5 小时等于多少分钟？", "options": ["120", "130", "150", "250"], "answer": 2, "explanation": "2.5 × 60 = 150 分钟。"}
        ]
    },
    {
        "id": "t33", "stage": "数的起源", "stage_index": 0,
        "icon": "📐", "title": "基本图形", "description": "长方形、三角形、圆的周长和面积", "sort_order": 33,
        "lesson": [
            {"type": "title", "content": "长方形和正方形"},
            {"type": "formula", "content": "长方形周长 = 2 × (长 + 宽)\n长方形面积 = 长 × 宽\n正方形面积 = 边长²"},
            {"type": "ex", "content": "<b>例：</b>长 8cm 宽 5cm 的长方形\n周长 = 2×(8+5) = 26 cm\n面积 = 8×5 = 40 cm²"},
            {"type": "title", "content": "三角形"},
            {"type": "formula", "content": "三角形面积 = 底 × 高 ÷ 2"},
            {"type": "ex", "content": "<b>例：</b>底 10cm，高 6cm\n面积 = 10×6÷2 = 30 cm²"},
            {"type": "title", "content": "圆"},
            {"type": "formula", "content": "圆周长 = 2πr = πd\n圆面积 = πr²"},
            {"type": "ex", "content": "<b>例：</b>半径 7cm 的圆\n周长 = 2×π×7 ≈ 44 cm\n面积 = π×49 ≈ 154 cm²"},
            {"type": "highlight", "content": "π ≈ 3.14159... 是圆的周长与直径的比值，是一个无理数"}
        ],
        "quiz": [
            {"question": "边长 6 的正方形面积是？", "options": ["12", "24", "36", "48"], "answer": 2, "explanation": "面积 = 6² = 36。"},
            {"question": "底 8 高 5 的三角形面积是？", "options": ["13", "20", "40", "80"], "answer": 1, "explanation": "面积 = 8×5÷2 = 20。"},
            {"question": "半径 3 的圆面积约是？", "options": ["9", "18.8", "28.3", "37.7"], "answer": 2, "explanation": "面积 = π×9 ≈ 28.3。"}
        ]
    },
    {
        "id": "t34", "stage": "数的起源", "stage_index": 0,
        "icon": "⚖️", "title": "比与比例", "description": "比的概念、正反比例", "sort_order": 34,
        "lesson": [
            {"type": "title", "content": "比的概念"},
            {"type": "text", "content": "比表示两个量之间的倍数关系。a:b 读作「a 比 b」。"},
            {"type": "formula", "content": "a:b = a÷b = a/b\n比的基本性质：比的前项和后项同时乘或除以相同的非零数，比值不变"},
            {"type": "ex", "content": "<b>例：</b>6:4 = 3:2（同除以2）"},
            {"type": "title", "content": "比例"},
            {"type": "text", "content": "比例是两个比相等的式子。"},
            {"type": "formula", "content": "a:b = c:d 等价于 a×d = b×c（内项之积等于外项之积）"},
            {"type": "title", "content": "正比例与反比例"},
            {"type": "highlight", "content": "正比例：y/x = k（定值），y = kx\n反比例：xy = k（定值），y = k/x"},
            {"type": "ex", "content": "<b>正比例例：</b>速度不变时，路程和时间成正比\n<b>反比例例：</b>路程不变时，速度和时间成反比"}
        ],
        "quiz": [
            {"question": "6:9 化简后是？", "options": ["2:3", "3:2", "1:3", "6:9"], "answer": 0, "explanation": "同除以3：6:9 = 2:3。"},
            {"question": "如果 3:4 = 6:x，那么 x = ?", "options": ["6", "8", "10", "12"], "answer": 1, "explanation": "3x = 4×6 = 24，x = 8。"},
            {"question": "速度一定时，路程和时间成什么关系？", "options": ["正比例", "反比例", "没有关系", "不确定"], "answer": 0, "explanation": "速度 = 路程/时间，速度一定时路程/时间 = 定值，正比例。"}
        ]
    },
    {
        "id": "t35", "stage": "数的起源", "stage_index": 0,
        "icon": "📊", "title": "统计图表", "description": "条形图、折线图、扇形图", "sort_order": 35,
        "lesson": [
            {"type": "title", "content": "为什么要用图表"},
            {"type": "text", "content": "图表把数字变成图形，让人一眼看出数据的规律和趋势。"},
            {"type": "title", "content": "条形图"},
            {"type": "text", "content": "用长条的高低表示数量的多少。适合比较不同类别的数据。"},
            {"type": "highlight", "content": "条形图的特点：能清楚看出每个项目的具体数量，便于比较"},
            {"type": "title", "content": "折线图"},
            {"type": "text", "content": "用点和线表示数据的变化趋势。适合表示随时间变化的数据。"},
            {"type": "highlight", "content": "折线图的特点：能清楚看出数据的增减变化趋势"},
            {"type": "title", "content": "扇形图（饼图）"},
            {"type": "text", "content": "用圆的扇形表示各部分占总体的比例。适合表示部分与整体的关系。"},
            {"type": "highlight", "content": "扇形图的特点：能清楚看出各部分占总体的百分比"},
            {"type": "ex", "content": "<b>例：</b>一个班 40 人，喜欢数学的 15 人，语文 12 人，英语 8 人，其他 5 人\n数学占比 = 15/40 = 37.5%"}
        ],
        "quiz": [
            {"question": "想比较各班级人数，用什么图最合适？", "options": ["条形图", "折线图", "扇形图", "都可以"], "answer": 0, "explanation": "比较不同类别数量，条形图最合适。"},
            {"question": "想看某地一年气温变化趋势，用什么图？", "options": ["条形图", "折线图", "扇形图", "表格"], "answer": 1, "explanation": "随时间变化的趋势，折线图最合适。"},
            {"question": "扇形图主要表示什么？", "options": ["数量多少", "变化趋势", "各部分占比", "数据分布"], "answer": 2, "explanation": "扇形图表示各部分占总体的比例关系。"}
        ]
    },
    {
        "id": "t36", "stage": "数的起源", "stage_index": 0,
        "icon": "🧩", "title": "应用题", "description": "行程、工程、鸡兔同笼问题", "sort_order": 36,
        "lesson": [
            {"type": "title", "content": "解应用题的一般步骤"},
            {"type": "text", "content": "① 读题，找出已知条件和问题\n② 设未知数（可以是 x，也可以是具体的量）\n③ 列方程或算式\n④ 求解并检验"},
            {"type": "title", "content": "行程问题"},
            {"type": "highlight", "content": "核心公式：路程 = 速度 × 时间\n相遇问题：路程和 = (速度1 + 速度2) × 时间\n追及问题：路程差 = (速度1 - 速度2) × 时间"},
            {"type": "ex", "content": "<b>例：</b>甲乙两地相距 120km，甲速度 40km/h，乙速度 20km/h，相向而行几小时相遇？\n120 ÷ (40+20) = 2 小时"},
            {"type": "title", "content": "工程问题"},
            {"type": "text", "content": "把总工作量看作「1」，用工作效率（每天完成多少）来解题。"},
            {"type": "ex", "content": "<b>例：</b>甲单独做 10 天完成，乙单独做 15 天完成，合作几天完成？\n甲效率 1/10，乙效率 1/15\n合作效率 1/10 + 1/15 = 5/30 = 1/6\n合作 6 天完成"},
            {"type": "title", "content": "鸡兔同笼"},
            {"type": "text", "content": "经典问题：笼中有鸡和兔，数头有 n 个，数脚有 m 只，求各有几只。"},
            {"type": "ex", "content": "<b>例：</b>鸡兔同笼，头 10 个，脚 28 只\n设兔 x 只，则鸡 (10-x) 只\n4x + 2(10-x) = 28\n2x = 8，x = 4\n兔 4 只，鸡 6 只"}
        ],
        "quiz": [
            {"question": "甲速度 60km/h，乙速度 40km/h，相向而行，2 小时后相距多远？（初始距离 200km）", "options": ["0km", "50km", "100km", "200km"], "answer": 0, "explanation": "(60+40)×2 = 200km，刚好走完全程，相距 0km。"},
            {"question": "甲 5 天完成，乙 10 天完成，合作几天完成？", "options": ["3天", "3.33天", "7.5天", "15天"], "answer": 1, "explanation": "1/5 + 1/10 = 3/10，合作 10/3 ≈ 3.33 天。"},
            {"question": "鸡兔同笼，头 8 个，脚 22 只，兔有几只？", "options": ["2", "3", "4", "5"], "answer": 1, "explanation": "设兔 x：4x + 2(8-x) = 22，2x = 6，x = 3。"}
        ]
    },

    # ═══════════════════════════════════════════
    # 初中补充（阶段1，+5 个）
    # ═══════════════════════════════════════════
    {
        "id": "t37", "stage": "代数语言", "stage_index": 1,
        "icon": "💪", "title": "整数指数幂", "description": "幂运算规则与科学记数法", "sort_order": 37,
        "lesson": [
            {"type": "title", "content": "幂的意义"},
            {"type": "text", "content": "aⁿ 表示 n 个 a 相乘。a 是底数，n 是指数。"},
            {"type": "formula", "content": "a³ = a × a × a\n2⁴ = 2 × 2 × 2 × 2 = 16"},
            {"type": "title", "content": "幂的运算法则"},
            {"type": "formula", "content": "aᵐ × aⁿ = aᵐ⁺ⁿ（同底数幂相乘，指数相加）\naᵐ ÷ aⁿ = aᵐ⁻ⁿ（同底数幂相除，指数相减）\n(aᵐ)ⁿ = aᵐⁿ（幂的乘方，指数相乘）\n(ab)ⁿ = aⁿbⁿ（积的乘方）"},
            {"type": "ex", "content": "<b>例：</b>2³ × 2⁴ = 2⁷ = 128\n3⁵ ÷ 3² = 3³ = 27\n(2³)² = 2⁶ = 64"},
            {"type": "title", "content": "零指数与负整数指数"},
            {"type": "formula", "content": "a⁰ = 1（任何非零数的 0 次幂等于 1）\na⁻ⁿ = 1/aⁿ（负指数 = 正指数的倒数）"},
            {"type": "title", "content": "科学记数法"},
            {"type": "text", "content": "把很大的数或很小的数写成 a × 10ⁿ 的形式（1 ≤ |a| < 10）。"},
            {"type": "formula", "content": "300000 = 3 × 10⁵\n0.00056 = 5.6 × 10⁻⁴"}
        ],
        "quiz": [
            {"question": "2³ × 2² = ?", "options": ["2⁵", "2⁶", "4⁵", "4⁶"], "answer": 0, "explanation": "同底数幂相乘，指数相加：2³ × 2² = 2⁵ = 32。"},
            {"question": "5⁰ = ?", "options": ["0", "1", "5", "无意义"], "answer": 1, "explanation": "任何非零数的 0 次幂等于 1。"},
            {"question": "0.003 用科学记数法表示是？", "options": ["3×10³", "3×10⁻³", "3×10²", "3×10⁻²"], "answer": 1, "explanation": "0.003 = 3 × 10⁻³。"}
        ]
    },
    {
        "id": "t38", "stage": "代数语言", "stage_index": 1,
        "icon": "📐", "title": "一元二次方程", "description": "求根公式、韦达定理", "sort_order": 38,
        "lesson": [
            {"type": "title", "content": "一元二次方程的标准形式"},
            {"type": "formula", "content": "ax² + bx + c = 0（a ≠ 0）"},
            {"type": "title", "content": "求根公式"},
            {"type": "text", "content": "对任意一元二次方程，都可以用求根公式求解。"},
            {"type": "formula", "content": "x = (-b ± √(b²-4ac)) / (2a)"},
            {"type": "title", "content": "判别式"},
            {"type": "formula", "content": "Δ = b² - 4ac\nΔ > 0：两个不相等的实数根\nΔ = 0：两个相等的实数根（一个重根）\nΔ < 0：无实数根（两个共轭复数根）"},
            {"type": "ex", "content": "<b>例：</b>x² - 5x + 6 = 0\nΔ = 25 - 24 = 1 > 0\nx = (5 ± 1) / 2\nx₁ = 3，x₂ = 2"},
            {"type": "title", "content": "韦达定理（根与系数的关系）"},
            {"type": "formula", "content": "x₁ + x₂ = -b/a\nx₁ × x₂ = c/a"},
            {"type": "ex", "content": "<b>例：</b>已知 x₁ + x₂ = 5，x₁ × x₂ = 6\n则方程为 x² - 5x + 6 = 0\n两个根为 2 和 3"}
        ],
        "quiz": [
            {"question": "x² - 4 = 0 的解是？", "options": ["x=2", "x=±2", "x=4", "x=±4"], "answer": 1, "explanation": "x² = 4，x = ±2。"},
            {"question": "x² + 2x + 1 = 0 的判别式 Δ = ?", "options": ["0", "1", "4", "8"], "answer": 0, "explanation": "Δ = 4 - 4 = 0，有两个相等的实根。"},
            {"question": "x₁+x₂=3，x₁×x₂=2，方程是？", "options": ["x²-3x+2=0", "x²+3x+2=0", "x²-3x-2=0", "x²+3x-2=0"], "answer": 0, "explanation": "由韦达定理：x²-(x₁+x₂)x + x₁x₂ = 0，即 x²-3x+2=0。"}
        ]
    },
    {
        "id": "t39", "stage": "代数语言", "stage_index": 1,
        "icon": "√", "title": "根式", "description": "平方根、立方根、化简", "sort_order": 39,
        "lesson": [
            {"type": "title", "content": "平方根"},
            {"type": "text", "content": "如果 x² = a（a ≥ 0），那么 x 叫做 a 的平方根。正数 a 的正平方根记作 √a。"},
            {"type": "formula", "content": "√9 = 3（因为 3² = 9）\n√16 = 4\n√2 ≈ 1.414（无理数）"},
            {"type": "title", "content": "立方根"},
            {"type": "text", "content": "如果 x³ = a，那么 x 叫做 a 的立方根，记作 ∛a。"},
            {"type": "formula", "content": "∛8 = 2（因为 2³ = 8）\n∛(-27) = -3"},
            {"type": "title", "content": "根式的化简"},
            {"type": "formula", "content": "√(ab) = √a × √b\n√(a/b) = √a / √b\n(√a)² = a"},
            {"type": "ex", "content": "<b>例：</b>化简 √50\n= √(25×2)\n= √25 × √2\n= 5√2"},
            {"type": "title", "content": "分母有理化"},
            {"type": "text", "content": "把分母中的根号去掉。方法：分子分母同乘以适当的根式。"},
            {"type": "ex", "content": "<b>例：</b>1/√2 = (1×√2)/(√2×√2) = √2/2"}
        ],
        "quiz": [
            {"question": "√36 = ?", "options": ["4", "6", "8", "18"], "answer": 1, "explanation": "6² = 36，所以 √36 = 6。"},
            {"question": "∛27 = ?", "options": ["3", "9", "27", "81"], "answer": 0, "explanation": "3³ = 27，所以 ∛27 = 3。"},
            {"question": "化简 √72 = ?", "options": ["6√2", "8√2", "3√8", "2√36"], "answer": 0, "explanation": "√72 = √(36×2) = 6√2。"}
        ]
    },
    {
        "id": "t40", "stage": "代数语言", "stage_index": 1,
        "icon": "✅", "title": "几何证明", "description": "全等三角形与证明思路", "sort_order": 40,
        "lesson": [
            {"type": "title", "content": "什么是证明"},
            {"type": "text", "content": "证明是用逻辑推理，从已知条件出发，一步步推导出结论的过程。"},
            {"type": "highlight", "content": "证明的结构：已知条件 → 逻辑推理链 → 结论"},
            {"type": "title", "content": "全等三角形的判定"},
            {"type": "text", "content": "两个三角形全等 = 形状和大小完全相同。"},
            {"type": "formula", "content": "判定方法：\nSSS（三边对应相等）\nSAS（两边及夹角相等）\nASA（两角及夹边相等）\nAAS（两角及一对边相等）\nHL（直角三角形：斜边和一条直角边相等）"},
            {"type": "title", "content": "全等三角形的性质"},
            {"type": "text", "content": "全等三角形的对应边相等、对应角相等。"},
            {"type": "ex", "content": "<b>例：</b>已知 △ABC ≌ △DEF\n则 AB=DE, BC=EF, AC=DF\n∠A=∠D, ∠B=∠E, ∠C=∠F"},
            {"type": "title", "content": "证明的书写格式"},
            {"type": "text", "content": "① 写「已知」：列出题目给的条件\n② 写「求证」：写出要证明的结论\n③ 写「证明」：每一步写出依据"},
            {"type": "ex", "content": "<b>例：</b>证明等腰三角形两底角相等\n已知：AB = AC\n求证：∠B = ∠C\n证明：作 BC 边上的高 AD\n在 △ABD 和 △ACD 中：\nAB=AC（已知），AD=AD（公共边），∠ADB=∠ADC=90°\n∴ △ABD ≌ △ACD（HL）\n∴ ∠B = ∠C"}
        ],
        "quiz": [
            {"question": "SSS 判定全等需要什么条件？", "options": ["三边相等", "三角相等", "两边一角相等", "两角一边相等"], "answer": 0, "explanation": "SSS = Side-Side-Side，三边对应相等。"},
            {"question": "全等三角形的对应角？", "options": ["互补", "相等", "互余", "不确定"], "answer": 1, "explanation": "全等三角形的对应角相等、对应边相等。"},
            {"question": "HL 判定适用于什么三角形？", "options": ["任意三角形", "等腰三角形", "直角三角形", "等边三角形"], "answer": 2, "explanation": "HL 只适用于直角三角形：斜边和一条直角边相等。"}
        ]
    },
    {
        "id": "t41", "stage": "代数语言", "stage_index": 1,
        "icon": "🔍", "title": "相似与位似", "description": "相似三角形、比例线段", "sort_order": 41,
        "lesson": [
            {"type": "title", "content": "相似三角形"},
            {"type": "text", "content": "两个三角形形状相同但大小不同 = 相似。对应角相等，对应边成比例。"},
            {"type": "formula", "content": "△ABC ∽ △DEF\n∠A=∠D, ∠B=∠E, ∠C=∠F\nAB/DE = BC/EF = AC/DF = k（相似比）"},
            {"type": "title", "content": "相似三角形的判定"},
            {"type": "formula", "content": "AA（两角对应相等）\nSAS（两边成比例且夹角相等）\nSSS（三边成比例）"},
            {"type": "ex", "content": "<b>例：</b>DE ∥ BC，D 在 AB 上，E 在 AC 上\n则 △ADE ∽ △ABC\nAD/AB = AE/AC = DE/BC"},
            {"type": "title", "content": "相似的性质"},
            {"type": "formula", "content": "面积比 = 相似比的平方\nS₁/S₂ = k²"},
            {"type": "ex", "content": "<b>例：</b>相似比为 2:3\n则面积比为 4:9"},
            {"type": "title", "content": "位似变换"},
            {"type": "text", "content": "位似是一种特殊的相似：以某点为中心，按比例放大或缩小图形。"},
            {"type": "highlight", "content": "位似图形的对应点连线经过位似中心，对应边平行"}
        ],
        "quiz": [
            {"question": "两个三角形相似比为 1:2，面积比为？", "options": ["1:2", "1:4", "1:8", "2:1"], "answer": 1, "explanation": "面积比 = 相似比的平方 = 1²:2² = 1:4。"},
            {"question": "DE∥BC，AD/AB = 1/3，则 △ADE 与 △ABC 的面积比为？", "options": ["1:3", "1:6", "1:9", "1:2"], "answer": 2, "explanation": "相似比为 1:3，面积比 = 1:9。"},
            {"question": "判定相似三角形最少需要几个条件？", "options": ["1个", "2个", "3个", "4个"], "answer": 1, "explanation": "AA（两角相等）即可判定，最少2个条件。"}
        ]
    },

    # ═══════════════════════════════════════════
    # 高中补充（阶段3-4，+8 个）
    # ═══════════════════════════════════════════
    {
        "id": "t42", "stage": "函数世界", "stage_index": 3,
        "icon": "🔄", "title": "反函数", "description": "逆映射——交换输入输出", "sort_order": 42,
        "lesson": [
            {"type": "title", "content": "什么是反函数"},
            {"type": "text", "content": "如果函数 f 把 x 映射到 y，那么反函数 f⁻¹ 把 y 映射回 x。反函数「撤销」原函数的操作。"},
            {"type": "formula", "content": "y = f(x) ⟺ x = f⁻¹(y)"},
            {"type": "title", "content": "反函数的求法"},
            {"type": "text", "content": "① 用 y 表示 x：从 y = f(x) 解出 x = g(y)\n② 交换 x 和 y：y = g(x)\n③ 标明定义域"},
            {"type": "ex", "content": "<b>例：</b>求 y = 2x + 3 的反函数\n解出 x：x = (y-3)/2\n交换：y = (x-3)/2\n反函数：f⁻¹(x) = (x-3)/2"},
            {"type": "title", "content": "反函数的图像"},
            {"type": "highlight", "content": "原函数和反函数的图像关于直线 y = x 对称"},
            {"type": "title", "content": "反函数存在条件"},
            {"type": "text", "content": "只有单调函数（严格递增或递减）才有反函数。单调性保证了一个 y 只对应一个 x。"}
        ],
        "quiz": [
            {"question": "y = 3x - 6 的反函数是？", "options": ["y=(x+6)/3", "y=(x-6)/3", "y=3x+6", "y=x/3+6"], "answer": 0, "explanation": "x=(y+6)/3，交换得 y=(x+6)/3。"},
            {"question": "原函数与反函数的图像关于什么对称？", "options": ["x轴", "y轴", "y=x", "原点"], "answer": 2, "explanation": "原函数和反函数关于直线 y=x 对称。"},
            {"question": "y=x² 有反函数吗？", "options": ["有", "没有", "取决于定义域", "有时有"], "answer": 2, "explanation": "y=x² 在全体实数上不单调，限制 x≥0 时有反函数 y=√x。"}
        ]
    },
    {
        "id": "t43", "stage": "函数世界", "stage_index": 3,
        "icon": "📐", "title": "三角恒等变换", "description": "和差公式、二倍角公式", "sort_order": 43,
        "lesson": [
            {"type": "title", "content": "两角和差公式"},
            {"type": "formula", "content": "sin(α±β) = sinα·cosβ ± cosα·sinβ\ncos(α±β) = cosα·cosβ ∓ sinα·sinβ\ntan(α±β) = (tanα ± tanβ) / (1 ∓ tanα·tanβ)"},
            {"type": "ex", "content": "<b>例：</b>sin75° = sin(45°+30°)\n= sin45°·cos30° + cos45°·sin30°\n= (√6+√2)/4"},
            {"type": "title", "content": "二倍角公式"},
            {"type": "formula", "content": "sin2α = 2sinα·cosα\ncos2α = cos²α - sin²α = 2cos²α - 1 = 1 - 2sin²α"},
            {"type": "title", "content": "辅助角公式"},
            {"type": "formula", "content": "asinα + bcosα = √(a²+b²) · sin(α+φ)\n其中 tanφ = b/a"}
        ],
        "quiz": [
            {"question": "sin(α+β) = ?", "options": ["sinα+sinβ", "sinα·cosβ+cosα·sinβ", "sinα·cosβ-cosα·sinβ", "cosα·cosβ+sinα·sinβ"], "answer": 1, "explanation": "两角和的正弦公式。"},
            {"question": "cos2α 用 sinα 表示是？", "options": ["1-2sin²α", "2sin²α-1", "1-sin²α", "2sinα"], "answer": 0, "explanation": "cos2α = 1 - 2sin²α。"},
            {"question": "sinα+cosα 用辅助角公式化简？", "options": ["√2·sin(α+π/4)", "√2·cos(α+π/4)", "2sin(α+π/4)", "sin(α+π/4)"], "answer": 0, "explanation": "sinα+cosα = √2·sin(α+π/4)。"}
        ]
    },
    {
        "id": "t44", "stage": "函数世界", "stage_index": 3,
        "icon": "↩️", "title": "反三角函数", "description": "arcsin/arccos/arctan", "sort_order": 44,
        "lesson": [
            {"type": "title", "content": "为什么需要反三角函数"},
            {"type": "text", "content": "sin(x)=1/2 有无穷多个解。反三角函数给出唯一确定的「主值」。"},
            {"type": "title", "content": "反正弦 arcsin"},
            {"type": "formula", "content": "y = arcsin(x) ⟺ sin(y) = x\n定义域 [-1,1]，值域 [-π/2, π/2]"},
            {"type": "title", "content": "反余弦 arccos"},
            {"type": "formula", "content": "y = arccos(x) ⟺ cos(y) = x\n定义域 [-1,1]，值域 [0, π]"},
            {"type": "title", "content": "反正切 arctan"},
            {"type": "formula", "content": "y = arctan(x) ⟺ tan(y) = x\n定义域 (-∞,+∞)，值域 (-π/2, π/2)"}
        ],
        "quiz": [
            {"question": "arcsin(0) = ?", "options": ["0", "π/2", "π", "-π/2"], "answer": 0, "explanation": "sin(0)=0，所以 arcsin(0)=0。"},
            {"question": "arccos 的值域是？", "options": ["[-π/2,π/2]", "[0,π]", "[-π,π]", "[0,2π]"], "answer": 1, "explanation": "arccos 的值域是 [0, π]。"},
            {"question": "arctan(1) = ?", "options": ["π/6", "π/4", "π/3", "π/2"], "answer": 1, "explanation": "tan(π/4)=1，所以 arctan(1)=π/4。"}
        ]
    },
    {
        "id": "t45", "stage": "变化的科学", "stage_index": 4,
        "icon": "➡️", "title": "向量", "description": "有方向的量——向量运算", "sort_order": 45,
        "lesson": [
            {"type": "title", "content": "什么是向量"},
            {"type": "text", "content": "向量是既有大小又有方向的量。用带箭头的线段表示。"},
            {"type": "highlight", "content": "标量：只有大小（温度、质量）\n向量：有大小和方向（力、速度、位移）"},
            {"type": "title", "content": "向量的运算"},
            {"type": "formula", "content": "设 a⃗=(a₁,a₂), b⃗=(b₁,b₂)\na⃗+b⃗ = (a₁+b₁, a₂+b₂)\na⃗·b⃗ = a₁b₁ + a₂b₂（数量积/点积）"},
            {"type": "title", "content": "向量的应用"},
            {"type": "formula", "content": "垂直判定：a⃗·b⃗ = 0 ⟹ a⃗⊥b⃗\n夹角：cosθ = (a⃗·b⃗)/(|a⃗|·|b⃗|)\n模：|a⃗| = √(a₁²+a₂²)"}
        ],
        "quiz": [
            {"question": "a⃗=(2,3), b⃗=(1,4)，a⃗+b⃗ = ?", "options": ["(3,7)", "(1,-1)", "(2,12)", "(3,7)"], "answer": 0, "explanation": "坐标分别相加：(3,7)。"},
            {"question": "a⃗=(1,0), b⃗=(0,1)，a⃗·b⃗ = ?", "options": ["0", "1", "2", "√2"], "answer": 0, "explanation": "1×0+0×1=0，两向量垂直。"},
            {"question": "a⃗·b⃗ = 0 意味着？", "options": ["平行", "垂直", "相等", "相反"], "answer": 1, "explanation": "点积为零说明两向量垂直。"}
        ]
    },
    {
        "id": "t46", "stage": "函数世界", "stage_index": 3,
        "icon": "🌀", "title": "圆锥曲线", "description": "椭圆、双曲线、抛物线", "sort_order": 46,
        "lesson": [
            {"type": "title", "content": "椭圆"},
            {"type": "text", "content": "到两个焦点距离之和为常数的点的轨迹。"},
            {"type": "formula", "content": "x²/a² + y²/b² = 1 (a>b>0)\nc²=a²-b²，离心率 e=c/a<1"},
            {"type": "title", "content": "双曲线"},
            {"type": "text", "content": "到两个焦点距离之差的绝对值为常数的点的轨迹。"},
            {"type": "formula", "content": "x²/a² - y²/b² = 1\nc²=a²+b²，离心率 e=c/a>1"},
            {"type": "title", "content": "抛物线"},
            {"type": "text", "content": "到焦点和准线距离相等的点的轨迹。"},
            {"type": "formula", "content": "y²=2px (p>0)\n焦点 (p/2,0)，准线 x=-p/2"}
        ],
        "quiz": [
            {"question": "椭圆的离心率范围？", "options": ["e>1", "0<e<1", "e=1", "e=0"], "answer": 1, "explanation": "椭圆 0<e<1。"},
            {"question": "y²=8x 的焦点是？", "options": ["(2,0)", "(4,0)", "(8,0)", "(0,2)"], "answer": 0, "explanation": "2p=8, p=4, 焦点(p/2,0)=(2,0)。"},
            {"question": "双曲线与椭圆的本质区别？", "options": ["形状", "离心率", "焦点", "方程"], "answer": 1, "explanation": "椭圆 e<1，双曲线 e>1。"}
        ]
    },
    {
        "id": "t47", "stage": "函数世界", "stage_index": 3,
        "icon": "🧭", "title": "极坐标与参数方程", "description": "另一种描述曲线的方式", "sort_order": 47,
        "lesson": [
            {"type": "title", "content": "极坐标系"},
            {"type": "text", "content": "用距离 r 和角度 θ 定位点。"},
            {"type": "formula", "content": "x=r·cosθ, y=r·sinθ\nr²=x²+y², tanθ=y/x"},
            {"type": "title", "content": "参数方程"},
            {"type": "text", "content": "用参数 t 表示 x 和 y。"},
            {"type": "formula", "content": "圆：x=r·cost, y=r·sint\n椭圆：x=a·cost, y=b·sint"}
        ],
        "quiz": [
            {"question": "极坐标(2,π/4)的直角坐标？", "options": ["(√2,√2)", "(1,1)", "(2,2)", "(√2,1)"], "answer": 0, "explanation": "x=2cos(π/4)=√2, y=2sin(π/4)=√2。"},
            {"question": "r 代表什么？", "options": ["角度", "到原点距离", "半径", "斜率"], "answer": 1, "explanation": "r 是点到极点的距离。"},
            {"question": "圆的参数方程中 t 的范围？", "options": ["0到π", "0到2π", "-∞到+∞", "0到π/2"], "answer": 1, "explanation": "t 从 0 到 2π 遍历整个圆。"}
        ]
    },
    {
        "id": "t48", "stage": "抽象与推理", "stage_index": 5,
        "icon": "🪜", "title": "数学归纳法", "description": "证明与自然数有关的命题", "sort_order": 48,
        "lesson": [
            {"type": "title", "content": "什么是数学归纳法"},
            {"type": "text", "content": "证明「对所有自然数 n 成立」的方法，像推倒多米诺骨牌。"},
            {"type": "highlight", "content": "基础步：验证 n=1 成立\n归纳步：假设 n=k 成立，证明 n=k+1 也成立\n结论：对所有 n 成立"},
            {"type": "ex", "content": "<b>例：</b>证明 1+2+...+n = n(n+1)/2\n基础步：n=1，左边=1，右边=1 ✓\n归纳步：假设 n=k 时成立\nn=k+1 时：k(k+1)/2+(k+1)=(k+1)(k+2)/2 ✓"}
        ],
        "quiz": [
            {"question": "归纳法第一步是？", "options": ["假设n=k", "验证n=1", "证明n=k+1", "结论"], "answer": 1, "explanation": "先验证基础情况 n=1。"},
            {"question": "「假设n=k成立」叫？", "options": ["基础步", "归纳假设", "归纳步", "结论"], "answer": 1, "explanation": "这叫归纳假设。"},
            {"question": "两步可以省略一步吗？", "options": ["省第一", "省第二", "都不能省", "都可省"], "answer": 2, "explanation": "两步缺一不可。"}
        ]
    },
    {
        "id": "t49", "stage": "抽象与推理", "stage_index": 5,
        "icon": "🎴", "title": "排列组合", "description": "计数原理与二项式定理", "sort_order": 49,
        "lesson": [
            {"type": "title", "content": "加法原理与乘法原理"},
            {"type": "highlight", "content": "加法原理：分类计数，各类方法数相加\n乘法原理：分步计数，各步方法数相乘"},
            {"type": "title", "content": "排列"},
            {"type": "text", "content": "从 n 个取 m 个排列（考虑顺序）。"},
            {"type": "formula", "content": "A(n,m) = n!/(n-m)!\nA(5,3)=5×4×3=60"},
            {"type": "title", "content": "组合"},
            {"type": "text", "content": "从 n 个取 m 个（不考虑顺序）。"},
            {"type": "formula", "content": "C(n,m) = n!/(m!(n-m)!)\nC(5,3)=10"},
            {"type": "title", "content": "二项式定理"},
            {"type": "formula", "content": "(a+b)ⁿ = Σ C(n,k)·aⁿ⁻ᵏ·bᵏ"}
        ],
        "quiz": [
            {"question": "A(4,2) = ?", "options": ["6", "8", "12", "24"], "answer": 2, "explanation": "A(4,2)=4×3=12。"},
            {"question": "C(6,2) = ?", "options": ["12", "15", "30", "36"], "answer": 1, "explanation": "C(6,2)=6×5/2=15。"},
            {"question": "排列和组合的区别？", "options": ["数量", "是否考虑顺序", "元素", "方法"], "answer": 1, "explanation": "排列考虑顺序，组合不考虑。"}
        ]
    },

    # ═══════════════════════════════════════════
    # 大学新阶段（阶段6，+6 个）
    # ═══════════════════════════════════════════
    {
        "id": "t50", "stage": "高等数学", "stage_index": 6,
        "icon": "🎯", "title": "极限", "description": "无穷逼近——极限的严格定义", "sort_order": 50,
        "lesson": [
            {"type": "title", "content": "极限的直觉"},
            {"type": "text", "content": "当 x 越来越接近 a 时，f(x) 越来越接近 L，L 就是极限。"},
            {"type": "formula", "content": "lim[x→a] f(x) = L"},
            {"type": "title", "content": "ε-δ 定义"},
            {"type": "text", "content": "对任意 ε>0，存在 δ>0，当 0<|x-a|<δ 时，|f(x)-L|<ε。"},
            {"type": "highlight", "content": "直觉：无论要求多精确（ε），都能找到范围（δ）使 f(x) 与 L 的差距小于 ε"},
            {"type": "title", "content": "重要极限"},
            {"type": "formula", "content": "lim[x→0] sin(x)/x = 1\nlim[x→∞] (1+1/x)ˣ = e"},
            {"type": "ex", "content": "<b>例：</b>lim[x→2] (x²-4)/(x-2)\n= lim (x+2)(x-2)/(x-2) = lim (x+2) = 4"}
        ],
        "quiz": [
            {"question": "lim[x→3] (2x+1) = ?", "options": ["5", "6", "7", "8"], "answer": 2, "explanation": "代入：2×3+1=7。"},
            {"question": "lim[x→0] sin(x)/x = ?", "options": ["0", "1", "∞", "不存在"], "answer": 1, "explanation": "第一个重要极限，结果为1。"},
            {"question": "lim[x→∞] (1+1/x)ˣ = ?", "options": ["1", "2", "e", "∞"], "answer": 2, "explanation": "e 的定义之一。"}
        ]
    },
    {
        "id": "t51", "stage": "高等数学", "stage_index": 6,
        "icon": "📈", "title": "连续与间断", "description": "连续性、间断点、介值定理", "sort_order": 51,
        "lesson": [
            {"type": "title", "content": "连续的定义"},
            {"type": "text", "content": "f(x) 在点 a 连续需满足：① f(a) 有定义 ② 极限存在 ③ 极限=f(a)"},
            {"type": "highlight", "content": "连续 = 图像没有断开、跳跃或空洞"},
            {"type": "title", "content": "间断点分类"},
            {"type": "formula", "content": "第一类（左右极限都存在）：可去、跳跃\n第二类（至少一侧极限不存在）：无穷、振荡"},
            {"type": "title", "content": "介值定理与零点定理"},
            {"type": "text", "content": "介值定理：连续函数取遍 f(a) 和 f(b) 之间的所有值\n零点定理：f(a) 和 f(b) 异号，则 (a,b) 内有零点"},
            {"type": "ex", "content": "<b>例：</b>f(x)=x³-x-1\nf(1)=-1<0, f(2)=5>0\n由零点定理，(1,2) 内有根"}
        ],
        "quiz": [
            {"question": "连续需要几个条件？", "options": ["1", "2", "3", "4"], "answer": 2, "explanation": "三个：有定义、极限存在、极限=函数值。"},
            {"question": "f(x)=1/x 在 x=0 是？", "options": ["连续", "可去间断", "跳跃间断", "无穷间断"], "answer": 3, "explanation": "x→0 时 f→∞，无穷间断点。"},
            {"question": "零点定理要求？", "options": ["任意函数", "连续函数", "可导函数", "单调函数"], "answer": 1, "explanation": "要求在闭区间上连续。"}
        ]
    },
    {
        "id": "t52", "stage": "高等数学", "stage_index": 6,
        "icon": "📐", "title": "多元函数微积分", "description": "偏导数、全微分、重积分", "sort_order": 52,
        "lesson": [
            {"type": "title", "content": "偏导数"},
            {"type": "text", "content": "对某一个变量求导，其他变量视为常数。"},
            {"type": "formula", "content": "f(x,y)=x²y\n∂f/∂x = 2xy\n∂f/∂y = x²"},
            {"type": "title", "content": "全微分"},
            {"type": "formula", "content": "df = (∂f/∂x)dx + (∂f/∂y)dy"},
            {"type": "title", "content": "重积分"},
            {"type": "text", "content": "二重积分是对平面区域上的函数求「体积」。"},
            {"type": "formula", "content": "∬_D f(x,y) dA = ∫∫ f(x,y) dydx"}
        ],
        "quiz": [
            {"question": "f(x,y)=x²y，∂f/∂x = ?", "options": ["2xy", "x²", "2x", "y"], "answer": 0, "explanation": "对 x 求偏导，y 视为常数：2xy。"},
            {"question": "偏导数和全导数的区别？", "options": ["没区别", "偏导只对一个变量", "全导更简单", "偏导不存在"], "answer": 1, "explanation": "偏导只对一个变量求导。"},
            {"question": "二重积分的几何意义？", "options": ["面积", "体积", "长度", "斜率"], "answer": 1, "explanation": "曲面下方的体积。"}
        ]
    },
    {
        "id": "t53", "stage": "高等数学", "stage_index": 6,
        "icon": "📊", "title": "线性代数基础", "description": "矩阵、行列式、线性方程组", "sort_order": 53,
        "lesson": [
            {"type": "title", "content": "矩阵"},
            {"type": "text", "content": "矩阵是数的矩形排列。m×n 矩阵有 m 行 n 列。"},
            {"type": "formula", "content": "矩阵加法：对应元素相加\n矩阵乘法：行×列求和"},
            {"type": "title", "content": "行列式"},
            {"type": "formula", "content": "2×2 行列式：|a b; c d| = ad-bc"},
            {"type": "title", "content": "线性方程组"},
            {"type": "text", "content": "用矩阵表示 Ax=b，解法：高斯消元、克拉默法则。"},
            {"type": "formula", "content": "克拉默法则：xᵢ = |Aᵢ|/|A|\n行列式为 0 则无唯一解"}
        ],
        "quiz": [
            {"question": "2×2 行列式公式？", "options": ["a+b+c+d", "ad-bc", "ab-cd", "ac-bd"], "answer": 1, "explanation": "ad-bc。"},
            {"question": "矩阵乘法满足交换律吗？", "options": ["满足", "不满足", "有时", "取决于"], "answer": 1, "explanation": "一般 AB≠BA。"},
            {"question": "行列式为0意味着？", "options": ["可逆", "不可逆", "单位矩阵", "零矩阵"], "answer": 1, "explanation": "行列式为0，矩阵不可逆。"}
        ]
    },
    {
        "id": "t54", "stage": "高等数学", "stage_index": 6,
        "icon": "🔀", "title": "常微分方程", "description": "含有未知函数导数的方程", "sort_order": 54,
        "lesson": [
            {"type": "title", "content": "什么是微分方程"},
            {"type": "text", "content": "含有未知函数及其导数的方程。解 = 找出满足方程的函数。"},
            {"type": "title", "content": "可分离变量方程"},
            {"type": "formula", "content": "y' = g(x)·h(y)\ndy/h(y) = g(x)dx，两边积分"},
            {"type": "ex", "content": "<b>例：</b>y'=xy → dy/y = xdx → ln|y|=x²/2+C → y=Ce^(x²/2)"},
            {"type": "title", "content": "二阶常系数齐次方程"},
            {"type": "formula", "content": "y''+py'+qy=0\n特征方程 r²+pr+q=0\n根据根写通解"}
        ],
        "quiz": [
            {"question": "y'=2x 的通解？", "options": ["y=x²", "y=x²+C", "y=2x+C", "y=2"], "answer": 1, "explanation": "积分得 x²+C。"},
            {"question": "可分离变量的核心？", "options": ["两边求导", "分离x和y分别积分", "代入", "画图"], "answer": 1, "explanation": "分离后分别积分。"},
            {"question": "y''-y=0 的特征方程？", "options": ["r²-r=0", "r²-1=0", "r²+1=0", "r-1=0"], "answer": 1, "explanation": "r²-1=0。"}
        ]
    },
    {
        "id": "t55", "stage": "高等数学", "stage_index": 6,
        "icon": "🎲", "title": "概率论", "description": "随机变量、分布、期望与大数定律", "sort_order": 55,
        "lesson": [
            {"type": "title", "content": "随机变量"},
            {"type": "text", "content": "把随机事件结果映射为数值的函数。离散型取有限个值，连续型取值充满区间。"},
            {"type": "title", "content": "常见分布"},
            {"type": "formula", "content": "二项分布 B(n,p)：n 次试验中成功次数\n正态分布 N(μ,σ²)：钟形曲线\n泊松分布 P(λ)：稀有事件"},
            {"type": "title", "content": "期望与方差"},
            {"type": "formula", "content": "E(X) = Σ xᵢpᵢ 或 ∫xf(x)dx\nD(X) = E(X²) - [E(X)]²"},
            {"type": "title", "content": "大数定律与中心极限定理"},
            {"type": "highlight", "content": "大数定律：样本越大，均值越接近真值\n中心极限定理：大量独立随机变量之和近似正态分布"}
        ],
        "quiz": [
            {"question": "掷骰子的期望？", "options": ["3", "3.5", "4", "6"], "answer": 1, "explanation": "(1+2+3+4+5+6)/6=3.5。"},
            {"question": "正态分布形状？", "options": ["直线", "钟形", "U形", "均匀"], "answer": 1, "explanation": "钟形曲线。"},
            {"question": "大数定律说明？", "options": ["越大越准", "越大均值越接近真值", "越大方差越大", "越偏离"], "answer": 1, "explanation": "样本越大，均值越接近总体均值。"}
        ]
    },
]
