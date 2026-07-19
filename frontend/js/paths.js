/**
 * 个性化学习路径模块
 */
const Paths = {
  async render() {
    if (!API.token) {
      document.getElementById('paths-body').innerHTML = '<div class="wb"><p style="color:var(--ink-muted)">请先登录查看学习路径</p></div>';
      return;
    }

    const body = document.getElementById('paths-body');
    body.innerHTML = '<div class="loading">加载中...</div>';

    try {
      const [recommendations, weakAreas] = await Promise.all([
        API.getRecommendations(),
        API.getWeakAreas()
      ]);

      body.innerHTML = this._renderRecommendations(recommendations) +
                       this._renderWeakAreas(weakAreas) +
                       this._renderGenerateButton();
    } catch (e) {
      console.error('加载学习路径失败:', e);
      body.innerHTML = '<div class="wb"><p style="color:var(--danger)">加载失败</p></div>';
    }
  },

  _renderRecommendations(recommendations) {
    if (!recommendations || recommendations.length === 0) {
      return '<div class="wb"><h3>📍 推荐学习顺序</h3><p style="color:var(--ink-muted)">暂无推荐</p></div>';
    }

    let html = '<div class="wb"><h3>📍 推荐学习顺序</h3>';
    html += '<div class="path-list">';

    recommendations.forEach((r, i) => {
      let statusIcon, statusClass;
      if (r.status === 'completed') {
        statusIcon = '✅';
        statusClass = 'completed';
      } else if (r.is_recommended) {
        statusIcon = '📌';
        statusClass = 'recommended';
      } else {
        statusIcon = '🔒';
        statusClass = 'locked';
      }

      html += `
        <div class="path-item ${statusClass}">
          <span class="path-index">${i + 1}</span>
          <span class="path-icon">${r.icon}</span>
          <div class="path-info">
            <div class="path-title">${r.title}</div>
            <div class="path-stage">${r.stage}</div>
          </div>
          <span class="path-status">${statusIcon}</span>
          ${r.status === 'completed' ? `<span class="path-stars">${'⭐'.repeat(r.stars)}</span>` : ''}
          ${r.is_recommended ? `<button class="btn btn-sm btn-g" onclick="Lesson.start('${r.topic_id}')">开始</button>` : ''}
        </div>
      `;
    });

    html += '</div></div>';
    return html;
  },

  _renderWeakAreas(weakAreas) {
    if (!weakAreas || weakAreas.length === 0) {
      return '<div class="wb"><h3>🔴 薄弱环节</h3><p style="color:var(--ink-muted)">暂无薄弱环节，继续保持！</p></div>';
    }

    let html = '<div class="wb"><h3>🔴 薄弱环节 (需强化)</h3>';
    html += '<div class="weak-list">';

    weakAreas.forEach(w => {
      html += `
        <div class="weak-item">
          <div class="weak-info">
            <span class="weak-title">${w.title}</span>
            <span class="weak-stage">${w.stage}</span>
          </div>
          <div class="weak-stats">
            <span class="weak-accuracy" style="color:var(--danger)">${w.accuracy}%</span>
            <span class="weak-taken">已做${w.tests_taken}题</span>
          </div>
          <button class="btn btn-sm btn-o" onclick="Quiz.start('${w.topic_id}')">强化练习</button>
        </div>
      `;
    });

    html += '</div></div>';
    return html;
  },

  _renderGenerateButton() {
    return `
      <div style="text-align:center;margin-top:20px">
        <button class="btn btn-g" onclick="Paths.generatePersonalizedPath()">
          🤖 AI 生成个性化路径
        </button>
      </div>
    `;
  },

  async generatePersonalizedPath() {
    if (!confirm('根据你的学习数据生成个性化路径？')) return;

    try {
      const path = await API.generatePath();
      this.render(); // 刷新页面

      if (path.ai_suggestion) {
        alert('💡 AI 建议:\n' + path.ai_suggestion);
      }
    } catch (e) {
      alert('生成路径失败: ' + e.message);
    }
  }
};
