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

后端运行在 `http://localhost:8000`

### 2. 打开 Web 前端

浏览器打开 `http://localhost:8000`（Flask 自动托管前端静态文件）

或者直接打开 `frontend/index.html`

### 3. 微信小程序

1. 打开微信开发者工具
2. 导入 `miniprogram/` 目录
3. 在 `miniprogram/app.js` 中设置 `baseUrl` 为后端地址
4. 在 `project.config.json` 中填入你的 AppID

## 功能

- **推导式学习**：每个概念从第一性原理出发，逐步推导
- **30 个主题**：数的起源 → 代数语言 → 几何直觉 → 函数世界 → 变化的科学 → 抽象与推理
- **交互式测验**：选择题、填空题、推导评判、图形操作
- **Desmos 绘图**：Web 端嵌入 Desmos 计算器，实时函数绘图
- **AI 推导**：使用 OpenAI API 生成第一性原理推导过程
- **进度同步**：用户账户 + 云端进度存储
- **错题本**：自动记录错题，支持复习
- **多端支持**：Web + 微信小程序

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
- **AI**：OpenAI API
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
