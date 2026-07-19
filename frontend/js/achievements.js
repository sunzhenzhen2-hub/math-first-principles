/**
 * 成就与激励系统模块
 */
const Achievements = {
  async render() {
    if (!API.token) {
      document.getElementById('achievements-body').innerHTML = '<div class="wb"><p style="color:var(--ink-muted)">请先登录查看成就</p></div>';
      return;
    }

    const body = document.getElementById('achievements-body');
    body.innerHTML = '<div class="loading">加载中...</div>';

    try {
      const [allAchievements, userAchievements, points, streak, leaderboard] = await Promise.all([
        API.getAchievements(),
        API.getUserAchievements(),
        API.getPoints(),
        API.getStreak(),
        API.getLeaderboard()
      ]);

      const earnedIds = new Set(userAchievements.map(a => a.id));

      body.innerHTML = this._renderHeader(points, streak) +
                       this._renderAchievements(allAchievements, earnedIds) +
                       this._renderLeaderboard(leaderboard);
    } catch (e) {
      console.error('加载成就数据失败:', e);
      body.innerHTML = '<div class="wb"><p style="color:var(--danger)">加载失败</p></div>';
    }
  },

  _renderHeader(points, streak) {
    return `
      <div class="stats">
        <div class="st"><div class="sv2">💎${points.total_points}</div><div class="sl">总积分</div></div>
        <div class="st"><div class="sv2">🔥${streak.current_streak}</div><div class="sl">连续天数</div></div>
        <div class="st"><div class="sv2">🏆${streak.longest_streak}</div><div class="sl">最长连续</div></div>
      </div>
    `;
  },

  _renderAchievements(allAchievements, earnedIds) {
    const earned = allAchievements.filter(a => earnedIds.has(a.id));
    const locked = allAchievements.filter(a => !earnedIds.has(a.id));

    let html = '<div class="wb">';

    // 已获得
    html += `<h3>🎖️ 已获得 (${earned.length}/${allAchievements.length})</h3>`;
    if (earned.length > 0) {
      html += '<div class="achievement-grid">';
      earned.forEach(a => {
        html += `
          <div class="achievement-card earned">
            <div class="achievement-icon">${a.icon}</div>
            <div class="achievement-name">${a.name}</div>
            <div class="achievement-desc">${a.description}</div>
          </div>
        `;
      });
      html += '</div>';
    } else {
      html += '<p style="color:var(--ink-muted);font-size:0.85rem">暂无成就，继续加油！</p>';
    }

    html += '</div><div class="wb">';

    // 未获得
    html += `<h3>🔒 未获得 (${locked.length}/${allAchievements.length})</h3>`;
    html += '<div class="achievement-grid">';
    locked.forEach(a => {
      html += `
        <div class="achievement-card locked">
          <div class="achievement-icon">${a.icon}</div>
          <div class="achievement-name">${a.name}</div>
          <div class="achievement-desc">${a.description}</div>
        </div>
      `;
    });
    html += '</div></div>';

    return html;
  },

  _renderLeaderboard(leaderboard) {
    if (!leaderboard || leaderboard.length === 0) {
      return '';
    }

    let html = '<div class="wb"><h3>🏅 排行榜</h3>';
    html += '<div class="leaderboard-list">';

    const medals = ['🥇', '🥈', '🥉'];
    leaderboard.forEach((item, i) => {
      const medal = medals[i] || `${i + 1}.`;
      const isMe = item.username === document.getElementById('user-name')?.textContent;
      html += `
        <div class="leaderboard-item ${isMe ? 'is-me' : ''}">
          <span class="lb-medal">${medal}</span>
          <span class="lb-name">${item.username}</span>
          <span class="lb-points">💎${item.total_points}</span>
          <span class="lb-streak">🔥${item.streak}</span>
        </div>
      `;
    });

    html += '</div></div>';
    return html;
  },

  // 检查并授予新成就
  async checkNewAchievements() {
    if (!API.token) return [];
    try {
      const result = await API.checkAchievements();
      return result.new_achievements || [];
    } catch (e) {
      console.error('检查成就失败:', e);
      return [];
    }
  }
};
