"""API 测试脚本"""
import requests
import json
import sys
import io

# 设置 stdout 为 UTF-8
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

BASE_URL = "http://localhost:8000"

def test_health():
    """测试健康检查"""
    res = requests.get(f"{BASE_URL}/api/health")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "ok"
    print("[PASS] 健康检查")

def test_register_and_login():
    """测试注册和登录"""
    # 注册
    res = requests.post(f"{BASE_URL}/api/auth/register", json={
        "username": "test_user_2",
        "email": "test2@example.com",
        "password": "test123"
    })
    if res.status_code == 200:
        token = res.json()["access_token"]
        print("[PASS] 注册成功")
        return token
    elif "already" in res.json().get("detail", "").lower() or "已存在" in res.json().get("detail", ""):
        # 已存在，直接登录
        res = requests.post(f"{BASE_URL}/api/auth/login", json={
            "username": "test_user_2",
            "password": "test123"
        })
        token = res.json()["access_token"]
        print("[PASS] 登录成功")
        return token
    else:
        print(f"[FAIL] 注册失败: {res.json()}")
        return None

def test_stats_endpoints(token):
    """测试统计端点"""
    headers = {"Authorization": f"Bearer {token}"}

    # 获取统计摘要
    res = requests.get(f"{BASE_URL}/api/stats/summary", headers=headers)
    assert res.status_code == 200
    print("[PASS] 获取统计摘要")

    # 获取每日统计
    res = requests.get(f"{BASE_URL}/api/stats/daily?days=7", headers=headers)
    assert res.status_code == 200
    print("[PASS] 获取每日统计")

    # 获取主题掌握度
    res = requests.get(f"{BASE_URL}/api/stats/topic-mastery", headers=headers)
    assert res.status_code == 200
    print("[PASS] 获取主题掌握度")

def test_achievements_endpoints(token):
    """测试成就端点"""
    headers = {"Authorization": f"Bearer {token}"}

    # 获取所有成就
    res = requests.get(f"{BASE_URL}/api/achievements")
    assert res.status_code == 200
    achievements = res.json()
    print(f"[PASS] 获取所有成就 ({len(achievements)} 个)")

    # 获取用户成就
    res = requests.get(f"{BASE_URL}/api/achievements/user", headers=headers)
    assert res.status_code == 200
    print("[PASS] 获取用户成就")

    # 获取积分
    res = requests.get(f"{BASE_URL}/api/points", headers=headers)
    assert res.status_code == 200
    print("[PASS] 获取积分")

    # 获取连续天数
    res = requests.get(f"{BASE_URL}/api/streak", headers=headers)
    assert res.status_code == 200
    print("[PASS] 获取连续天数")

    # 获取排行榜
    res = requests.get(f"{BASE_URL}/api/achievements/leaderboard")
    assert res.status_code == 200
    print("[PASS] 获取排行榜")

def test_favorites_endpoints(token):
    """测试收藏端点"""
    headers = {"Authorization": f"Bearer {token}"}

    # 获取收藏列表
    res = requests.get(f"{BASE_URL}/api/favorites", headers=headers)
    assert res.status_code == 200
    print("[PASS] 获取收藏列表")

    # 添加收藏
    res = requests.post(f"{BASE_URL}/api/favorites", json={"topic_id": "t1"}, headers=headers)
    if res.status_code == 200:
        print("[PASS] 添加收藏")
    else:
        print(f"添加收藏: {res.json()}")

def test_notes_endpoints(token):
    """测试笔记端点"""
    headers = {"Authorization": f"Bearer {token}"}

    # 获取笔记列表
    res = requests.get(f"{BASE_URL}/api/notes", headers=headers)
    assert res.status_code == 200
    print("[PASS] 获取笔记列表")

    # 添加笔记
    res = requests.post(f"{BASE_URL}/api/notes", json={
        "topic_id": "t1",
        "content": "test note"
    }, headers=headers)
    if res.status_code == 200:
        note_id = res.json()["id"]
        print("[PASS] 添加笔记")

        # 删除笔记
        res = requests.delete(f"{BASE_URL}/api/notes/{note_id}", headers=headers)
        assert res.status_code == 200
        print("[PASS] 删除笔记")

def test_paths_endpoints(token):
    """测试学习路径端点"""
    headers = {"Authorization": f"Bearer {token}"}

    # 获取推荐
    res = requests.get(f"{BASE_URL}/api/paths/recommend", headers=headers)
    assert res.status_code == 200
    print("[PASS] 获取推荐")

    # 获取薄弱环节
    res = requests.get(f"{BASE_URL}/api/paths/weak-areas", headers=headers)
    assert res.status_code == 200
    print("[PASS] 获取薄弱环节")

if __name__ == "__main__":
    print("=" * 50)
    print("API 测试开始")
    print("=" * 50)

    test_health()
    token = test_register_and_login()

    if token:
        test_stats_endpoints(token)
        test_achievements_endpoints(token)
        test_favorites_endpoints(token)
        test_notes_endpoints(token)
        test_paths_endpoints(token)

    print("=" * 50)
    print("API 测试完成")
    print("=" * 50)
