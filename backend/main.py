"""数学第一性原理学习系统 — Flask 后端"""
import sys
import os

# Windows UTF-8 支持
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

sys.path.insert(0, os.path.dirname(__file__))

from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
from database import init_db, get_db
from config import CORS_ORIGINS

# ---------- 初始化数据库 & 种子数据 ----------
init_db()

with get_db() as conn:
    count = conn.execute("SELECT COUNT(*) as c FROM topics").fetchone()["c"]
    if count == 0:
        print("导入种子数据...")
        from seed_data import seed_all
        seed_all(conn)
        from seed_data_extra import EXTRA_TOPICS
        from seed_data import seed_topics
        seed_topics(conn, EXTRA_TOPICS)
        total = conn.execute("SELECT COUNT(*) FROM topics").fetchone()[0]
        print(f"已导入 {total} 个主题")

    pq_count = conn.execute("SELECT COUNT(*) as c FROM placement_questions").fetchone()["c"]
    if pq_count == 0:
        from seed_data_placement import PLACEMENT_QUESTIONS
        import json
        for i, q in enumerate(PLACEMENT_QUESTIONS):
            conn.execute(
                "INSERT INTO placement_questions (stage_index, difficulty, question, options, answer, explanation, sort_order) VALUES (?,?,?,?,?,?,?)",
                (q["stage_index"], q["difficulty"], q["question"], json.dumps(q["options"]), q["answer"], q["explanation"], i + 1)
            )
        print(f"已导入 {len(PLACEMENT_QUESTIONS)} 道定位测试题")

    derive_count = conn.execute(
        "SELECT COUNT(*) FROM lesson_sections WHERE content LIKE '%推导：%'"
    ).fetchone()[0]
    if derive_count == 0:
        from seed_data_derive import DERIVE_SECTIONS
        for topic_id, sections in DERIVE_SECTIONS.items():
            row = conn.execute(
                "SELECT MAX(sort_order) as m FROM lesson_sections WHERE topic_id = ?",
                (topic_id,)
            ).fetchone()
            max_order = row["m"] if row["m"] else 0
            for i, s in enumerate(sections):
                conn.execute(
                    "INSERT INTO lesson_sections (topic_id, section_type, content, sort_order) VALUES (?,?,?,?)",
                    (topic_id, s["type"], s["content"], max_order + i + 1)
                )
        print(f"已为 {len(DERIVE_SECTIONS)} 个主题补充推导过程")

    extra_quiz_count = conn.execute(
        "SELECT COUNT(*) FROM quiz_questions WHERE id > 200"
    ).fetchone()[0]
    if extra_quiz_count == 0:
        import json as _json
        all_quiz = {}
        quiz_files = [
            "seed_data_extra_quiz",
            "seed_data_quiz_full",
            "seed_data_quiz_full2",
            "seed_data_quiz_full3",
        ]
        for fname in quiz_files:
            try:
                mod = __import__(fname)
                quiz_dict = getattr(mod, [k for k in dir(mod) if k.startswith("FULL") or k.startswith("EXTRA")][0])
                for tid, qs in quiz_dict.items():
                    if tid not in all_quiz:
                        all_quiz[tid] = []
                    all_quiz[tid].extend(qs)
            except Exception as e:
                print(f"加载 {fname} 失败: {e}")

        quiz_added = 0
        for topic_id, questions in all_quiz.items():
            row = conn.execute(
                "SELECT MAX(sort_order) as m FROM quiz_questions WHERE topic_id = ?",
                (topic_id,)
            ).fetchone()
            max_order = row["m"] if row["m"] else 0
            for i, q in enumerate(questions):
                conn.execute(
                    "INSERT INTO quiz_questions (topic_id, question, options, answer, explanation, sort_order) VALUES (?,?,?,?,?,?)",
                    (topic_id, q["question"], _json.dumps(q["options"]), q["answer"], q["explanation"], max_order + i + 1)
                )
                quiz_added += 1
        print(f"已扩充 {quiz_added} 道测验题")

# ---------- Flask 应用 ----------
frontend_dir = os.path.join(os.path.dirname(__file__), "..", "frontend")
app = Flask(__name__, static_folder=frontend_dir, static_url_path="")
CORS(app, resources={r"/api/*": {"origins": CORS_ORIGINS}})

# 注册蓝图
from blueprints.auth_bp import auth_bp
from blueprints.content_bp import content_bp
from blueprints.progress_bp import progress_bp
from blueprints.ai_bp import ai_bp
from blueprints.placement_bp import placement_bp

app.register_blueprint(auth_bp)
app.register_blueprint(content_bp)
app.register_blueprint(progress_bp)
app.register_blueprint(ai_bp)
app.register_blueprint(placement_bp)


@app.route("/api/health")
def health():
    return jsonify({"status": "ok", "version": "1.0.0"})


# 前端静态文件 catch-all
@app.route("/")
@app.route("/<path:path>")
def serve_frontend(path=""):
    if path and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    return send_from_directory(app.static_folder, "index.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
