# 数学第一性原理学习系统

从第一性原理出发，通过推导式学习数学。覆盖从算术到微积分的 30 个主题，6 个阶段。

## 架构

```
├── backend/           # Python Flask + SQLite API 服务
├── frontend/          # Web 前端（Vanilla HTML/CSS/JS + Desmos）
├── miniprogram/       # 微信小程序端
└── ARCHITECTURE.md    # 业务架构图 + 系统架构图（Mermaid）
```

## 快速开始

### 1. 启动后端

```bash
cd backend
pip install -r requirements.txt
python main.py
```

后端运行在 `http://localhost:8088`（与 `main.py` / 前端 `api.js` 一致）

### 2. 打开 Web 前端

浏览器打开 `http://localhost:8088`（Flask 自动托管前端静态文件）

或者直接打开 `frontend/index.html`（此时 API 仍指向 `http://localhost:8088`）

### 3. 微信小程序

1. 打开微信开发者工具
2. 导入 `miniprogram/` 目录
3. 在 `miniprogram/app.js` 中设置 `baseUrl` 为后端地址（如 `http://localhost:8088`）
4. 在 `project.config.json` 中填入你的 AppID

## 功能

- **推导式学习**：每个概念从第一性原理出发，逐步推导
- **30 个主题**：数的起源 → 代数语言 → 几何直觉 → 函数世界 → 变化的科学 → 抽象与推理
- **交互式测验**：选择题、填空题、推导评判、图形操作
- **Desmos 绘图**：Web 端嵌入 Desmos 计算器，实时函数绘图
- **AI 推导**：形式化公理/定理陈述 + 逐步证明（含依据）；禁止套话；无 Key 时用内置证明库
- **进度同步**：用户账户 + 云端进度存储
- **错题本**：自动记录错题，支持复习
- **学习统计**：学习会话、日/周汇总、主题掌握度
- **成就与积分**：成就解锁、积分、排行榜、连续打卡
- **收藏与笔记**：主题收藏、学习笔记 CRUD
- **学习路径**：推荐路径、弱项分析、生成个性化路径
- **多端支持**：Web + 微信小程序（小程序功能面可能少于 Web）

## 环境变量

| 变量 | 说明 | 默认值 |
|------|------|--------|
| `AI_API_KEY` | 小米 MiMo API Key | （空） |
| `AI_BASE_URL` | API 端点 | https://token-plan-cn.xiaomimimo.com/v1 |
| `AI_MODEL` | 模型名称 | mimo-v2.5 |
| `MATH_SECRET_KEY` | JWT 密钥 | dev-secret |

### 配置小米 MiMo AI

1. 访问 https://mimo.mi.com 注册账号
2. 进入 Token Plan 页面获取 API Key
3. 设置环境变量：

```bash
# Windows
set AI_API_KEY=your-api-key

# Linux/Mac
export AI_API_KEY=your-api-key
```

或创建 `.env` 文件（参考 `.env.example`）。

## 技术栈

- **前端**：Vanilla HTML/CSS/JS + Desmos API
- **后端**：Python Flask + SQLite
- **AI**：OpenAI 兼容 API（默认小米 MiMo `mimo-v2.5`）
- **小程序**：微信小程序原生框架

## API 端点

| 方法 | 路径 | 认证 | 说明 |
|------|------|------|------|
| GET | `/api/health` | 否 | 健康检查 |
| POST | `/api/auth/register` | 否 | 用户注册 |
| POST | `/api/auth/login` | 否 | 用户登录 |
| GET | `/api/auth/me` | 是 | 获取当前用户 |
| GET | `/api/topics` | 否 | 主题列表 |
| GET | `/api/topics/<id>` | 否 | 主题详情 |
| GET | `/api/progress` | 是 | 学习进度 |
| POST | `/api/progress` | 是 | 更新进度 |
| GET | `/api/wrong-answers` | 是 | 错题列表 |
| POST | `/api/wrong-answers` | 是 | 添加错题 |
| DELETE | `/api/wrong-answers/<id>` | 是 | 删除错题 |
| POST | `/api/ai/derive` | 是 | AI 推导 |
| POST | `/api/ai/quiz` | 是 | AI 出题 |
| POST | `/api/ai/explain` | 是 | AI 解释 |
| GET | `/api/placement/questions` | 否 | 定位测试题 |
| POST | `/api/placement/submit` | 是 | 提交定位测试 |
| POST | `/api/stats/session/start` | 是 | 开始学习会话 |
| POST | `/api/stats/session/end` | 是 | 结束学习会话 |
| GET | `/api/stats/summary` | 是 | 学习统计摘要 |
| GET | `/api/stats/daily` | 是 | 日统计 |
| GET | `/api/stats/weekly` | 是 | 周统计 |
| GET | `/api/stats/topic-mastery` | 是 | 主题掌握度 |
| POST | `/api/stats/record-quiz` | 是 | 记录测验结果 |
| GET | `/api/achievements` | 否 | 成就定义列表 |
| GET | `/api/achievements/user` | 是 | 用户已获成就 |
| POST | `/api/achievements/check` | 是 | 检查并解锁成就 |
| GET | `/api/achievements/leaderboard` | 否 | 积分排行榜 |
| GET | `/api/points` | 是 | 当前积分 |
| GET | `/api/points/history` | 是 | 积分历史 |
| GET | `/api/streak` | 是 | 连续学习天数 |
| GET | `/api/favorites` | 是 | 收藏列表 |
| POST | `/api/favorites` | 是 | 添加收藏 |
| DELETE | `/api/favorites/<topic_id>` | 是 | 取消收藏 |
| GET | `/api/favorites/check/<topic_id>` | 是 | 是否已收藏 |
| GET | `/api/notes` | 是 | 笔记列表 |
| POST | `/api/notes` | 是 | 新增笔记 |
| PUT | `/api/notes/<id>` | 是 | 更新笔记 |
| DELETE | `/api/notes/<id>` | 是 | 删除笔记 |
| GET | `/api/paths/recommend` | 是 | 推荐学习路径 |
| POST | `/api/paths/generate` | 是 | 生成个性化路径 |
| GET | `/api/paths/current` | 是 | 当前学习路径 |
| GET | `/api/paths/weak-areas` | 是 | 弱项分析 |

## 下一步可选方向（待你选定）

完成文档对齐后，常见后续工作任选其一即可继续开发：

1. **本地演示**：启动后端，走一遍注册 → 定位测试 → 学主题 → 测验全流程  
2. **小程序同步**：把 Web 端统计/成就/收藏/路径能力同步到 `miniprogram/`  
3. **某一功能深挖**：例如成就规则、路径推荐算法、或 AI 无 Key 时的体验优化  
4. **测试完善**：扩展 `test_api.py` 覆盖新蓝图接口  

请直接说选哪一项（或描述你想改的问题），即可开工。

## 会话总结（累积）

### 2026-07-19 — 项目理解总览 & 文档对齐

- **会话主要目的**：读懂工作区与主产品结构，并落实计划中的文档对齐待办  
- **完成的主要任务**：梳理 `claude-howto`（PDF 脚本 + `math-learning-system`）；将 README / ARCHITECTURE / `test_api.py` 与代码对齐（端口 `8088`、MiMo AI、新 API）  
- **关键决策和解决方案**：以 `main.py` 的 `8088` 为准修正文档；API 表补全 stats / achievements / favorites / paths；在 README 列出「下一步可选方向」供选定后实现  
- **使用的技术栈**：Flask、SQLite、Vanilla JS、Desmos、OpenAI 兼容 API（MiMo）、Markdown 文档  
- **修改了哪些文件**：
  - `math-learning-system/README.md`
  - `math-learning-system/ARCHITECTURE.md`
  - `math-learning-system/test_api.py`

### 2026-07-19 — 优化 AI 推导（公理/定理通俗化）

- **会话主要目的**：让 AI 推导明确给出主要公理与定理，并用白话逐步推出结论  
- **完成的主要任务**：新建公理/定理通俗库；升级 AI 提示词与离线回退；前端分块展示；缓存版本 bump 为 derive-v2  
- **关键决策和解决方案**：双通道（有 API 注入库要点生成 / 无 API 直接返回库）；JSON 结构统一含 axioms、theorem、analogy、steps、plain_summary；旧缓存通过 hash 版本失效  
- **使用的技术栈**：Python Flask、内置知识库、OpenAI 兼容 API、Vanilla JS、CSS  
- **修改了哪些文件**：
  - `math-learning-system/backend/services/axiom_theorem_bank.py`（新建）
  - `math-learning-system/backend/services/ai_service.py`
  - `math-learning-system/backend/blueprints/ai_bp.py`
  - `math-learning-system/frontend/js/ai-derive.js`
  - `math-learning-system/frontend/css/style.css`
  - `math-learning-system/frontend/index.html`
  - `math-learning-system/README.md`

### 2026-07-19 — 纠正为「公理/定理 + 证明过程」

- **会话主要目的**：按用户澄清，AI 推导应呈现真正的数学公理、定理及其证明，而非仅生活化讲解  
- **完成的主要任务**：重写公理/定理库为形式陈述 + 已知/求证 + 带「依据」的证明步骤；升级 AI 提示词与缓存 derive-v3；前端优先展示证明过程  
- **关键决策和解决方案**：proof 为主、analogy 标为「非证明」；steps 与 proof 同步以兼容旧逻辑  
- **使用的技术栈**：Python 知识库、Flask AI 服务、Vanilla JS/CSS  
- **修改了哪些文件**：
  - `backend/services/axiom_theorem_bank.py`
  - `backend/services/ai_service.py`
  - `frontend/js/ai-derive.js`
  - `frontend/css/style.css`
  - `frontend/index.html`
  - `README.md`

### 2026-07-19 — 修复 AI 推导缺图

- **会话主要目的**：用户反馈 AI 推导页面看不到图形  
- **完成的主要任务**：为各主题补全数形结合图示；证明无图时自动附加图示步骤；增强 SVG 解析（隐式乘法、segment 线段）；延后渲染避免宽度为 0；缓存 bump 为 derive-v4  
- **关键决策和解决方案**：ILLUSTRATION_GRAPHS + ensure_content_has_graph，保证有库主题必有图  
- **使用的技术栈**：SVG Graph、Flask、Vanilla JS  
- **修改了哪些文件**：
  - `backend/services/axiom_theorem_bank.py`
  - `backend/services/ai_service.py`
  - `frontend/js/graph.js`
  - `frontend/js/ai-derive.js`
  - `README.md`

### 2026-07-19 — 导航栏移到左侧（已撤销）

- 已按用户要求撤销左侧栏，改回顶部导航并做手机适配。

### 2026-07-19 — 优化顶部导航（手机适配）

- **会话主要目的**：撤销左侧栏；保留顶部导航并适配手机  
- **完成的主要任务**：恢复顶栏结构；小屏用汉堡菜单展开/收起；增大触控面积（约 44px）；点击菜单项后自动收起  
- **关键决策和解决方案**：桌面仍横向展示菜单；≤768px 默认折叠，避免顶栏拥挤  
- **使用的技术栈**：HTML / CSS / 少量 JS  
- **修改了哪些文件**：
  - `frontend/index.html`
  - `frontend/css/style.css`
  - `README.md`

### 2026-07-19 — 全链路禁止套话

- **会话主要目的**：所有说明改为严谨数学表述，禁止励志/空话  
- **完成的主要任务**：重写 AI 提示词与清洗器；删除旧通用套话回退大段；前端去掉「白话/回顾/直觉辅助」话术；缓存 derive-v6  
- **关键决策和解决方案**：只输出公理/定理/证明/公式；套话命中则 scrub 或回退题库  
- **使用的技术栈**：Python / Vanilla JS  
- **修改了哪些文件**：
  - `backend/services/ai_service.py`
  - `backend/services/axiom_theorem_bank.py`
  - `backend/seed_data_derive.py`
  - `frontend/js/ai-derive.js`
  - `frontend/js/achievements.js`
  - `frontend/index.html`
  - `README.md`

### 2026-07-19 — 上传 GitHub

- **会话主要目的**：将本地改动提交并推送到 GitHub  
- **完成的主要任务**：提交并 push 至 `origin/master`（仓库 math-first-principles）  
- **关键决策和解决方案**：一次提交包含公理证明库、严谨 AI 推导、手机顶栏与文档对齐  
- **使用的技术栈**：Git / GitHub  
- **修改了哪些文件**：已推送至远程，见提交 `e1b9a95`

- **会话主要目的**：排查无法打开学习系统  
- **完成的主要任务**：确认代码可导入；发现 8088 无进程；已重新启动 Flask  
- **关键决策和解决方案**：访问地址为 `http://localhost:8088`（需先 `python main.py`）  
- **使用的技术栈**：Flask  
- **修改了哪些文件**：无代码修改（仅启动服务）

- **会话主要目的**：去掉「数学大厦/知识网络」等空话；为四边形补正式证明  
- **完成的主要任务**：新增 t14 多边形内角和证明；删除通用套话模板  
- **修改了哪些文件**：`axiom_theorem_bank.py`、`ai_service.py`、`README.md`
