"""个性化学习路径 API — Flask Blueprint"""
from flask import Blueprint, request, jsonify, g
from auth import login_required
from services import paths_service

paths_bp = Blueprint("paths", __name__, url_prefix="/api")


@paths_bp.route("/paths/recommend", methods=["GET"])
@login_required
def get_recommendations():
    """获取推荐学习顺序"""
    recommendations = paths_service.get_recommendations(g.user["sub"])
    return jsonify(recommendations)


@paths_bp.route("/paths/generate", methods=["POST"])
@login_required
def generate_path():
    """生成个性化学习路径"""
    path = paths_service.generate_personalized_path(g.user["sub"])
    return jsonify(path)


@paths_bp.route("/paths/current", methods=["GET"])
@login_required
def get_current_path():
    """获取当前学习路径"""
    path = paths_service.get_or_create_path(g.user["sub"])
    return jsonify(path)


@paths_bp.route("/paths/weak-areas", methods=["GET"])
@login_required
def get_weak_areas():
    """获取薄弱环节分析"""
    weak_areas = paths_service.get_weak_areas(g.user["sub"])
    return jsonify(weak_areas)
