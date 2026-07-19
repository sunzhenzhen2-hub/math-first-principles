/**
 * 学习统计模块
 */
const Stats = {
  currentSession: null,

  async render() {
    if (!API.token) {
      document.getElementById('stats-body').innerHTML = '<div class="wb"><p style="color:var(--ink-muted)">请先登录查看学习报告</p></div>';
      return;
    }

    const body = document.getElementById('stats-body');
    body.innerHTML = '<div class="loading">加载中...</div>';

    try {
      const [summary, daily, weekly, mastery] = await Promise.all([
        API.getStatsSummary(),
        API.getDailyStats(7),
        API.getWeeklyStats(),
        API.getTopicMastery()
      ]);

      body.innerHTML = this._renderSummary(summary) +
                       this._renderDailyChart(daily) +
                       this._renderWeeklyTrend(weekly) +
                       this._renderTopicMastery(mastery);
    } catch (e) {
      console.error('加载统计数据失败:', e);
      body.innerHTML = '<div class="wb"><p style="color:var(--danger)">加载失败</p></div>';
    }
  },

  _renderSummary(summary) {
    return `
      <div class="stats">
        <div class="st"><div class="sv2">${summary.total_study_hours}h</div><div class="sl">总学时</div></div>
        <div class="st"><div class="sv2" style="color:${summary.accuracy >= 70 ? 'var(--success)' : 'var(--danger)'}">${summary.accuracy}%</div><div class="sl">正确率</div></div>
        <div class="st"><div class="sv2">🔥${summary.current_streak}</div><div class="sl">连续天数</div></div>
        <div class="st"><div class="sv2">💎${summary.total_points}</div><div class="sl">积分</div></div>
      </div>
      <div class="stats" style="margin-top:12px">
        <div class="st"><div class="sv2">${summary.completed_topics}/30</div><div class="sl">已完成主题</div></div>
        <div class="st"><div class="sv2">${summary.total_quizzes}</div><div class="sl">总做题数</div></div>
        <div class="st"><div class="sv2">${summary.total_correct}</div><div class="sl">答对数</div></div>
      </div>
    `;
  },

  _renderDailyChart(daily) {
    if (!daily || daily.length === 0) {
      return '<div class="wb"><h3>📅 每日学习</h3><p style="color:var(--ink-muted);font-size:0.85rem">暂无数据</p></div>';
    }

    const maxMinutes = Math.max(...daily.map(d => d.study_minutes), 1);
    const bars = daily.map(d => {
      const height = Math.max((d.study_minutes / maxMinutes) * 100, 2);
      const day = new Date(d.date).toLocaleDateString('zh-CN', { weekday: 'short' });
      return `
        <div class="chart-bar-wrap">
          <div class="chart-bar" style="height:${height}%" title="${d.study_minutes}分钟"></div>
          <div class="chart-label">${day}</div>
        </div>
      `;
    }).join('');

    return `
      <div class="wb">
        <h3>📅 每日学习时长</h3>
        <div class="chart-container">${bars}</div>
      </div>
    `;
  },

  _renderWeeklyTrend(weekly) {
    const tw = weekly.this_week || {};
    const lw = weekly.last_week || {};
    const trend = weekly.trend || {};

    const minutesChange = trend.minutes_change || 0;
    const accuracyChange = trend.accuracy_change || 0;

    return `
      <div class="wb">
        <h3>📊 本周 vs 上周</h3>
        <div class="trend-grid">
          <div class="trend-item">
            <div class="trend-value">${tw.minutes || 0} 分钟</div>
            <div class="trend-label">本周学时</div>
            <div class="trend-change ${minutesChange >= 0 ? 'positive' : 'negative'}">
              ${minutesChange >= 0 ? '↑' : '↓'} ${Math.abs(minutesChange)} 分钟
            </div>
          </div>
          <div class="trend-item">
            <div class="trend-value">${tw.correct || 0}/${tw.attempted || 0}</div>
            <div class="trend-label">本周做题</div>
          </div>
        </div>
      </div>
    `;
  },

  _renderTopicMastery(mastery) {
    if (!mastery || mastery.length === 0) {
      return '<div class="wb"><h3>🎯 知识掌握度</h3><p style="color:var(--ink-muted);font-size:0.85rem">暂无数据</p></div>';
    }

    // 按阶段分组
    const stages = {};
    mastery.forEach(m => {
      if (!stages[m.stage]) stages[m.stage] = [];
      stages[m.stage].push(m);
    });

    let html = '<div class="wb"><h3>🎯 知识掌握度</h3>';

    Object.entries(stages).forEach(([stage, topics]) => {
      html += `<div class="stage-mastery"><div class="stage-name">${stage}</div>`;
      topics.forEach(t => {
        const accuracy = t.tests_taken > 0 ? Math.round(t.tests_passed / t.tests_taken * 100) : 0;
        const color = accuracy >= 80 ? 'var(--success)' : accuracy >= 50 ? 'var(--accent)' : 'var(--danger)';
        html += `
          <div class="mastery-item">
            <span class="mastery-title">${t.title}</span>
            <div class="mastery-bar-bg">
              <div class="mastery-bar" style="width:${accuracy}%;background:${color}"></div>
            </div>
            <span class="mastery-pct" style="color:${color}">${accuracy}%</span>
          </div>
        `;
      });
      html += '</div>';
    });

    html += '</div>';
    return html;
  },

  // 开始学习会话
  async startSession(topicId) {
    if (!API.token) return null;
    try {
      const result = await API.startStudySession(topicId);
      this.currentSession = result.session_id;
      return result.session_id;
    } catch (e) {
      console.error('开始学习会话失败:', e);
      return null;
    }
  },

  // 结束学习会话
  async endSession() {
    if (!API.token || !this.currentSession) return null;
    try {
      const result = await API.endStudySession(this.currentSession);
      this.currentSession = null;
      return result;
    } catch (e) {
      console.error('结束学习会话失败:', e);
      return null;
    }
  }
};
