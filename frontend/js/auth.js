/**
 * 认证模块 — 登录/注册 UI
 */
const Auth = {
  renderLogin() {
    return `
      <h2>🔐 登录</h2>
      <div class="field"><label>用户名</label><input id="auth-user" type="text" placeholder="输入用户名"></div>
      <div class="field"><label>密码</label><input id="auth-pass" type="password" placeholder="输入密码"></div>
      <button class="btn btn-g auth-btn" onclick="Auth.doLogin()">登录</button>
      <div class="auth-switch">没有账号？<a onclick="Auth.renderRegister()">注册</a></div>
      <div class="auth-error" id="auth-err"></div>
    `;
  },

  renderRegister() {
    document.getElementById('auth-card').innerHTML = `
      <h2>📝 注册</h2>
      <div class="field"><label>用户名</label><input id="auth-user" type="text" placeholder="起个名字"></div>
      <div class="field"><label>邮箱</label><input id="auth-email" type="email" placeholder="your@email.com"></div>
      <div class="field"><label>密码</label><input id="auth-pass" type="password" placeholder="设置密码"></div>
      <button class="btn btn-g auth-btn" onclick="Auth.doRegister()">注册</button>
      <div class="auth-switch">已有账号？<a onclick="Auth.showLogin()">登录</a></div>
      <div class="auth-error" id="auth-err"></div>
    `;
  },

  showLogin() {
    document.getElementById('auth-card').innerHTML = this.renderLogin();
  },

  async doLogin() {
    const u = document.getElementById('auth-user').value.trim();
    const p = document.getElementById('auth-pass').value;
    if (!u || !p) { document.getElementById('auth-err').textContent = '请填写完整'; return; }
    try {
      await API.login(u, p);
      App.onAuth();
    } catch (e) {
      document.getElementById('auth-err').textContent = e.message;
    }
  },

  async doRegister() {
    const u = document.getElementById('auth-user').value.trim();
    const e = document.getElementById('auth-email').value.trim();
    const p = document.getElementById('auth-pass').value;
    if (!u || !e || !p) { document.getElementById('auth-err').textContent = '请填写完整'; return; }
    try {
      await API.register(u, e, p);
      App.onAuth();
    } catch (err) {
      document.getElementById('auth-err').textContent = err.message;
    }
  }
};
