/**
 * 小程序入口
 */
App({
  globalData: {
    baseUrl: '', // 部署后填入后端地址
    token: '',
    user: null,
    topics: [],
    progress: []
  },

  onLaunch() {
    // 从缓存读取 token
    const token = wx.getStorageSync('math_token');
    if (token) {
      this.globalData.token = token;
      this.checkAuth();
    }
    // 加载主题数据
    this.loadTopics();
  },

  async loadTopics() {
    try {
      const res = await this.request('/api/topics');
      this.globalData.topics = res;
    } catch (e) {
      console.error('加载主题失败:', e);
    }
  },

  async checkAuth() {
    try {
      const user = await this.request('/api/auth/me');
      this.globalData.user = user;
    } catch {
      this.globalData.token = '';
      wx.removeStorageSync('math_token');
    }
  },

  request(path, opts = {}) {
    const that = this;
    return new Promise((resolve, reject) => {
      wx.request({
        url: that.globalData.baseUrl + path,
        method: opts.method || 'GET',
        data: opts.data || {},
        header: {
          'Content-Type': 'application/json',
          ...(that.globalData.token ? { 'Authorization': 'Bearer ' + that.globalData.token } : {})
        },
        success(res) {
          if (res.statusCode === 401) {
            that.globalData.token = '';
            wx.removeStorageSync('math_token');
            reject(new Error('请重新登录'));
          } else if (res.statusCode >= 200 && res.statusCode < 300) {
            resolve(res.data);
          } else {
            reject(new Error(res.data?.detail || '请求失败'));
          }
        },
        fail: reject
      });
    });
  },

  setToken(token) {
    this.globalData.token = token;
    wx.setStorageSync('math_token', token);
  },

  logout() {
    this.globalData.token = '';
    this.globalData.user = null;
    wx.removeStorageSync('math_token');
  }
});
