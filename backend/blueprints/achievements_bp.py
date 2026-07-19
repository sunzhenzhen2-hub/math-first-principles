"""成就与激励系统 API — Flask Blueprint"""
from flask import Blueprint, request, jsonify, g
from auth import login_required
from services import achievements_service

achievements_bp = Blueprint("achievements", __name__, url_prefix="/api")


@achievements_bp.route("/achievements", methods=["GET"])
def get_all_achievements():
    """获取所有成就定义"""
    achievements = achievements_service.get_all_achievements()
    return jsonify(achievements)


@achievements_bp.route("/achievements/user", methods=["GET"])
@login_required
def get_user_achievements():
    """获取用户已获得的成就"""
    achievements = achievements_service.get_user_achievements(g.user["sub"])
    return jsonify(achievements)


@achievements_bp.route("/achievements/check", methods=["POST"])
@login_required
def check_achievements():
    """检查并授予成就"""
    new_achievements = achievements_service.check_and_award_achievements(g.user["sub"])
    return jsonify({"new_achievements": new_achievements})


@achievements_bp.route("/achievements/leaderboard", methods=["GET"])
def get_leaderboard():
    """获取排行榜"""
    limit = request.args.get("limit", 10, type=int)
    leaderboard = achievements_service.get_leaderboard(limit)
    return jsonify(leaderboard)


@achievements_bp.route("/points", methods=["GET"])
@login_required
def get_points():
    """获取用户积分"""
    points = achievements_service.get_points(g.user["sub"])
    return jsonify(points)


@achievements_bp.route("/points/history", methods=["GET"])
@login_required
def get_points_history():
    """获取积分历史"""
    limit = request.args.get("limit", 20, type=int)
    history = achievements_service.get_points_history(g.user["sub"], limit)
    return jsonify(history)


@achievements_bp.route("/streak", methods=["GET"])
@login_required
def get_streak():
    """获取学习连续天数"""
    streak = achievements_service.get_streak(g.user["sub"])
    return jsonify(streak)
