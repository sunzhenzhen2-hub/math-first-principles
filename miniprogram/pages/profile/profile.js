const api = require('../../utils/api');
const app = getApp();

Page({
  data: {
    user: null,
    username: '',
    password: '',
    authError: '',
    completedTopics: 0,
    totalTests: 0,
    accuracy: 0,
    totalStars: 0,
    wrongCount: 0,
    wrongList: []
  },

  onShow() {
    if (app.globalData.user) {
      this.setData({ user: app.globalData.user });
      this.loadStats();
    }
  },

  async loadStats() {
    try {
      const [progress, wrong] = await Promise.all([
        api.getProgress().catch(() => []),
        api.getWrongAnswers().catch(() => [])
      ]);

      const completedTopics = progress.filter(p => p.stars > 0).length;
      const totalTests = progress.reduce((s, p) => s + p.tests_taken, 0);
      const totalStars = progress.reduce((s, p) => s + p.stars, 0);
      const accuracy = totalTests > 0 ? Math.round(progress.reduce((s, p) => s + p.best_score, 0) / (totalTests * 3) * 100) : 0;

      this.setData({
        completedTopics,
        totalTests,
        totalStars,
        accuracy,
        wrongCount: wrong.length,
        wrongList: wrong.slice(0, 3)
      });
    } catch (e) {
      console.error(e);
    }
  },

  onUsername(e) { this.setData({ username: e.detail.value }); },
  onPassword(e) { this.setData({ password: e.detail.value }); },

  async doLogin() {
    const { username, password } = this.data;
    if (!username || !password) {
      this.setData({ authError: '请填写完整' });
      return;
    }
    try {
      const res = await api.login(username, password);
      app.setToken(res.access_token);
      await app.checkAuth();
      this.setData({ user: app.globalData.user, authError: '' });
      this.loadStats();
    } catch (e) {
      this.setData({ authError: e.message || '登录失败' });
    }
  },

  switchToRegister() {
    // 简化处理：提示用户在 Web 端注册
    wx.showModal({
      title: '注册',
      content: '请在 Web 端注册账号，或使用测试账号登录',
      showCancel: false
    });
  },

  logout() {
    app.logout();
    this.setData({
      user: null,
      completedTopics: 0,
      totalTests: 0,
      accuracy: 0,
      totalStars: 0,
      wrongCount: 0,
      wrongList: []
    });
  },

  viewAllWrong() {
    wx.showToast({ title: '完整错题本请查看 Web 端', icon: 'none' });
  }
});
