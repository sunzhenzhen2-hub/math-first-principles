"""用户注册/登录 API — Flask Blueprint"""
from flask import Blueprint, request, jsonify, g
from database import get_db
from auth import hash_password, verify_password, create_token, login_required

auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")


@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    if not data:
        return jsonify({"detail": "请求体为空"}), 400

    username = data.get("username", "").strip()
    email = data.get("email", "").strip()
    password = data.get("password", "")

    if not username or not email or not password:
        return jsonify({"detail": "用户名、邮箱和密码不能为空"}), 400

    with get_db() as conn:
        existing = conn.execute("SELECT id FROM users WHERE username = ?", (username,)).fetchone()
        if existing:
            return jsonify({"detail": "用户名已存在"}), 400
        existing = conn.execute("SELECT id FROM users WHERE email = ?", (email,)).fetchone()
        if existing:
            return jsonify({"detail": "邮箱已被注册"}), 400
        cursor = conn.execute(
            "INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)",
            (username, email, hash_password(password))
        )
        user_id = cursor.lastrowid
        token = create_token(user_id, username)
        return jsonify({"access_token": token, "token_type": "bearer"})


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    if not data:
        return jsonify({"detail": "请求体为空"}), 400

    username = data.get("username", "")
    password = data.get("password", "")

    with get_db() as conn:
        user = conn.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
        if not user or not verify_password(password, user["password_hash"]):
            return jsonify({"detail": "用户名或密码错误"}), 401
        token = create_token(user["id"], user["username"])
        return jsonify({"access_token": token, "token_type": "bearer"})


@auth_bp.route("/me", methods=["GET"])
@login_required
def me():
    with get_db() as conn:
        row = conn.execute(
            "SELECT id, username, email, created_at FROM users WHERE id = ?",
            (g.user["sub"],)
        ).fetchone()
        if not row:
            return jsonify({"detail": "用户不存在"}), 404
        return jsonify({
            "id": row["id"],
            "username": row["username"],
            "email": row["email"],
            "created_at": str(row["created_at"])
        })
