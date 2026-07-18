const api = require('../../utils/api');
const app = getApp();

Page({
  data: {
    stages: [],
    completed: 0,
    total: 0,
    accuracy: 0,
    stars: 0,
    progressPercent: 0,
    showLogin: false,
    username: '',
    password: '',
    authError: ''
  },

  onLoad() {
    this.loadData();
  },

  onShow() {
    this.loadData();
  },

  async loadData() {
    try {
      const topics = await api.getTopics();
      let progress = [];
      if (app.globalData.token) {
        progress = await api.getProgress().catch(() => []);
      }
      app.globalData.topics = topics;
      app.globalData.progress = progress;

      // 按阶段分组
      const stageMap = {};
      topics.forEach(t => {
        if (!stageMap[t.stage]) stageMap[t.stage] = { name: t.stage, topics: [] };
        const prog = progress.find(p => p.topic_id === t.id) || { stars: 0, tests_taken: 0 };
        const idx = topics.indexOf(t);
        const unlocked = idx === 0 || (progress.find(p => p.topic_id === topics[idx - 1]?.id)?.stars > 0);
        stageMap[t.stage].topics.push({
          ...t,
          stars: prog.stars,
          locked: !unlocked,
          done: prog.stars > 0,
          starsStr: prog.stars > 0 ? '⭐'.repeat(prog.stars) + '☆'.repeat(3 - prog.stars) : '☆☆☆',
          pct: prog.tests_taken > 0 ? Math.round(prog.stars / 3 * 100) + '%' : '—'
        });
      });

      const stages = Object.values(stageMap);
      const completed = topics.filter(t => progress.find(p => p.topic_id === t.id && p.stars > 0).length).length;
      const totalStars = progress.reduce((s, p) => s + p.stars, 0);
      const totalTests = progress.reduce((s, p) => s + p.tests_taken, 0);

      this.setData({
        stages,
        completed: progress.filter(p => p.stars > 0).length,
        total: topics.length,
        accuracy: totalTests > 0 ? Math.round(progress.reduce((s, p) => s + p.best_score, 0) / (totalTests * 3) * 100) : 0,
        stars: totalStars,
        progressPercent: topics.length > 0 ? Math.round(progress.filter(p => p.stars > 0).length / topics.length * 100) : 0
      });
    } catch (e) {
      console.error('加载失败:', e);
    }
  },

  goLesson(e) {
    const id = e.currentTarget.dataset.id;
    const topic = app.globalData.topics.find(t => t.id === id);
    const progress = app.globalData.progress.find(p => p.topic_id === id);
    if (!progress || progress.stars === 0) {
      // 检查是否解锁
      const idx = app.globalData.topics.findIndex(t => t.id === id);
      if (idx > 0) {
        const prevId = app.globalData.topics[idx - 1].id;
        const prevProg = app.globalData.progress.find(p => p.topic_id === prevId);
        if (!prevProg || prevProg.stars === 0) {
          wx.showToast({ title: '请先完成前面的课程', icon: 'none' });
          return;
        }
      }
    }
    wx.navigateTo({ url: '/pages/lesson/lesson?id=' + id });
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
      this.setData({ showLogin: false, authError: '' });
      this.loadData();
    } catch (e) {
      this.setData({ authError: e.message || '登录失败' });
    }
  },

  showRegister() {
    this.setData({ showLogin: false });
    wx.navigateTo({ url: '/pages/profile/profile?mode=register' });
  },

  hideLogin() {
    this.setData({ showLogin: false });
  }
});
