# 数学第一性原理学习系统 — 架构文档

## 一、业务架构图

```mermaid
graph TB
    subgraph 用户层
        U1[学生用户]
        U2[教师/管理员]
    end

    subgraph 业务域
        direction TB
        subgraph 学习域
            B1[推导式学习]
            B2[交互式测验]
            B3[Desmos 绘图]
        end
        subgraph 评估域
            B4[定位测试]
            B5[进度追踪]
            B6[错题本]
        end
        subgraph 智能域
            B7[AI 推导生成]
            B8[AI 错题解释]
            B9[AI 出题]
        end
        subgraph 用户域
            B10[注册/登录]
            B11[个人信息]
        end
    end

    subgraph 内容域
        C1[30 个数学主题]
        C2[6 个学习阶段]
        C3[课程章节]
        C4[题库]
    end

    U1 --> B10
    U1 --> B1
    U1 --> B2
    U1 --> B4
    U1 --> B5
    U1 --> B6
    U1 --> B3

    B1 --> C1
    B2 --> C4
    B4 --> C2
    B5 --> C1

    B1 --> B7
    B2 --> B9
    B6 --> B8

    B7 --> C3
    B9 --> C4
```

### 业务流程

```mermaid
flowchart LR
    A[新用户访问] --> B{已有账号?}
    B -->|否| C[注册账号]
    B -->|是| D[登录]
    C --> D
    D --> E{选择学习路径}
    E -->|定位测试| F[完成测试] --> G[推荐阶段]
    E -->|自由浏览| H[浏览主题列表]
    G --> H
    H --> I[选择主题]
    I --> J[学习推导过程]
    J --> K[Desmos 交互绘图]
    K --> L[完成测验]
    L --> M{通过?}
    M -->|是| N[获得星星 + 进入下一主题]
    M -->|否| O[查看错题解释]
    O --> P[AI 生成解释]
    P --> J
    N --> Q{还有更多主题?}
    Q -->|是| H
    Q -->|否| R[完成学习]
```

---

## 二、系统架构图

```mermaid
graph TB
    subgraph 客户端
        direction LR
        FW[Web 前端<br/>Vanilla HTML/CSS/JS]
        MP[微信小程序]
        DM[Desmos 绘图引擎]
    end

    subgraph Flask 后端
        direction TB
        subgraph API 层
            R1[auth_bp<br/>/api/auth/*]
            R2[content_bp<br/>/api/topics/*]
            R3[progress_bp<br/>/api/progress/*<br/>/api/wrong-answers/*]
            R4[ai_bp<br/>/api/ai/*]
            R5[placement_bp<br/>/api/placement/*]
            R6[health<br/>/api/health]
            R7[stats_bp<br/>/api/stats/*]
            R8[achievements_bp<br/>/api/achievements/*]
            R9[favorites_bp<br/>/api/favorites/*<br/>/api/notes/*]
            R10[paths_bp<br/>/api/paths/*]
        end
        subgraph 中间件
            MW1[CORS 跨域]
            MW2[JWT 认证<br/>@login_required]
        end
        subgraph 服务层
            SV1[ai_service<br/>OpenAI兼容_MiMo]
            SV2[stats_service]
            SV3[achievements_service]
            SV4[paths_service]
        end
        subgraph 数据层
            DB[(SQLite<br/>math_learning.db)]
        end
    end

    subgraph 外部服务
        EXT1[MiMo_API<br/>mimo-v2.5]
    end

    FW -->|HTTP| MW1
    MP -->|HTTP| MW1
    MW1 --> R1 & R2 & R3 & R4 & R5 & R6 & R7 & R8 & R9 & R10
    R1 & R3 & R4 & R5 & R7 & R8 & R9 & R10 --> MW2
    MW2 --> DB
    R2 --> DB
    R6 --> DB
    R4 --> SV1
    R7 --> SV2
    R8 --> SV3
    R10 --> SV4
    SV1 --> EXT1
    FW --> DM
```

### 技术分层

```mermaid
graph LR
    subgraph 展示层
        L1[HTML 页面]
        L2[CSS 样式]
        L3[JavaScript 逻辑]
        L4[Desmos API]
    end

    subgraph 接口层
        L5[RESTful API<br/>16 个端点]
        L6[JWT 令牌认证]
    end

    subgraph 业务层
        L7[用户管理]
        L8[内容管理]
        L9[进度管理]
        L10[AI 生成]
        L11[定位评估]
    end

    subgraph 数据层
        L12[SQLite 数据库<br/>8 张表]
        L13[AI 内容缓存]
    end

    L1 & L2 & L3 --> L5
    L4 --> L5
    L5 --> L6
    L6 --> L7 & L8 & L9 & L10 & L11
    L7 & L8 & L9 & L10 & L11 --> L12
    L10 --> L13
```

---

## 三、数据模型

```mermaid
erDiagram
    users {
        int id PK
        string username UK
        string email UK
        string password_hash
        timestamp created_at
    }

    topics {
        string id PK
        string stage
        int stage_index
        string title
        string description
        string icon
        int sort_order
    }

    progress {
        int id PK
        int user_id FK
        string topic_id FK
        int stars
        int tests_taken
        int tests_passed
        int best_score
        timestamp completed_at
    }

    wrong_answers {
        int id PK
        int user_id FK
        string topic_id
        string question
        string user_answer
        string correct_answer
        string explanation
        timestamp created_at
    }

    lesson_sections {
        int id PK
        string topic_id FK
        string section_type
        string content
        int sort_order
    }

    quiz_questions {
        int id PK
        string topic_id FK
        string question
        string options
        int answer
        string explanation
        int sort_order
    }

    placement_questions {
        int id PK
        int stage_index
        int difficulty
        string question
        string options
        int answer
        string explanation
        int sort_order
    }

    ai_content_cache {
        int id PK
        string topic_id FK
        string prompt_hash
        string content
        timestamp created_at
    }

    users ||--o{ progress : "has"
    users ||--o{ wrong_answers : "has"
    topics ||--o{ progress : "tracked by"
    topics ||--o{ lesson_sections : "has"
    topics ||--o{ quiz_questions : "has"
    topics ||--o{ ai_content_cache : "cached for"
```

---

## 四、API 端点总览

| 模块 | 方法 | 路径 | 认证 | 说明 |
|------|------|------|------|------|
| 健康检查 | GET | `/api/health` | 否 | 服务状态 |
| 认证 | POST | `/api/auth/register` | 否 | 用户注册 |
| 认证 | POST | `/api/auth/login` | 否 | 用户登录 |
| 认证 | GET | `/api/auth/me` | 是 | 当前用户信息 |
| 内容 | GET | `/api/topics` | 否 | 主题列表 |
| 内容 | GET | `/api/topics/<id>` | 否 | 主题详情+课程+测验 |
| 进度 | GET | `/api/progress` | 是 | 学习进度列表 |
| 进度 | POST | `/api/progress` | 是 | 更新学习进度 |
| 错题 | GET | `/api/wrong-answers` | 是 | 错题列表 |
| 错题 | POST | `/api/wrong-answers` | 是 | 添加错题 |
| 错题 | DELETE | `/api/wrong-answers/<id>` | 是 | 删除错题 |
| AI | POST | `/api/ai/derive` | 是 | AI 推导生成 |
| AI | POST | `/api/ai/quiz` | 是 | AI 出题 |
| AI | POST | `/api/ai/explain` | 是 | AI 错题解释 |
| 定位 | GET | `/api/placement/questions` | 否 | 定位测试题 |
| 定位 | POST | `/api/placement/submit` | 是 | 提交定位测试 |
| 统计 | POST | `/api/stats/session/start` | 是 | 开始学习会话 |
| 统计 | POST | `/api/stats/session/end` | 是 | 结束学习会话 |
| 统计 | GET | `/api/stats/summary` | 是 | 学习统计摘要 |
| 统计 | GET | `/api/stats/daily` | 是 | 日统计 |
| 统计 | GET | `/api/stats/weekly` | 是 | 周统计 |
| 统计 | GET | `/api/stats/topic-mastery` | 是 | 主题掌握度 |
| 统计 | POST | `/api/stats/record-quiz` | 是 | 记录测验结果 |
| 成就 | GET | `/api/achievements` | 否 | 成就定义列表 |
| 成就 | GET | `/api/achievements/user` | 是 | 用户已获成就 |
| 成就 | POST | `/api/achievements/check` | 是 | 检查并解锁成就 |
| 成就 | GET | `/api/achievements/leaderboard` | 否 | 积分排行榜 |
| 积分 | GET | `/api/points` | 是 | 当前积分 |
| 积分 | GET | `/api/points/history` | 是 | 积分历史 |
| 积分 | GET | `/api/streak` | 是 | 连续学习天数 |
| 收藏 | GET | `/api/favorites` | 是 | 收藏列表 |
| 收藏 | POST | `/api/favorites` | 是 | 添加收藏 |
| 收藏 | DELETE | `/api/favorites/<topic_id>` | 是 | 取消收藏 |
| 收藏 | GET | `/api/favorites/check/<topic_id>` | 是 | 是否已收藏 |
| 笔记 | GET | `/api/notes` | 是 | 笔记列表 |
| 笔记 | POST | `/api/notes` | 是 | 新增笔记 |
| 笔记 | PUT | `/api/notes/<id>` | 是 | 更新笔记 |
| 笔记 | DELETE | `/api/notes/<id>` | 是 | 删除笔记 |
| 路径 | GET | `/api/paths/recommend` | 是 | 推荐学习路径 |
| 路径 | POST | `/api/paths/generate` | 是 | 生成个性化路径 |
| 路径 | GET | `/api/paths/current` | 是 | 当前学习路径 |
| 路径 | GET | `/api/paths/weak-areas` | 是 | 弱项分析 |

---

## 五、部署架构

```mermaid
graph TB
    subgraph 用户设备
        Browser[浏览器]
        WeChat[微信]
    end

    subgraph 服务器
        Flask[Flask :8088]
        SQLite[(SQLite DB)]
        Static[静态文件<br/>frontend/]
    end

    subgraph 云端
        MiMo[小米MiMo_API]
    end

    Browser -->|HTTP| Flask
    WeChat -->|HTTP| Flask
    Flask --> SQLite
    Flask --> Static
    Flask -->|HTTPS| MiMo
    Static --> Browser
```
