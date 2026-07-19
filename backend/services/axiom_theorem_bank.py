"""
数学公理 / 定理及其证明过程库

供 AI 推导注入提示词，以及无 API Key 时的离线回退。
核心：给出真正的公理、定理表述，以及可跟读的证明步骤；
plain / analogy 仅为辅助理解，不替代形式陈述与证明。
"""
import json
from typing import Optional


def _entry(
    axioms,
    theorem_name,
    theorem_statement,
    theorem_plain,
    proof,
    plain_summary,
    analogy="",
    given="",
    to_prove="",
):
    """axioms: [{name, statement, plain}]；proof: [{title, content, formula?, reason?, hint?, example?, graph?}]"""
    return {
        "axioms": axioms,
        "theorem": {
            "name": theorem_name,
            "statement": theorem_statement,
            "plain": theorem_plain,
        },
        "given": given,
        "to_prove": to_prove or theorem_statement,
        "analogy": analogy,
        "proof": proof,
        # 兼容旧前端：steps 与 proof 同步
        "steps": proof,
        "plain_summary": plain_summary,
    }


BANK = {
    # ── 自然数：皮亚诺公理 ──
    "t1": _entry(
        axioms=[
            {
                "name": "皮亚诺公理（Peano）— 起点",
                "statement": "1 是自然数。",
                "plain": "自然数集合不是空的，至少从 1 开始（有的教材从 0 开始，规则同类）。",
            },
            {
                "name": "皮亚诺公理 — 后继",
                "statement": "每个自然数 n 都有唯一的后继 S(n)，且 S(n) 也是自然数。",
                "plain": "每个数后面恰好有一个「下一个数」。",
            },
            {
                "name": "皮亚诺公理 — 后继单射",
                "statement": "若 S(m)=S(n)，则 m=n；且对任意 n，S(n)≠1。",
                "plain": "不同的数后继不同；1 不是任何数的后继（没有「0.5 的下一个是 1」这种混淆）。",
            },
            {
                "name": "皮亚诺公理 — 归纳原理",
                "statement": "若集合 A 含 1，且 n∈A ⇒ S(n)∈A，则全体自然数都属于 A。",
                "plain": "数学归纳法的公理基础：从 1 能推到下一个，就能推到全部。",
            },
        ],
        theorem_name="自然数的后继生成性",
        theorem_statement="每一个自然数都可以由 1 经有限次后继运算得到。",
        theorem_plain="任意自然数都是「从 1 开始，加 1 加够若干次」得到的。",
        given="皮亚诺公理成立。",
        to_prove="任意自然数 n 均可写成 S(S(…S(1)…)) 的有限次后继。",
        analogy="像从第 1 级楼梯每次只上一级：任意一级都能这样走上去。",
        proof=[
            {
                "title": "证明准备：设集合 A",
                "content": "令 A 为「可由 1 经有限次后继得到」的全体自然数构成的集合。要证 A 等于全体自然数 ℕ。",
                "reason": "目标：用归纳公理证明 A=ℕ",
            },
            {
                "title": "第一步：1∈A",
                "content": "由定义，1 是 0 次后继的结果，故 1∈A。",
                "formula": "1 ∈ A",
                "reason": "依据：皮亚诺公理「1 是自然数」及集合 A 的定义",
            },
            {
                "title": "第二步：若 n∈A，则 S(n)∈A",
                "content": "若 n 可由 1 经 k 次后继得到，则 S(n) 可由 1 经 k+1 次后继得到，故 S(n)∈A。",
                "formula": "n ∈ A ⇒ S(n) ∈ A",
                "reason": "依据：后继公理 + A 的定义",
            },
            {
                "title": "第三步：由归纳公理得 A=ℕ",
                "content": "A 含 1，且对后继封闭。由归纳公理，ℕ⊆A。又显然 A⊆ℕ，故 A=ℕ。证毕。",
                "formula": "A = ℕ",
                "reason": "依据：皮亚诺归纳公理",
                "hint": "这就是「归纳法能用」的根源",
            },
        ],
        plain_summary="皮亚诺公理规定自然数的起点与后继规则；由归纳公理可证明：每个自然数都由 1 反复取后继得到。",
    ),
    # ── 加法交换律（基于后继）──
    "t2": _entry(
        axioms=[
            {
                "name": "加法递归定义（基于后继）",
                "statement": "a+1 := S(a)；a+S(b) := S(a+b)。",
                "plain": "加 1 就是取后继；加更大的数，就是对「已经加完的结果」再取后继。",
            },
            {
                "name": "皮亚诺归纳公理",
                "statement": "见自然数主题：对含 1 且对后继封闭的集合，等于全体自然数。",
                "plain": "要证「对所有自然数成立」，证 n=1 与「n 成立 ⇒ n+1 成立」即可。",
            },
        ],
        theorem_name="加法交换律",
        theorem_statement="对任意自然数 a,b，有 a+b = b+a。",
        theorem_plain="两个自然数相加，交换顺序结果相同。",
        given="加法由后继递归定义；归纳公理成立。",
        to_prove="∀a,b∈ℕ，a+b=b+a。",
        analogy="两堆石子合在一起，先拿哪一堆，总数不变——下面用公理严格证明。",
        proof=[
            {
                "title": "引理：a+1 = 1+a（对 a 归纳）",
                "content": "当 a=1：1+1=S(1)=1+1，成立。假设 a+1=1+a。则 S(a)+1 = S(S(a))，而 1+S(a)=S(1+a)=S(a+1)=S(S(a))。故对 a+1 也成立。由归纳，∀a，a+1=1+a。",
                "formula": "a+1 = 1+a",
                "reason": "依据：加法定义 + 归纳公理",
            },
            {
                "title": "对固定 a，关于 b 归纳证明 a+b=b+a",
                "content": "b=1 时由引理得 a+1=1+a。假设 a+b=b+a。则 a+S(b)=S(a+b)=S(b+a)=S(b)+a（最后一步用加法定义与归纳假设）。故 a+S(b)=S(b)+a。",
                "formula": "a+b = b+a",
                "reason": "依据：引理 + 加法递归定义 + 对 b 的归纳",
            },
            {
                "title": "结论",
                "content": "对任意固定 a，命题对一切 b 成立；又 a 任意，故交换律对一切自然数成立。证毕。",
                "reason": "全称量化",
            },
        ],
        plain_summary="交换律不是死记口诀，而是由「加法=后继」与归纳公理可证明的定理。",
    ),
    # ── 分配律 ──
    "t7": _entry(
        axioms=[
            {
                "name": "乘法递归定义",
                "statement": "a·1 := a；a·S(b) := a·b + a。",
                "plain": "乘 1 得自己；乘「更大一号」等于「原来的积再加一个 a」。",
            },
            {
                "name": "加法结合律 / 交换律",
                "statement": "(a+b)+c=a+(b+c)，a+b=b+a（可由皮亚诺体系证明，此处作为已证引理使用）。",
                "plain": "加法可随意换序、换括号。",
            },
        ],
        theorem_name="乘法对加法的分配律",
        theorem_statement="对任意自然数 a,b,c，有 a(b+c)=ab+ac。",
        theorem_plain="先加后乘等于分别乘再加。",
        given="乘法、加法的递归定义；加法运算律。",
        to_prove="a(b+c)=ab+ac。",
        analogy="长方形面积切开再拼：严格证明见下方对 c 的归纳。",
        proof=[
            {
                "title": "对 c 作归纳（固定 a,b）",
                "content": "c=1：左边 a(b+1)=a·S(b)=ab+a；右边 ab+a·1=ab+a。相等。",
                "formula": "a(b+1) = ab + a",
                "reason": "乘法定义：a·S(b)=ab+a",
            },
            {
                "title": "归纳步骤",
                "content": "假设 a(b+c)=ab+ac。则 a(b+S(c))=a·S(b+c)=a(b+c)+a = (ab+ac)+a = ab+(ac+a)=ab+a·S(c)。",
                "formula": "a(b+S(c)) = ab + a·S(c)",
                "reason": "归纳假设 + 乘法定义 + 加法结合律",
            },
            {
                "title": "结论",
                "content": "由归纳公理，对一切自然数 c 成立。a,b 任意，故分配律普遍成立。证毕。",
                "reason": "归纳公理",
            },
        ],
        plain_summary="分配律可由乘法的递归定义对其中一个加数归纳证明。",
    ),
    # ── 等式性质（解方程依据）──
    "t8": _entry(
        axioms=[
            {
                "name": "等式的自反、对称、传递",
                "statement": "a=a；若 a=b 则 b=a；若 a=b 且 b=c 则 a=c。",
                "plain": "相等是等价关系。",
            },
            {
                "name": "等式的运算相容性（等式公理）",
                "statement": "若 a=b，则 a+c=b+c，a·c=b·c（在适当数集中）。",
                "plain": "相等的两边做相同运算，结果仍相等。",
            },
        ],
        theorem_name="一元一次方程的同解变形",
        theorem_statement="对方程两边同时加（减）同一数，或乘（除）同一非零数，所得方程与原方程同解。",
        theorem_plain="天平两边做同样合法操作，解集不变。",
        given="实数域上的等式公理；c≠0。",
        to_prove="a=b ⇔ a+c=b+c；a=b ⇔ a·c=b·c（c≠0）。",
        proof=[
            {
                "title": "⇒：由运算相容性",
                "content": "若 a=b，由等式公理直接得 a+c=b+c 与 a·c=b·c。",
                "reason": "等式公理",
            },
            {
                "title": "⇐（加法）：两边加 −c",
                "content": "若 a+c=b+c，两边同加 (−c)，得 a=b。故两边加同一数是可逆的，解集相同。",
                "formula": "a+c=b+c ⇒ a=b",
                "reason": "加法逆元 + 等式公理",
            },
            {
                "title": "⇐（乘法）：两边乘 1/c",
                "content": "若 a·c=b·c 且 c≠0，两边同乘 c⁻¹，得 a=b。故乘非零数亦可逆。",
                "formula": "ac=bc (c≠0) ⇒ a=b",
                "reason": "乘法逆元 + 等式公理",
                "example": "2x+3=7 ⇒ 2x=4 ⇒ x=2；每步可逆故同解。",
            },
        ],
        plain_summary="解方程的每一步都对应等式公理及其可逆变形，因此解不多也不丢。",
    ),
    # ── 不等式乘负数 ──
    "t9": _entry(
        axioms=[
            {
                "name": "实数序公理（加法保序）",
                "statement": "若 a<b，则对一切实数 c，a+c<b+c。",
                "plain": "两边加同一个数，大小关系不变。",
            },
            {
                "name": "实数序公理（正数乘法保序）",
                "statement": "若 a<b 且 c>0，则 ac<bc。",
                "plain": "乘正数，不等号方向不变。",
            },
            {
                "name": "实数序公理（正负三分）",
                "statement": "对任意实数 x，恰有其一：x>0，x=0，或 x<0。",
                "plain": "每个数要么正、要么零、要么负。",
            },
        ],
        theorem_name="不等式乘负数变号",
        theorem_statement="若 a<b 且 c<0，则 ac>bc。",
        theorem_plain="两边乘负数，不等号方向反转。",
        given="a<b，c<0。",
        to_prove="ac>bc。",
        proof=[
            {
                "title": "设 d=−c",
                "content": "因 c<0，故 d=−c>0。",
                "formula": "d = −c > 0",
                "reason": "负数的定义 / 序公理",
            },
            {
                "title": "对 a<b 两边乘正数 d",
                "content": "由正数乘法保序：ad<bd，即 a(−c)<b(−c)，即 −ac < −bc。",
                "formula": "−ac < −bc",
                "reason": "正数乘法保序公理",
            },
            {
                "title": "两边加 ac+bc",
                "content": "−ac < −bc，两边同加 (ac+bc)，得 bc < ac，即 ac>bc。证毕。",
                "formula": "ac > bc",
                "reason": "加法保序公理",
                "example": "3>2，乘 −1：−3<−2。",
            },
        ],
        plain_summary="乘负数变号可由「先乘其相反数（正数）」再移项严格推出。",
    ),
    # ── 平行公理 ──
    "t12": _entry(
        axioms=[
            {
                "name": "欧几里得平行公理（第五公设的常用等价形式）",
                "statement": "过直线外一点，有且只有一条直线与已知直线平行。",
                "plain": "在平面内，给定直线与线外一点，平行线恰好一条。",
            },
            {
                "name": "同位角定义",
                "statement": "两条直线被第三条直线所截，位置相同的角称为同位角。",
                "plain": "截线切两条线时，「同一侧同一方位」的那对角。",
            },
        ],
        theorem_name="平行线的同位角相等",
        theorem_statement="若两直线平行，则同位角相等。",
        theorem_plain="平行 ⇒ 同位角相等（亦可作判定定理的逆方向使用，需另证）。",
        given="直线 a∥b，截线 t 与它们相交，∠1 与 ∠2 为同位角。",
        to_prove="∠1 = ∠2。",
        proof=[
            {
                "title": "反证法假设",
                "content": "假设 ∠1 ≠ ∠2。则可过交点作另一条直线 a′，使它与 t 所成同位角等于 ∠2，从而 a′∥b（同位角相等的判定，若已作为公理/已证定理使用）。",
                "reason": "反证法",
            },
            {
                "title": "与平行公理矛盾",
                "content": "此时过同一点有 a 与 a′ 两条不同直线都平行于 b，与「有且只有一条」矛盾。故假设不成立，必有 ∠1=∠2。证毕。",
                "reason": "平行公理（唯一性）",
                "hint": "核心是用「唯一平行线」逼出角相等",
            },
        ],
        plain_summary="同位角相等是平行公理的推论；证明常用反证法抓住「只能有一条平行线」。",
    ),
    # ── 勾股定理 ──
    "t13": _entry(
        axioms=[
            {
                "name": "面积公理（有限可加性）",
                "statement": "若多边形分解为内部不重叠的若干多边形，则总面积等于各部分面积之和。",
                "plain": "拼图不重叠不留缝，总面积等于各块之和。",
            },
            {
                "name": "正方形面积公式",
                "statement": "边长为 s 的正方形面积为 s²。",
                "plain": "正方形面积=边×边。",
            },
            {
                "name": "直角三角形面积",
                "statement": "直角边为 a,b 的直角三角形面积为 ab/2。",
                "plain": "直角三角形是对应长方形的一半。",
            },
        ],
        theorem_name="勾股定理（毕达哥拉斯定理）",
        theorem_statement="直角三角形中，两直角边 a,b 与斜边 c 满足 a²+b²=c²。",
        theorem_plain="直角边平方和等于斜边平方。",
        given="△ABC 中 ∠C=90°，BC=a，AC=b，AB=c。",
        to_prove="a²+b²=c²。",
        analogy="四个全等直角三角形围成「斜边朝内」的图案时，内外正方形面积关系给出证明。",
        proof=[
            {
                "title": "构图",
                "content": "作边长为 a+b 的大正方形。在其四边上分别截取长度为 a 与 b，连接得四个全等直角三角形，中间围成边长为 c 的正方形（由直角与全等可证四边相等且角为直角）。",
                "reason": "尺规/几何作图；全等三角形",
            },
            {
                "title": "用两种方式算大正方形面积",
                "content": "方式一：边长平方 (a+b)² = a²+2ab+b²。方式二：四个三角形面积之和 4·(ab/2)=2ab，加上中间小正方形 c²。",
                "formula": "(a+b)² = 2ab + c²",
                "reason": "面积可加性 + 正方形/三角形面积公式",
            },
            {
                "title": "化简得定理",
                "content": "a²+2ab+b² = 2ab+c²，两边减去 2ab，得 a²+b²=c²。证毕。",
                "formula": "a² + b² = c²",
                "reason": "等式性质（两边减同一式）",
                "example": "3²+4²=5² ⇒ 9+16=25。",
            },
        ],
        plain_summary="勾股定理可用「大正方形两种面积算法」严格证明，依据是面积可加与基本面积公式。",
    ),
    # ── 四边形与多边形内角和 ──
    "t14": _entry(
        axioms=[
            {
                "name": "三角形内角和定理",
                "statement": "任意三角形三个内角之和等于 180°。",
                "plain": "三角形的三个角加起来是一个平角。",
            },
            {
                "name": "简单多边形的三角剖分",
                "statement": "从凸 n 边形的一个顶点向所有不相邻顶点连对角线，可将该多边形分成互不重叠的 (n−2) 个三角形。",
                "plain": "四边形切一刀成 2 个三角形，五边形切成 3 个……",
            },
        ],
        theorem_name="多边形内角和公式",
        theorem_statement="凸 n 边形（n≥3）的内角和等于 (n−2)×180°。",
        theorem_plain="边数减 2，再乘 180°，就是全部内角的和。",
        given="凸 n 边形 P（n≥3）。",
        to_prove="P 的内角和 = (n−2)×180°。",
        analogy="把多边形从一顶点切开成若干三角形：切几刀、有几个三角形，内角就加几次 180°。",
        proof=[
            {
                "title": "三角剖分",
                "content": "在凸 n 边形中任取一顶点 A，向所有不相邻顶点作对角线。这些对角线落在多边形内部且互不交叉（凸性保证），从而把 P 分成恰好 (n−2) 个三角形，它们的并集是 P，内部两两不重叠。",
                "formula": "三角形个数 = n − 2",
                "reason": "凸多边形的三角剖分（标准几何事实）",
            },
            {
                "title": "内角之和等于各三角形内角之和",
                "content": "多边形每个内角恰好是剖分后某个（或相邻拼成的）三角形内角的一部分，且剖分不增加新的「多边形内角」。因此 P 的全部内角之和，等于这 (n−2) 个三角形的全部内角之和。",
                "reason": "角的分割与可加性；剖分覆盖全部内角",
            },
            {
                "title": "代入三角形内角和",
                "content": "每个三角形内角和为 180°，共有 (n−2) 个，故总和为 (n−2)×180°。特别地，四边形 n=4 时内角和为 360°。证毕。",
                "formula": "Σ内角 = (n−2)×180°",
                "reason": "三角形内角和定理 + 乘法",
                "example": "五边形：(5−2)×180°=540°；六边形：720°。",
            },
        ],
        plain_summary="多边形内角和 = (边数−2)×180°，证法是切成 (n−2) 个三角形再相加。",
    ),
    # ── 圆与 π ──
    "t15": _entry(
        axioms=[
            {
                "name": "圆的定义",
                "statement": "平面上到定点 O 的距离等于定长 r 的点的集合称为圆；O 为圆心，r 为半径。",
                "plain": "圆规一脚固定，另一脚画出的轨迹。",
            },
            {
                "name": "相似比与周长",
                "statement": "任意两圆相似；周长与直径成正比。",
                "plain": "放大圆，周长按同一比例变大。",
            },
        ],
        theorem_name="圆周长公式",
        theorem_statement="半径为 r 的圆周长 C=2πr，其中 π 定义为圆周长与直径之比（对一切圆为同一常数）。",
        theorem_plain="周长=2×π×半径。",
        given="圆半径 r，直径 d=2r；π:=C/d（与圆的选取无关）。",
        to_prove="C=2πr。",
        proof=[
            {
                "title": "由 π 的定义",
                "content": "定义 π=C/d。因一切圆相似，该比值与圆的大小无关，故 π 为绝对常数。",
                "formula": "π = C/d",
                "reason": "定义 + 圆的相似性",
            },
            {
                "title": "代入 d=2r",
                "content": "C=π·d=π·2r=2πr。证毕。",
                "formula": "C = 2πr",
                "reason": "代换",
            },
            {
                "title": "面积公式的极限证明思路（简述）",
                "content": "将圆等分为 n 个扇形，拼成近似平行四边形（或矩形），底→πr，高→r，面积→πr²。严格化需极限定义。",
                "formula": "A = πr²",
                "reason": "穷竭法 / 定积分思想",
            },
        ],
        plain_summary="π 是「周长÷直径」的常数；由此立刻推出 C=2πr；面积 πr² 需极限严格化。",
    ),
    # ── 函数定义 ──
    "t16": _entry(
        axioms=[
            {
                "name": "函数的集合论定义",
                "statement": "设 X,Y 为集合。关系 f⊆X×Y 称为从 X 到 Y 的函数，当且仅当：对每个 x∈X，存在唯一的 y∈Y 使 (x,y)∈f。记 y=f(x)。",
                "plain": "每个输入恰好对应一个输出。",
            }
        ],
        theorem_name="垂直线检验（图像判据）",
        theorem_statement="平面曲线 Γ 是某函数 y=f(x) 的图像，当且仅当任意竖直线 x=x₀ 与 Γ 至多交于一点。",
        theorem_plain="竖线扫过去最多碰一个点，才是函数图像。",
        given="曲线 Γ⊂ℝ²。",
        to_prove="Γ 为函数图像 ⇔ 任意竖直线与 Γ 交点个数 ≤1。",
        proof=[
            {
                "title": "⇒",
                "content": "若 Γ={(x,f(x))}，则对固定 x₀，满足的点只有 (x₀,f(x₀)) 至多一个。故竖线交点≤1。",
                "reason": "函数单值性",
            },
            {
                "title": "⇐",
                "content": "若每条竖线至多一个交点，则对每个 x，使 (x,y)∈Γ 的 y 至多一个。令定义域为有交点的 x 之集，定义 f(x) 为该唯一 y，则 Γ 即 f 的图像。",
                "reason": "由几何条件构造函数",
            },
        ],
        plain_summary="函数的本质是单值对应；垂直线检验是这一定义在坐标平面上的等价说法。",
    ),
    # ── 一次函数 ──
    "t17": _entry(
        axioms=[
            {
                "name": "平面直角坐标系与两点确定直线",
                "statement": "平面内不重合两点确定唯一直线；直线方程在适当坐标系下可写为线性式。",
                "plain": "两点一线。",
            },
            {
                "name": "斜率定义",
                "statement": "非竖直直线的斜率 k:=Δy/Δx（对直线上任意两点相同）。",
                "plain": "升高量÷水平量。",
            },
        ],
        theorem_name="一次函数图像为直线",
        theorem_statement="函数 f(x)=kx+b（k,b∈ℝ）的图像是斜率为 k、在 y 轴截距为 b 的直线。",
        theorem_plain="y=kx+b 画出来是一条直的线。",
        given="f(x)=kx+b。",
        to_prove="点集 {(x,kx+b)} 是斜率为 k、截距 b 的直线。",
        proof=[
            {
                "title": "取两点算斜率",
                "content": "取 x₁≠x₂，对应点 (x₁,kx₁+b)、(x₂,kx₂+b)。Δy/Δx=(k(x₂−x₁))/(x₂−x₁)=k。故任意两点连线斜率恒为 k。",
                "formula": "Δy/Δx = k",
                "reason": "斜率定义 + 代数运算",
            },
            {
                "title": "截距",
                "content": "x=0 时 y=b，故与 y 轴交于 (0,b)。",
                "formula": "f(0)=b",
                "reason": "代入",
            },
            {
                "title": "结论",
                "content": "斜率恒定的点集是直线；故图像为所求直线。证毕。",
                "reason": "平面几何：定斜率轨迹为直线",
            },
        ],
        plain_summary="由斜率恒为 k 与过 (0,b)，证明 y=kx+b 的图像是直线。",
    ),
    # ── 二次函数顶点 ──
    "t18": _entry(
        axioms=[
            {
                "name": "实数域代数恒等变形",
                "statement": "对表达式加上再减去同一项，值不变；完全平方公式 (x+p)²=x²+2px+p²。",
                "plain": "合法变形不改变函数值。",
            }
        ],
        theorem_name="二次函数的顶点公式",
        theorem_statement="对 a≠0，f(x)=ax²+bx+c 可配方为 f(x)=a(x+b/(2a))²+(4ac−b²)/(4a)；顶点为 (−b/(2a), (4ac−b²)/(4a))。",
        theorem_plain="顶点横坐标是 −b/(2a)。",
        given="a≠0，f(x)=ax²+bx+c。",
        to_prove="顶点坐标公式成立。",
        proof=[
            {
                "title": "提取 a 并配方",
                "content": "f(x)=a(x²+(b/a)x)+c。令 p=b/(2a)，则 x²+(b/a)x=(x+p)²−p²。",
                "formula": "x²+(b/a)x = (x+b/(2a))² − (b/(2a))²",
                "reason": "完全平方公式",
            },
            {
                "title": "整理",
                "content": "f(x)=a(x+b/(2a))² − a·(b²/4a²) + c = a(x+b/(2a))² + (4ac−b²)/(4a)。",
                "reason": "代数运算",
            },
            {
                "title": "读出顶点",
                "content": "因 a(x+b/(2a))² 在 x=−b/(2a) 处取 0（若 a>0 为最小，a<0 为最大），故顶点为 (−b/(2a), (4ac−b²)/(4a))。证毕。",
                "formula": "x_v = -b/(2a)",
                "reason": "平方项非负（或非正）时的最值",
            },
        ],
        plain_summary="顶点公式由配方法从一般式严格导出，不是硬记口诀。",
    ),
    # ── 对数法则 ──
    "t19": _entry(
        axioms=[
            {
                "name": "对数定义",
                "statement": "若 a>0,a≠1，M>0，则 log_a M = x 当且仅当 aˣ=M。",
                "plain": "对数是「问指数」的运算。",
            },
            {
                "name": "指数运算法则",
                "statement": "aᵘ·aᵛ=aᵘ⁺ᵛ（a>0）。",
                "plain": "同底数幂相乘，指数相加。",
            },
        ],
        theorem_name="对数乘法法则",
        theorem_statement="log_a(MN)=log_a M + log_a N（M,N>0）。",
        theorem_plain="积的对数等于对数的和。",
        given="a>0,a≠1，M>0，N>0。",
        to_prove="log_a(MN)=log_a M+log_a N。",
        proof=[
            {
                "title": "设指数",
                "content": "令 m=log_a M，n=log_a N，则 aᵐ=M，aⁿ=N。",
                "reason": "对数定义",
            },
            {
                "title": "相乘并用指数法则",
                "content": "MN=aᵐ·aⁿ=aᵐ⁺ⁿ。再由对数定义，log_a(MN)=m+n=log_a M+log_a N。证毕。",
                "formula": "log_a(MN)=log_a M+log_a N",
                "reason": "指数法则 + 对数定义",
            },
        ],
        plain_summary="对数法则是指数法则在「取对数」下的直接翻译。",
    ),
    # ── 斜率 ──
    "t21": _entry(
        axioms=[
            {
                "name": "直线的方向唯一性",
                "statement": "同一直线上任意两点所确定的 Δy/Δx（若存在）相同。",
                "plain": "一条直线只有一个陡峭程度。",
            }
        ],
        theorem_name="两点间的斜率公式",
        theorem_statement="过两点 (x₁,y₁)、(x₂,y₂)（x₁≠x₂）的直线斜率为 k=(y₂−y₁)/(x₂−x₁)。",
        theorem_plain="斜率=纵坐标差÷横坐标差。",
        given="两点横坐标不等。",
        to_prove="k=(y₂−y₁)/(x₂−x₁)。",
        proof=[
            {
                "title": "由定义",
                "content": "斜率定义为该直线上任意两点的 Δy/Δx。取给定两点，即得公式。",
                "formula": "k=(y₂−y₁)/(x₂−x₁)",
                "reason": "斜率定义",
            },
            {
                "title": "与点斜式一致",
                "content": "若直线过 (x₀,y₀) 且斜率为 k，则对线上任一点 (x,y) 有 (y−y₀)/(x−x₀)=k，即 y−y₀=k(x−x₀)。",
                "reason": "同一直线斜率唯一",
            },
        ],
        plain_summary="斜率公式就是定义本身在两点上的写出；点斜式由此导出。",
    ),
    # ── 导数定义 ──
    "t22": _entry(
        axioms=[
            {
                "name": "极限的定义（ε-δ 思想，初等表述）",
                "statement": "lim_{h→0} g(h)=L 表示：当 h 充分接近 0（但 h≠0）时，g(h) 可任意接近 L。",
                "plain": "无限逼近某个确定值。",
            },
            {
                "name": "平均变化率",
                "statement": "函数在 [x,x+h] 上的平均变化率为 [f(x+h)−f(x)]/h（h≠0）。",
                "plain": "这一段上的「平均陡峭程度」。",
            },
        ],
        theorem_name="导数的定义及幂函数求导（例）",
        theorem_statement="若极限 f'(x)=lim_{h→0}[f(x+h)−f(x)]/h 存在，则称 f 在 x 可导，该极限为导数值。特别地，(x²)'=2x。",
        theorem_plain="导数是平均变化率的极限；x² 的导数是 2x。",
        given="f(x)=x²。",
        to_prove="f'(x)=2x。",
        proof=[
            {
                "title": "写出差商",
                "content": "[f(x+h)−f(x)]/h = [(x+h)²−x²]/h = (x²+2xh+h²−x²)/h = 2x+h（h≠0）。",
                "formula": "[(x+h)²−x²]/h = 2x+h",
                "reason": "代数展开",
            },
            {
                "title": "取极限",
                "content": "lim_{h→0}(2x+h)=2x。故 f'(x)=2x。证毕。",
                "formula": "(x²)' = 2x",
                "reason": "极限运算法则（常数与恒等函数）",
                "graph": {
                    "expressions": [
                        {"latex": "y=x^2", "color": "#c87832"},
                        {"latex": "y=2x-1", "color": "#1a6a6a"},
                        {"latex": "(1,1)", "color": "#b84040", "pointStyle": "POINT", "pointSize": "12"},
                    ],
                    "bounds": {"left": -2, "right": 4, "bottom": -2, "top": 8},
                    "description": "几何意义：f'(1)=2 为切线斜率",
                },
            },
        ],
        plain_summary="导数由差商极限定义；对 x² 可直接算出差商再取极限得 2x。",
    ),
    # ── 导数应用 ──
    "t23": _entry(
        axioms=[
            {
                "name": "费马内部极值定理（可导情形）",
                "statement": "若 f 在开区间内点 c 取局部极值，且 f'(c) 存在，则 f'(c)=0。",
                "plain": "光滑曲线的峰顶/谷底处切线水平。",
            }
        ],
        theorem_name="可导函数极值的一阶必要条件",
        theorem_statement="局部极值点（可导）必为驻点：f'(c)=0。",
        theorem_plain="先找导数为 0 的点，再判断是否极值。",
        given="f 在 c 可导，且 c 为局部极大或极小。",
        to_prove="f'(c)=0。",
        proof=[
            {
                "title": "局部极大情形",
                "content": "存在 δ>0，使 |h|<δ 时 f(c+h)≤f(c)。则当 0<h<δ 时差商 ≤0；当 −δ<h<0 时差商 ≥0。令 h→0⁺ 与 h→0⁻，得 f'(c)≤0 且 f'(c)≥0，故 f'(c)=0。",
                "reason": "单侧极限与导数存在",
            },
            {
                "title": "局部极小同理",
                "content": "不等式反向，同样逼出 f'(c)=0。证毕。",
                "hint": "注意：f'=0 是必要非充分（如 x³ 在 0）",
            },
        ],
        plain_summary="极值点（可导时）导数必为 0；这是最优化「先求驻点」的定理依据。",
    ),
    # ── 定积分 ──
    "t24": _entry(
        axioms=[
            {
                "name": "黎曼积分定义（初等表述）",
                "statement": "若区间 [a,b] 上分割的黎曼和在网径→0 时极限存在且与取点无关，则称 f 在 [a,b] 可积，极限为 ∫_a^b f(x)dx。",
                "plain": "用无限细的矩形条面积之和逼近曲线下面积。",
            }
        ],
        theorem_name="定积分的分割求和极限表示",
        theorem_statement="∫_a^b f(x)dx = lim_{n→∞} Σ_{i=1}^n f(ξ_i)Δx（在可积条件下）。",
        theorem_plain="定积分就是黎曼和的极限。",
        given="f 在 [a,b] 连续（连续必可积）。",
        to_prove="积分等于上述极限。",
        proof=[
            {
                "title": "等分区间",
                "content": "令 Δx=(b−a)/n，分点 x_i=a+iΔx，在第 i 段取 ξ_i。黎曼和 S_n=Σ f(ξ_i)Δx。",
                "formula": "S_n = Σ f(ξ_i)Δx",
                "reason": "定义",
            },
            {
                "title": "取极限",
                "content": "由可积性（连续函数在闭区间可积），当 n→∞（分割变细）时 S_n → ∫_a^b f。证毕。",
                "formula": "∫_a^b f = lim S_n",
                "reason": "黎曼可积定义",
            },
        ],
        plain_summary="定积分由黎曼和极限定义；连续函数一定可积。",
    ),
    # ── 微积分基本定理 ──
    "t25": _entry(
        axioms=[
            {
                "name": "原函数定义",
                "statement": "若 F'=f，则称 F 为 f 的一个原函数。",
                "plain": "导数是 f 的函数叫 f 的原函数。",
            },
            {
                "name": "变上限积分的导数（可先作为引理）",
                "statement": "若 f 连续，令 G(x)=∫_a^x f(t)dt，则 G'(x)=f(x)。",
                "plain": "积分上限对 x 求导，回到被积函数。",
            },
        ],
        theorem_name="牛顿–莱布尼茨公式（微积分基本定理）",
        theorem_statement="若 f 在 [a,b] 连续，F'=f，则 ∫_a^b f(x)dx = F(b)−F(a)。",
        theorem_plain="定积分等于原函数在两端点的差。",
        given="f 连续，F'=f。",
        to_prove="∫_a^b f = F(b)−F(a)。",
        proof=[
            {
                "title": "引入变上限积分",
                "content": "令 G(x)=∫_a^x f(t)dt。由引理 G'=f。又 F'=f，故 (F−G)'=0，从而 F−G 为常数。",
                "reason": "导数为零 ⇒ 常数（微分中值/拉格朗日思想）",
            },
            {
                "title": "定出常数",
                "content": "G(a)=0，故 F(a)−G(a)=F(a)，即 F(x)−G(x)=F(a)。于是 G(x)=F(x)−F(a)。",
                "formula": "∫_a^x f = F(x)−F(a)",
                "reason": "代入 x=a",
            },
            {
                "title": "取 x=b",
                "content": "∫_a^b f = F(b)−F(a)。证毕。",
                "formula": "∫_a^b f(x)dx = F(b)−F(a)",
                "example": "∫_0^1 x² dx = [x³/3]_0^1 = 1/3",
            },
        ],
        plain_summary="微积分基本定理把「求面积」化为「求原函数再两端相减」。",
    ),
    # ── 等差数列求和 ──
    "t26": _entry(
        axioms=[
            {
                "name": "等差数列定义",
                "statement": "数列 {a_n} 满足 a_{n+1}−a_n=d（常数）对一切 n 成立，则称为公差为 d 的等差数列。",
                "plain": "相邻两项差固定。",
            }
        ],
        theorem_name="等差数列前 n 项和",
        theorem_statement="S_n = n(a_1+a_n)/2 = n[2a_1+(n−1)d]/2。",
        theorem_plain="首项加末项，乘项数，再除以 2。",
        given="a_n=a_1+(n−1)d，S_n=a_1+…+a_n。",
        to_prove="S_n=n(a_1+a_n)/2。",
        proof=[
            {
                "title": "正序与倒序相加",
                "content": "S_n=a_1+(a_1+d)+…+a_n。倒写：S_n=a_n+(a_n−d)+…+a_1。两式相加：2S_n=n(a_1+a_n)。",
                "formula": "2S_n = n(a_1+a_n)",
                "reason": "每一对对应项之和均为 a_1+a_n",
            },
            {
                "title": "除以 2",
                "content": "S_n=n(a_1+a_n)/2。再代入 a_n=a_1+(n−1)d 得另一常用形式。证毕。",
                "formula": "S_n = n(a_1+a_n)/2",
                "example": "1+…+100=100×101/2=5050",
            },
        ],
        plain_summary="等差求和公式由倒序相加法严格证明。",
    ),
    # ── 排列组合 ──
    "t28": _entry(
        axioms=[
            {
                "name": "乘法原理",
                "statement": "完成一件事分 k 个步骤，第 i 步有 n_i 种方法，则总方法数为 n_1·n_2·…·n_k。",
                "plain": "分步计数则相乘。",
            },
            {
                "name": "加法原理",
                "statement": "完成一件事有 m 类互斥方法，第 j 类有 m_j 种，则总数为 m_1+…+m_m。",
                "plain": "分类计数则相加。",
            },
        ],
        theorem_name="排列数与组合数公式",
        theorem_statement="P(n,r)=n!/(n−r)!；C(n,r)=P(n,r)/r! = n!/[r!(n−r)!]（0≤r≤n）。",
        theorem_plain="排列在乎顺序；组合不在乎，故再除以 r!。",
        given="从 n 个不同元素中取 r 个。",
        to_prove="排列、组合计数公式。",
        proof=[
            {
                "title": "推导排列数",
                "content": "第 1 位 n 种选法，第 2 位 n−1 种，…，第 r 位 n−r+1 种。由乘法原理：P(n,r)=n(n−1)…(n−r+1)=n!/(n−r)!。",
                "formula": "P(n,r)=n!/(n−r)!",
                "reason": "乘法原理",
            },
            {
                "title": "推导组合数",
                "content": "每个 r 元无序子集对应 r! 个有序排列。故 C(n,r)=P(n,r)/r!。证毕。",
                "formula": "C(n,r)=P(n,r)/r!",
                "reason": "有序与无序的倍数关系",
                "example": "C(5,3)=10，P(5,3)=60",
            },
        ],
        plain_summary="排列、组合公式由乘法原理与「有序÷r!」严格导出。",
    ),
}

TITLE_KEYWORDS = [
    ("自然数", "t1"),
    ("计数", "t1"),
    ("加法与乘法", "t2"),
    ("整式", "t7"),
    ("多项式", "t7"),
    ("一元一次", "t8"),
    ("不等式", "t9"),
    ("角与平行", "t12"),
    ("平行", "t12"),
    ("勾股", "t13"),
    ("三角形", "t13"),
    ("四边形", "t14"),
    ("多边形", "t14"),
    ("圆", "t15"),
    ("变量与函数", "t16"),
    ("一次函数", "t17"),
    ("二次函数", "t18"),
    ("指数", "t19"),
    ("对数", "t19"),
    ("斜率", "t21"),
    ("导数应用", "t23"),
    ("微积分基本", "t25"),
    ("牛顿", "t25"),
    ("导数", "t22"),
    ("积分", "t24"),
    ("数列", "t26"),
    ("排列组合", "t28"),
    ("排列", "t28"),
    ("组合", "t28"),
]

# 各主题配套数形结合图示（证明步骤缺图时自动附加）
ILLUSTRATION_GRAPHS = {
    "t1": {
        "expressions": [
            {"latex": "y=0", "color": "#888888", "lineStyle": "DASHED"},
            {"latex": "(1,0)", "color": "#c87832", "pointStyle": "POINT", "pointSize": "12", "label": "1"},
            {"latex": "(2,0)", "color": "#c87832", "pointStyle": "POINT", "pointSize": "12", "label": "2"},
            {"latex": "(3,0)", "color": "#c87832", "pointStyle": "POINT", "pointSize": "12", "label": "3"},
            {"latex": "(4,0)", "color": "#c87832", "pointStyle": "POINT", "pointSize": "12", "label": "4"},
            {"latex": "(5,0)", "color": "#c87832", "pointStyle": "POINT", "pointSize": "12", "label": "5"},
        ],
        "bounds": {"left": -1, "right": 7, "bottom": -1.5, "top": 1.5},
        "description": "数轴上的后继：1→2→3→…",
    },
    "t2": {
        "expressions": [
            {"latex": "y=0", "color": "#888888", "lineStyle": "DASHED"},
            {"latex": "segment((0,0),(3,0))", "color": "#1a6a6a", "lineWidth": "4", "label": "a=3"},
            {"latex": "segment((3,0),(5,0))", "color": "#c87832", "lineWidth": "4", "label": "b=2"},
            {"latex": "(0,0)", "color": "#333333", "pointStyle": "POINT", "pointSize": "8"},
            {"latex": "(3,0)", "color": "#1a6a6a", "pointStyle": "POINT", "pointSize": "10", "label": "3"},
            {"latex": "(5,0)", "color": "#c87832", "pointStyle": "POINT", "pointSize": "10", "label": "5"},
        ],
        "bounds": {"left": -1, "right": 7, "bottom": -1.5, "top": 1.5},
        "description": "数轴上 3+2=5：先走 a 再走 b",
    },
    "t7": {
        "expressions": [
            {"latex": "segment((0,0),(6,0))", "color": "#888888", "lineWidth": "2"},
            {"latex": "segment((0,0),(0,3))", "color": "#888888", "lineWidth": "2"},
            {"latex": "segment((6,0),(6,3))", "color": "#888888", "lineWidth": "2"},
            {"latex": "segment((0,3),(6,3))", "color": "#888888", "lineWidth": "2"},
            {"latex": "segment((4,0),(4,3))", "color": "#c87832", "lineWidth": "2", "lineStyle": "DASHED"},
            {"latex": "(2,1.5)", "color": "#1a6a6a", "pointStyle": "POINT", "pointSize": "1", "label": "a×b"},
            {"latex": "(5,1.5)", "color": "#c87832", "pointStyle": "POINT", "pointSize": "1", "label": "a×c"},
        ],
        "bounds": {"left": -1, "right": 8, "bottom": -1, "top": 5},
        "description": "面积模型：a(b+c)=ab+ac",
    },
    "t12": {
        "expressions": [
            {"latex": "y=1", "color": "#1a6a6a", "lineWidth": "3", "label": "a"},
            {"latex": "y=-1", "color": "#1a6a6a", "lineWidth": "3", "label": "b∥a"},
            {"latex": "y=0.5x", "color": "#c87832", "lineWidth": "2", "label": "截线 t"},
        ],
        "bounds": {"left": -5, "right": 5, "bottom": -3, "top": 3},
        "description": "两平行线被截线所截（同位角示意）",
    },
    "t13": {
        "expressions": [
            {"latex": "segment((0,0),(4,0))", "color": "#1a6a6a", "lineWidth": "3", "label": "a=4"},
            {"latex": "segment((4,0),(4,3))", "color": "#2a7a4a", "lineWidth": "3", "label": "b=3"},
            {"latex": "segment((0,0),(4,3))", "color": "#c87832", "lineWidth": "3", "label": "c=5"},
            {"latex": "(0,0)", "color": "#333333", "pointStyle": "POINT", "pointSize": "10", "label": "C"},
            {"latex": "(4,0)", "color": "#333333", "pointStyle": "POINT", "pointSize": "10", "label": "B"},
            {"latex": "(4,3)", "color": "#333333", "pointStyle": "POINT", "pointSize": "10", "label": "A"},
        ],
        "bounds": {"left": -1, "right": 6, "bottom": -1, "top": 5},
        "description": "直角三角形 3-4-5：a²+b²=c²",
    },
    "t14": {
        "expressions": [
            {"latex": "segment((0,0),(4,0))", "color": "#1a6a6a", "lineWidth": "2"},
            {"latex": "segment((4,0),(5,3))", "color": "#1a6a6a", "lineWidth": "2"},
            {"latex": "segment((5,3),(1,4))", "color": "#1a6a6a", "lineWidth": "2"},
            {"latex": "segment((1,4),(0,0))", "color": "#1a6a6a", "lineWidth": "2"},
            {"latex": "segment((0,0),(5,3))", "color": "#c87832", "lineWidth": "2", "lineStyle": "DASHED", "label": "对角线"},
            {"latex": "(0,0)", "color": "#333333", "pointStyle": "POINT", "pointSize": "8", "label": "A"},
            {"latex": "(4,0)", "color": "#333333", "pointStyle": "POINT", "pointSize": "8", "label": "B"},
            {"latex": "(5,3)", "color": "#333333", "pointStyle": "POINT", "pointSize": "8", "label": "C"},
            {"latex": "(1,4)", "color": "#333333", "pointStyle": "POINT", "pointSize": "8", "label": "D"},
        ],
        "bounds": {"left": -1, "right": 7, "bottom": -1, "top": 5.5},
        "description": "四边形由一条对角线分成 2 个三角形 → 内角和 360°",
    },
    "t15": {
        "expressions": [
            {"latex": "y=sqrt(4-x^2)", "color": "#c87832", "lineWidth": "2.5"},
            {"latex": "y=-sqrt(4-x^2)", "color": "#c87832", "lineWidth": "2.5"},
            {"latex": "(0,0)", "color": "#1a6a6a", "pointStyle": "POINT", "pointSize": "10", "label": "O"},
            {"latex": "segment((0,0),(2,0))", "color": "#1a6a6a", "lineWidth": "2", "label": "r"},
        ],
        "bounds": {"left": -3, "right": 3, "bottom": -3, "top": 3},
        "description": "圆：到定点距离为定长 r",
    },
    "t16": {
        "expressions": [
            {"latex": "y=x^2", "color": "#2a7a4a", "label": "函数"},
            {"latex": "y=sqrt(1-x^2)", "color": "#b84040", "label": "上半圆"},
            {"latex": "y=-sqrt(1-x^2)", "color": "#b84040", "label": "下半圆"},
            {"latex": "x=0.5", "color": "#888888", "lineStyle": "DASHED"},
        ],
        "bounds": {"left": -2, "right": 2, "bottom": -2, "top": 3},
        "description": "垂直线检验：抛物线过关，整圆不过关",
    },
    "t17": {
        "expressions": [
            {"latex": "y=2x+1", "color": "#c87832", "label": "y=2x+1"},
            {"latex": "y=-x+3", "color": "#1a6a6a", "label": "y=-x+3"},
            {"latex": "(0,1)", "color": "#c87832", "pointStyle": "POINT", "pointSize": "10", "label": "截距1"},
        ],
        "bounds": {"left": -4, "right": 4, "bottom": -4, "top": 6},
        "description": "一次函数图像是直线",
    },
    "t18": {
        "expressions": [
            {"latex": "y=x^2-4x+3", "color": "#c87832"},
            {"latex": "x=2", "color": "#1a6a6a", "lineStyle": "DASHED", "label": "对称轴"},
            {"latex": "(2,-1)", "color": "#b84040", "pointStyle": "POINT", "pointSize": "12", "label": "顶点"},
        ],
        "bounds": {"left": -1, "right": 5, "bottom": -3, "top": 6},
        "description": "二次函数抛物线与顶点",
    },
    "t19": {
        "expressions": [
            {"latex": "y=2^x", "color": "#c87832", "label": "y=2^x"},
            {"latex": "y=x", "color": "#888888", "lineStyle": "DASHED", "label": "y=x"},
            {"latex": "(1,2)", "color": "#1a6a6a", "pointStyle": "POINT", "pointSize": "10", "label": "(1,2)"},
            {"latex": "(2,4)", "color": "#1a6a6a", "pointStyle": "POINT", "pointSize": "10", "label": "(2,4)"},
        ],
        "bounds": {"left": -2, "right": 4, "bottom": -1, "top": 8},
        "description": "指数函数 y=2^x（对数是其反运算）",
    },
    "t21": {
        "expressions": [
            {"latex": "y=0.75x+1", "color": "#c87832"},
            {"latex": "(0,1)", "color": "#1a6a6a", "pointStyle": "POINT", "pointSize": "10", "label": "(0,1)"},
            {"latex": "(4,4)", "color": "#1a6a6a", "pointStyle": "POINT", "pointSize": "10", "label": "(4,4)"},
            {"latex": "segment((0,1),(4,1))", "color": "#888888", "lineStyle": "DASHED", "label": "Δx"},
            {"latex": "segment((4,1),(4,4))", "color": "#888888", "lineStyle": "DASHED", "label": "Δy"},
        ],
        "bounds": {"left": -1, "right": 6, "bottom": -1, "top": 6},
        "description": "斜率 k=Δy/Δx",
    },
    "t22": {
        "expressions": [
            {"latex": "y=x^2", "color": "#c87832"},
            {"latex": "y=2x-1", "color": "#1a6a6a", "label": "切线"},
            {"latex": "(1,1)", "color": "#b84040", "pointStyle": "POINT", "pointSize": "12", "label": "切点"},
        ],
        "bounds": {"left": -2, "right": 4, "bottom": -2, "top": 8},
        "description": "导数的几何意义：切线斜率",
    },
    "t23": {
        "expressions": [
            {"latex": "y=x^3-3x", "color": "#c87832"},
            {"latex": "(-1,2)", "color": "#2a7a4a", "pointStyle": "POINT", "pointSize": "12", "label": "极大"},
            {"latex": "(1,-2)", "color": "#b84040", "pointStyle": "POINT", "pointSize": "12", "label": "极小"},
            {"latex": "y=0", "color": "#888888", "lineStyle": "DASHED"},
        ],
        "bounds": {"left": -3, "right": 3, "bottom": -5, "top": 5},
        "description": "驻点（导数为 0）与极值",
    },
    "t24": {
        "expressions": [
            {"latex": "y=x^2/4", "color": "#c87832"},
            {"latex": "x=0", "color": "#888888", "lineStyle": "DASHED"},
            {"latex": "x=4", "color": "#888888", "lineStyle": "DASHED"},
            {"latex": "y=0", "color": "#888888", "lineStyle": "DASHED"},
        ],
        "bounds": {"left": -1, "right": 5, "bottom": -1, "top": 5},
        "description": "定积分：曲线下面积（黎曼和思想）",
    },
    "t25": {
        "expressions": [
            {"latex": "y=x^2", "color": "#c87832", "label": "f(x)=x^2"},
            {"latex": "y=x^3/3", "color": "#1a6a6a", "label": "F(x)=x^3/3"},
            {"latex": "(1,1)", "color": "#b84040", "pointStyle": "POINT", "pointSize": "10"},
            {"latex": "(1,0.333)", "color": "#2a7a4a", "pointStyle": "POINT", "pointSize": "10"},
        ],
        "bounds": {"left": -0.5, "right": 2, "bottom": -0.5, "top": 2},
        "description": "原函数与微积分基本定理示意",
    },
    "t26": {
        "expressions": [
            {"latex": "(1,2)", "color": "#c87832", "pointStyle": "POINT", "pointSize": "10", "label": "a1"},
            {"latex": "(2,5)", "color": "#c87832", "pointStyle": "POINT", "pointSize": "10", "label": "a2"},
            {"latex": "(3,8)", "color": "#c87832", "pointStyle": "POINT", "pointSize": "10", "label": "a3"},
            {"latex": "(4,11)", "color": "#c87832", "pointStyle": "POINT", "pointSize": "10", "label": "a4"},
            {"latex": "y=3x-1", "color": "#1a6a6a", "lineStyle": "DASHED", "label": "通项趋势"},
        ],
        "bounds": {"left": 0, "right": 6, "bottom": 0, "top": 14},
        "description": "等差数列在坐标系中的点列",
    },
}


def lookup_bank(topic_id: str = None, topic_title: str = None) -> Optional[dict]:
    if topic_id and topic_id in BANK:
        return _with_illustration(topic_id, BANK[topic_id])
    title = topic_title or ""
    for kw, tid in TITLE_KEYWORDS:
        if kw in title and tid in BANK:
            return _with_illustration(tid, BANK[tid])
    return None


def _with_illustration(topic_id: str, entry: dict) -> dict:
    """若证明步骤中没有任何图形，附加一条数形结合图示步骤。"""
    import copy

    entry = copy.deepcopy(entry)
    proof = entry.get("proof") or entry.get("steps") or []
    has_graph = any(isinstance(s, dict) and s.get("graph") for s in proof)
    illus = ILLUSTRATION_GRAPHS.get(topic_id)
    if illus and not has_graph:
        proof.append(
            {
                "title": "图示",
                "content": "坐标系中标出与上述命题相关的几何对象或函数图像。",
                "reason": "对照陈述与图形",
                "graph": illus,
            }
        )
        entry["proof"] = proof
        entry["steps"] = proof
    elif illus and has_graph:
        # 已有图也保证至少一份完整图示在末尾（若最后一步无图则补）
        if not (proof and proof[-1].get("graph")):
            proof.append(
                {
                    "title": "图示",
                    "content": "坐标系中标出与上述命题相关的对象。",
                    "reason": "对照陈述与图形",
                    "graph": illus,
                }
            )
            entry["proof"] = proof
            entry["steps"] = proof
    return entry


def ensure_content_has_graph(parsed: dict, topic_id: str = None, topic_title: str = None) -> dict:
    """AI 返回若完全无图，从题库插图补上。"""
    if not isinstance(parsed, dict):
        return parsed
    proof = parsed.get("proof") or parsed.get("steps") or []
    if any(isinstance(s, dict) and s.get("graph") for s in proof):
        return parsed
    tid = topic_id
    if not tid:
        for kw, t in TITLE_KEYWORDS:
            if topic_title and kw in topic_title:
                tid = t
                break
    illus = ILLUSTRATION_GRAPHS.get(tid) if tid else None
    if not illus:
        return parsed
    proof = list(proof)
    proof.append(
        {
            "title": "图示",
            "content": "坐标系中标出与本定理相关的对象。",
            "reason": "对照陈述与图形",
            "graph": illus,
        }
    )
    parsed["proof"] = proof
    parsed["steps"] = proof
    return parsed


def bank_as_prompt_context(entry: dict) -> str:
    if not entry:
        return ""
    lines = [
        "【必须按真正的数学公理/定理/证明来写——不要只讲故事】",
        "下列内容供你对齐与展开；证明步骤要有「依据」（用了哪条公理/定义/已证定理）。",
    ]
    for ax in entry.get("axioms") or []:
        lines.append(
            f"- 公理「{ax.get('name','')}」：{ax.get('statement','')}"
            + (f"（说明：{ax.get('plain','')}）" if ax.get("plain") else "")
        )
    th = entry.get("theorem") or {}
    lines.append(f"- 定理「{th.get('name','')}」：{th.get('statement','')}")
    if entry.get("given"):
        lines.append(f"- 已知：{entry['given']}")
    if entry.get("to_prove"):
        lines.append(f"- 求证：{entry['to_prove']}")
    proof = entry.get("proof") or entry.get("steps") or []
    if proof:
        lines.append("- 证明提纲：")
        for i, p in enumerate(proof[:6], 1):
            lines.append(f"  {i}. {p.get('title','')}: {p.get('content','')[:120]}")
            if p.get("reason"):
                lines.append(f"     依据：{p['reason']}")
    return "\n".join(lines)


def bank_as_json(entry: dict) -> str:
    return json.dumps(entry, ensure_ascii=False)
