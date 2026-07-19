"""配置管理"""
import os

# 数据库
DB_PATH = os.path.join(os.path.dirname(__file__), "math_learning.db")

# JWT
SECRET_KEY = os.getenv("MATH_SECRET_KEY", "math-learning-dev-secret-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 天

# AI 模型配置 (小米 MiMo)
# 请设置环境变量 AI_API_KEY 为你的 API Key
AI_API_KEY = os.getenv("AI_API_KEY", "")
AI_BASE_URL = os.getenv("AI_BASE_URL", "https://token-plan-cn.xiaomimimo.com/v1")
AI_MODEL = os.getenv("AI_MODEL", "mimo-v2.5")

# 向后兼容
OPENAI_API_KEY = AI_API_KEY
OPENAI_MODEL = AI_MODEL

# CORS
CORS_ORIGINS = ["*"]
