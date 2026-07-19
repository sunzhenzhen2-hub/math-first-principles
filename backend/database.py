"""SQLite 数据库连接与建表"""
import sqlite3
from contextlib import contextmanager
from config import DB_PATH


def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    return conn


@contextmanager
def get_db():
    conn = get_connection()
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


def init_db():
    """初始化数据库表结构"""
    with get_db() as conn:
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS topics (
                id TEXT PRIMARY KEY,
                stage TEXT NOT NULL,
                stage_index INTEGER NOT NULL,
                title TEXT NOT NULL,
                description TEXT,
                icon TEXT,
                sort_order INTEGER NOT NULL
            );

            CREATE TABLE IF NOT EXISTS progress (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                topic_id TEXT NOT NULL,
                stars INTEGER DEFAULT 0,
                tests_taken INTEGER DEFAULT 0,
                tests_passed INTEGER DEFAULT 0,
                best_score INTEGER DEFAULT 0,
                completed_at TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id),
                FOREIGN KEY (topic_id) REFERENCES topics(id),
                UNIQUE(user_id, topic_id)
            );

            CREATE TABLE IF NOT EXISTS wrong_answers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                topic_id TEXT NOT NULL,
                question TEXT NOT NULL,
                user_answer TEXT NOT NULL,
                correct_answer TEXT NOT NULL,
                explanation TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            );

            CREATE TABLE IF NOT EXISTS ai_content_cache (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                topic_id TEXT NOT NULL,
                prompt_hash TEXT NOT NULL,
                content TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(topic_id, prompt_hash)
            );

            CREATE TABLE IF NOT EXISTS lesson_sections (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                topic_id TEXT NOT NULL,
                section_type TEXT NOT NULL,
                content TEXT NOT NULL,
                sort_order INTEGER NOT NULL,
                FOREIGN KEY (topic_id) REFERENCES topics(id)
            );

            CREATE TABLE IF NOT EXISTS quiz_questions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                topic_id TEXT NOT NULL,
                question TEXT NOT NULL,
                options TEXT NOT NULL,
                answer INTEGER NOT NULL,
                explanation TEXT,
                sort_order INTEGER NOT NULL,
                FOREIGN KEY (topic_id) REFERENCES topics(id)
            );

            CREATE INDEX IF NOT EXISTS idx_progress_user ON progress(user_id);
            CREATE INDEX IF NOT EXISTS idx_wrong_user ON wrong_answers(user_id);
            CREATE INDEX IF NOT EXISTS idx_ai_cache_topic ON ai_content_cache(topic_id);
            CREATE INDEX IF NOT EXISTS idx_lesson_topic ON lesson_sections(topic_id);
            CREATE INDEX IF NOT EXISTS idx_quiz_topic ON quiz_questions(topic_id);

            CREATE TABLE IF NOT EXISTS placement_questions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                stage_index INTEGER NOT NULL,
                difficulty INTEGER NOT NULL,
                question TEXT NOT NULL,
                options TEXT NOT NULL,
                answer INTEGER NOT NULL,
                explanation TEXT,
                sort_order INTEGER NOT NULL
            );

            -- ========== 功能增强: 学习报告与数据 ==========

            CREATE TABLE IF NOT EXISTS study_sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                topic_id TEXT NOT NULL,
                duration_seconds INTEGER DEFAULT 0,
                started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                completed_at TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id),
                FOREIGN KEY (topic_id) REFERENCES topics(id)
            );

            CREATE TABLE IF NOT EXISTS daily_stats (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                date TEXT NOT NULL,
                study_minutes INTEGER DEFAULT 0,
                questions_attempted INTEGER DEFAULT 0,
                questions_correct INTEGER DEFAULT 0,
                topics_completed INTEGER DEFAULT 0,
                FOREIGN KEY (user_id) REFERENCES users(id),
                UNIQUE(user_id, date)
            );

            -- ========== 功能增强: 成就与激励系统 ==========

            CREATE TABLE IF NOT EXISTS achievements (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                description TEXT NOT NULL,
                icon TEXT NOT NULL,
                criteria_type TEXT NOT NULL,
                criteria_value INTEGER NOT NULL
            );

            CREATE TABLE IF NOT EXISTS user_achievements (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                achievement_id TEXT NOT NULL,
                earned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id),
                FOREIGN KEY (achievement_id) REFERENCES achievements(id),
                UNIQUE(user_id, achievement_id)
            );

            CREATE TABLE IF NOT EXISTS user_points (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL UNIQUE,
                total_points INTEGER DEFAULT 0,
                FOREIGN KEY (user_id) REFERENCES users(id)
            );

            CREATE TABLE IF NOT EXISTS point_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                points INTEGER NOT NULL,
                reason TEXT NOT NULL,
                reference_id TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            );

            CREATE TABLE IF NOT EXISTS study_streaks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL UNIQUE,
                current_streak INTEGER DEFAULT 0,
                longest_streak INTEGER DEFAULT 0,
                last_study_date TEXT,
                FOREIGN KEY (user_id) REFERENCES users(id)
            );

            -- ========== 功能增强: 收藏与笔记 ==========

            CREATE TABLE IF NOT EXISTS favorites (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                topic_id TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id),
                FOREIGN KEY (topic_id) REFERENCES topics(id),
                UNIQUE(user_id, topic_id)
            );

            CREATE TABLE IF NOT EXISTS notes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                topic_id TEXT NOT NULL,
                section_id INTEGER,
                content TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id),
                FOREIGN KEY (topic_id) REFERENCES topics(id)
            );

            -- ========== 功能增强: 个性化学习路径 ==========

            CREATE TABLE IF NOT EXISTS learning_paths (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL UNIQUE,
                path_data TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            );

            -- ========== 索引 ==========

            CREATE INDEX IF NOT EXISTS idx_study_sessions_user ON study_sessions(user_id);
            CREATE INDEX IF NOT EXISTS idx_daily_stats_user_date ON daily_stats(user_id, date);
            CREATE INDEX IF NOT EXISTS idx_user_achievements_user ON user_achievements(user_id);
            CREATE INDEX IF NOT EXISTS idx_point_history_user ON point_history(user_id);
            CREATE INDEX IF NOT EXISTS idx_favorites_user ON favorites(user_id);
            CREATE INDEX IF NOT EXISTS idx_notes_user_topic ON notes(user_id, topic_id);
        """)
