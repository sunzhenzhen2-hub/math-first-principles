/**
 * 主应用模块 — 路由和全局状态
 */
const App = {
  currentView: 'dash',

  async init() {
    // 绑定导航按钮
    document.querySelectorAll('#nav-main button').forEach(btn => {
      btn.addEventListener('click', () => {
        const view = btn.dataset.view;
        if (view) this.showView(view);
      });
    });

    // 检查登录状态
    if (API.token) {
      try {
        await API.me();
        this.onAuth();
      } catch {
        API.setToken(null);
        this.showGuestUI();
      }
    } else {
      this.showGuestUI();
    }

    // 初始加载
    await Dashboard.load();
    Dashboard.render();
  },

  showView(view) {
    document.querySelectorAll('.sv').forEach(e => e.classList.remove('on'));
    document.querySelectorAll('#nav-main button').forEach(b => b.classList.remove('on'));

    const el = document.getElementById('v-' + view);
    if (el) el.classList.add('on');

    const btn = document.querySelector(`#nav-main button[data-view="${view}"]`);
    if (btn) btn.classList.add('on');

    this.currentView = view;

    // 视图特定逻辑
    switch (view) {
      case 'dash':
        Dashboard.load().then(() => Dashboard.render());
        break;
      case 'review':
        Progress.renderWrongBook();
        break;
      case 'report':
        Progress.renderReport();
        break;
      case 'ai-derive':
        AIDerive.render();
        break;
    }

    Dashboard.updateXP();
  },

  showAuth(mode) {
    this.showView('auth');
    if (mode === 'register') Auth.renderRegister();
    else Auth.showLogin();
  },

  showGuestUI() {
    document.getElementById('hdr-auth').style.display = 'flex';
    document.getElementById('hdr-user').style.display = 'none';
  },

  async onAuth() {
    try {
      const user = await API.me();
      document.getElementById('hdr-auth').style.display = 'none';
      document.getElementById('hdr-user').style.display = 'flex';
      document.getElementById('user-name').textContent = user.username;

      // 检查是否需要定位测试（新用户无进度时）
      const needsPlacement = await this.checkNeedsPlacement();
      if (needsPlacement) {
        Placement.start();
      } else {
        this.showView('dash');
      }
    } catch {
      this.showGuestUI();
    }
  },

  async checkNeedsPlacement() {
    try {
      const progress = await API.getProgress();
      // 如果没有任何进度，提示定位测试
      if (!progress || progress.length === 0) {
        return true;
      }
    } catch {
      // 获取进度失败，不提示
    }
    return false;
  },

  logout() {
    API.setToken(null);
    this.showGuestUI();
    this.showView('dash');
  }
};

// 启动
document.addEventListener('DOMContentLoaded', () => App.init());
