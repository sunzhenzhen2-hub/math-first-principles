/**
 * API 封装层
 * 所有与后端的通信都通过此模块
 */
const API = {
  BASE: window.location.origin.includes('localhost')
    ? 'http://localhost:8000'
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
};
