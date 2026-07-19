/**
 * API 封装层
 * 所有与后端的通信都通过此模块
 */
const API = {
  BASE: window.location.origin.includes('localhost')
    ? 'http://localhost:8088'
    : window.location.origin,

  token: localStorage.getItem('math_token') || null,

  setToken(t) { this.token = t; if (t) localStorage.setItem('math_token', t); else localStorage.removeItem('math_token'); },

  async _fetch(path, opts = {}) {
    const headers = { 'Content-Type': 'application/json', ...opts.headers };
    if (this.token) headers['Authorization'] = `Bearer ${this.token}`;
    const res = await fetch(this.BASE + path, { ...opts, headers });
    if (res.status === 401) { this.setToken(null); location.reload(); return null; }
    if (!res.ok) {
      const err = await res.json().catch(() => ({ detail: '请求失败' }));
      throw new Error(err.detail || '请求失败');
    }
    return res.json();
  },

  // 认证
  async register(username, email, password) {
    const data = await this._fetch('/api/auth/register', { method: 'POST', body: JSON.stringify({ username, email, password }) });
    if (data?.access_token) this.setToken(data.access_token);
    return data;
  },
  async login(username, password) {
    const data = await this._fetch('/api/auth/login', { method: 'POST', body: JSON.stringify({ username, password }) });
    if (data?.access_token) this.setToken(data.access_token);
    return data;
  },
  async me() { return this._fetch('/api/auth/me'); },

  // 主题
  async getTopics() { return this._fetch('/api/topics'); },
  async getTopic(id) { return this._fetch(`/api/topics/${id}`); },

  // 进度
  async getProgress() { return this._fetch('/api/progress'); },
  async updateProgress(topicId, stars, score, total) {
    return this._fetch('/api/progress', { method: 'POST', body: JSON.stringify({ topic_id: topicId, stars, score, total }) });
  },

  // 错题
  async getWrongAnswers() { return this._fetch('/api/wrong-answers'); },
  async addWrongAnswer(data) { return this._fetch('/api/wrong-answers', { method: 'POST', body: JSON.stringify(data) }); },
  async deleteWrongAnswer(id) { return this._fetch(`/api/wrong-answers/${id}`, { method: 'DELETE' }); },

  // AI
  async aiDerive(topicId, extra) { return this._fetch('/api/ai/derive', { method: 'POST', body: JSON.stringify({ topic_id: topicId, extra_context: extra }) }); },
  async aiExplain(q, ua, ca, title) { return this._fetch('/api/ai/explain', { method: 'POST', body: JSON.stringify({ question: q, user_answer: ua, correct_answer: ca, topic_title: title }) }); },

  // ========== 学习统计 ==========
  async startStudySession(topicId) { return this._fetch('/api/stats/session/start', { method: 'POST', body: JSON.stringify({ topic_id: topicId }) }); },
  async endStudySession(sessionId) { return this._fetch('/api/stats/session/end', { method: 'POST', body: JSON.stringify({ session_id: sessionId }) }); },
  async getStatsSummary() { return this._fetch('/api/stats/summary'); },
  async getDailyStats(days) { return this._fetch(`/api/stats/daily?days=${days || 7}`); },
  async getWeeklyStats() { return this._fetch('/api/stats/weekly'); },
  async getTopicMastery() { return this._fetch('/api/stats/topic-mastery'); },
  async recordQuizAttempt(correct) { return this._fetch('/api/stats/record-quiz', { method: 'POST', body: JSON.stringify({ correct }) }); },

  // ========== 成就系统 ==========
  async getAchievements() { return this._fetch('/api/achievements'); },
  async getUserAchievements() { return this._fetch('/api/achievements/user'); },
  async checkAchievements() { return this._fetch('/api/achievements/check', { method: 'POST' }); },
  async getLeaderboard() { return this._fetch('/api/achievements/leaderboard'); },
  async getPoints() { return this._fetch('/api/points'); },
  async getPointsHistory() { return this._fetch('/api/points/history'); },
  async getStreak() { return this._fetch('/api/streak'); },

  // ========== 收藏与笔记 ==========
  async getFavorites() { return this._fetch('/api/favorites'); },
  async addFavorite(topicId) { return this._fetch('/api/favorites', { method: 'POST', body: JSON.stringify({ topic_id: topicId }) }); },
  async removeFavorite(topicId) { return this._fetch(`/api/favorites/${topicId}`, { method: 'DELETE' }); },
  async checkFavorite(topicId) { return this._fetch(`/api/favorites/check/${topicId}`); },
  async getNotes(topicId) { return this._fetch(`/api/notes${topicId ? '?topic_id=' + topicId : ''}`); },
  async addNote(topicId, content, sectionId) { return this._fetch('/api/notes', { method: 'POST', body: JSON.stringify({ topic_id: topicId, content, section_id: sectionId }) }); },
  async updateNote(noteId, content) { return this._fetch(`/api/notes/${noteId}`, { method: 'PUT', body: JSON.stringify({ content }) }); },
  async deleteNote(noteId) { return this._fetch(`/api/notes/${noteId}`, { method: 'DELETE' }); },

  // ========== 学习路径 ==========
  async getRecommendations() { return this._fetch('/api/paths/recommend'); },
  async generatePath() { return this._fetch('/api/paths/generate', { method: 'POST' }); },
  async getCurrentPath() { return this._fetch('/api/paths/current'); },
  async getWeakAreas() { return this._fetch('/api/paths/weak-areas'); },
};
