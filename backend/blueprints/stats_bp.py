"""学习统计 API — Flask Blueprint"""
from flask import Blueprint, request, jsonify, g
from auth import login_required
from services import stats_service

stats_bp = Blueprint("stats", __name__, url_prefix="/api")


@stats_bp.route("/stats/session/start", methods=["POST"])
@login_required
def start_session():
    """开始学习会话"""
    data = request.get_json()
    if not data or not data.get("topic_id"):
        return jsonify({"detail": "topic_id 不能为空"}), 400

    session_id = stats_service.start_study_session(g.user["sub"], data["topic_id"])
    return jsonify({"session_id": session_id})


@stats_bp.route("/stats/session/end", methods=["POST"])
@login_required
def end_session():
    """结束学习会话"""
    data = request.get_json()
    if not data or not data.get("session_id"):
        return jsonify({"detail": "session_id 不能为空"}), 400

    result = stats_service.end_study_session(g.user["sub"], data["session_id"])
    return jsonify(result)


@stats_bp.route("/stats/summary", methods=["GET"])
@login_required
def get_summary():
    """获取统计摘要"""
    summary = stats_service.get_summary(g.user["sub"])
    return jsonify(summary)


@stats_bp.route("/stats/daily", methods=["GET"])
@login_required
def get_daily():
    """获取每日统计"""
    days = request.args.get("days", 7, type=int)
    stats = stats_service.get_daily_stats(g.user["sub"], days)
    return jsonify(stats)


@stats_bp.route("/stats/weekly", methods=["GET"])
@login_required
def get_weekly():
    """获取每周统计"""
    stats = stats_service.get_weekly_stats(g.user["sub"])
    return jsonify(stats)


@stats_bp.route("/stats/topic-mastery", methods=["GET"])
@login_required
def get_topic_mastery():
    """获取主题掌握度"""
    mastery = stats_service.get_topic_mastery(g.user["sub"])
    return jsonify(mastery)


@stats_bp.route("/stats/record-quiz", methods=["POST"])
@login_required
def record_quiz():
    """记录测验尝试"""
    data = request.get_json()
    if not data:
        return jsonify({"detail": "请求体为空"}), 400

    correct = data.get("correct", False)
    stats_service.record_quiz_attempt(g.user["sub"], correct)
    return jsonify({"ok": True})
