"""JWT 认证 — Flask 版本"""
import hashlib
import hmac
import json
import base64
import time
from functools import wraps
from flask import request, g, jsonify
from config import SECRET_KEY, ACCESS_TOKEN_EXPIRE_MINUTES


def _b64(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode()


def _unb64(s: str) -> bytes:
    s += "=" * (4 - len(s) % 4)
    return base64.urlsafe_b64decode(s)


def hash_password(password: str) -> str:
    """简单密码哈希（生产环境应使用 bcrypt）"""
    return hashlib.sha256((password + SECRET_KEY).encode()).hexdigest()


def verify_password(password: str, hashed: str) -> bool:
    return hmac.compare_digest(hash_password(password), hashed)


def create_token(user_id: int, username: str) -> str:
    """创建 JWT token"""
    header = _b64(json.dumps({"alg": "HS256", "typ": "JWT"}).encode())
    payload = _b64(json.dumps({
        "sub": user_id,
        "username": username,
        "exp": int(time.time()) + ACCESS_TOKEN_EXPIRE_MINUTES * 60
    }).encode())
    signature = _b64(hmac.new(
        SECRET_KEY.encode(), f"{header}.{payload}".encode(), hashlib.sha256
    ).digest())
    return f"{header}.{payload}.{signature}"


def verify_token(token: str) -> dict | None:
    """验证 JWT token，返回 payload 或 None"""
    try:
        parts = token.split(".")
        if len(parts) != 3:
            return None
        header, payload, signature = parts
        expected = _b64(hmac.new(
            SECRET_KEY.encode(), f"{header}.{payload}".encode(), hashlib.sha256
        ).digest())
        if not hmac.compare_digest(signature, expected):
            return None
        data = json.loads(_unb64(payload))
        if data.get("exp", 0) < time.time():
            return None
        return data
    except Exception:
        return None


def login_required(f):
    """Flask 装饰器：验证 JWT token，将用户信息存入 g.user"""
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer "):
            return jsonify({"detail": "未登录"}), 401
        token = auth_header[7:]
        payload = verify_token(token)
        if not payload:
            return jsonify({"detail": "登录已过期，请重新登录"}), 401
        g.user = payload
        return f(*args, **kwargs)
    return decorated
