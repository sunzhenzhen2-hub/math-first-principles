"""配置管理"""
import os

# 数据库
DB_PATH = os.path.join(os.path.dirname(__file__), "math_learning.db")

# JWT
SECRET_KEY = os.getenv("MATH_SECRET_KEY", "math-learning-dev-secret-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 天

# OpenAI
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

# CORS
CORS_ORIGINS = ["*"]
