"""用户注册/登录 API"""
from fastapi import APIRouter, HTTPException, Depends
from database import get_db
from auth import hash_password, verify_password, create_token, get_current_user
from models import UserRegister, UserLogin, UserResponse, Token

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/register", response_model=Token)
def register(data: UserRegister):
    with get_db() as conn:
        # 检查用户名
        existing = conn.execute("SELECT id FROM users WHERE username = ?", (data.username,)).fetchone()
        if existing:
            raise HTTPException(400, "用户名已存在")
        # 检查邮箱
        existing = conn.execute("SELECT id FROM users WHERE email = ?", (data.email,)).fetchone()
        if existing:
            raise HTTPException(400, "邮箱已被注册")
        # 创建用户
        cursor = conn.execute(
            "INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)",
            (data.username, data.email, hash_password(data.password))
        )
        user_id = cursor.lastrowid
        token = create_token(user_id, data.username)
        return Token(access_token=token)


@router.post("/login", response_model=Token)
def login(data: UserLogin):
    with get_db() as conn:
        user = conn.execute("SELECT * FROM users WHERE username = ?", (data.username,)).fetchone()
        if not user or not verify_password(data.password, user["password_hash"]):
            raise HTTPException(401, "用户名或密码错误")
        token = create_token(user["id"], user["username"])
        return Token(access_token=token)


@router.get("/me", response_model=UserResponse)
def me(user=Depends(get_current_user)):
    with get_db() as conn:
        row = conn.execute("SELECT id, username, email, created_at FROM users WHERE id = ?", (user["sub"],)).fetchone()
        if not row:
            raise HTTPException(404, "用户不存在")
        return UserResponse(id=row["id"], username=row["username"], email=row["email"], created_at=str(row["created_at"]))
