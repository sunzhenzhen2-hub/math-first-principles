/**
 * 小程序 API 封装
 */
const app = getApp();

module.exports = {
  // 认证
  login(username, password) {
    return app.request('/api/auth/login', {
      method: 'POST',
      data: { username, password }
    });
  },

  register(username, email, password) {
    return app.request('/api/auth/register', {
      method: 'POST',
      data: { username, email, password }
    });
  },

  // 主题
  getTopics() {
    return app.request('/api/topics');
  },

  getTopic(id) {
    return app.request('/api/topics/' + id);
  },

  // 进度
  getProgress() {
    return app.request('/api/progress');
  },

  updateProgress(topicId, stars, score, total) {
    return app.request('/api/progress', {
      method: 'POST',
      data: { topic_id: topicId, stars, score, total }
    });
  },

  // 错题
  getWrongAnswers() {
    return app.request('/api/wrong-answers');
  },

  addWrongAnswer(data) {
    return app.request('/api/wrong-answers', {
      method: 'POST',
      data
    });
  },

  deleteWrongAnswer(id) {
    return app.request('/api/wrong-answers/' + id, { method: 'DELETE' });
  },

  // AI
  aiDerive(topicId) {
    return app.request('/api/ai/derive', {
      method: 'POST',
      data: { topic_id: topicId }
    });
  }
};
