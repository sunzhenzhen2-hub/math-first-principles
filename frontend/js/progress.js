/**
 * 进度同步和报告模块
 */
const Progress = {
  async renderWrongBook() {
    if (!API.token) {
      document.getElementById('wb-list').innerHTML = '<p style="color:var(--ink-muted)">请先登录</p>';
      return;
    }

    try {
      const wrong = await API.getWrongAnswers();
      const list = document.getElementById('wb-list');
      const empty = document.getElementById('wb-empty');

      if (wrong.length === 0) { empty.style.display = 'block'; list.innerHTML = ''; return; }
      empty.style.display = 'none';

      const grouped = {};
      wrong.forEach(w => {
        const topic = Dashboard.topics.find(t => t.id === w.topic_id);
        const key = topic ? topic.title : w.topic_id;
        if (!grouped[key]) grouped[key] = [];
        grouped[key].push(w);
      });

      let html = '';
      Object.entries(grouped).forEach(([title, items]) => {
        html += `<h4 style="color:var(--teal);margin:14px 0 8px;font-size:0.88rem;font-family:var(--font-display)">${title} (${items.length}题)</h4>`;
        items.slice(-5).reverse().forEach(w => {
          html += `
            <div class="wi">
              <div class="wq">${w.question}</div>
              <div class="wa">✅ ${w.correct_answer}</div>
              <div class="wu">❌ ${w.user_answer}</div>
              ${w.explanation ? `<div style="font-size:0.78rem;color:var(--ink-muted);margin-top:5px">💡 ${w.explanation}</div>` : ''}
              <button class="btn btn-sm btn-o" style="margin-top:6px" onclick="Progress.deleteWrong(${w.id})">删除</button>
            </div>
          `;
        });
      });
      list.innerHTML = html;
    } catch (e) {
      console.error('加载错题本失败:', e);
    }
  },

  async deleteWrong(id) {
    try {
      await API.deleteWrongAnswer(id);
      this.renderWrongBook();
    } catch (e) {
      alert('删除失败: ' + e.message);
    }
  },

  async renderReport() {
    if (!API.token) {
      document.getElementById('report-body').innerHTML = '<div class="wb"><p style="color:var(--ink-muted)">请先登录查看学习报告</p></div>';
      return;
    }

    const body = document.getElementById('report-body');
    await Dashboard.load();
    const progress = Dashboard.progress;
    const topics = Dashboard.topics;

    const totalTests = progress.reduce((s, p) => s + p.tests_taken, 0);
    const totalPassed = progress.reduce((s, p) => s + p.tests_passed, 0);
    const acc = totalTests > 0 ? Math.round(totalPassed / totalTests * 100) : 0;
    const level = Math.floor(totalPassed / 5) + 1;

    let html = `
      <div class="stats">
        <div class="st"><div class="sv2">${totalTests}</div><div class="sl">总做题数</div></div>
        <div class="st"><div class="sv2" style="color:${acc >= 70 ? 'var(--success)' : 'var(--danger)'}">${acc}%</div><div class="sl">总正确率</div></div>
        <div class="st"><div class="sv2">${level}</div><div class="sl">当前等级</div></div>
        <div class="st"><div class="sv2">${progress.filter(p => p.stars >= 2).length}</div><div class="sl">已掌握</div></div>
      </div>
    `;

    // 薄弱环节
    const weak = progress.filter(p => p.tests_taken > 0 && p.best_score / (p.tests_taken * 3) < 0.7);
    if (weak.length > 0) {
      html += `<div class="wb"><h3>🔴 薄弱环节</h3>`;
      weak.forEach(p => {
        const topic = topics.find(t => t.id === p.topic_id);
        if (!topic) return;
        const pct = Math.round(p.best_score / (p.tests_taken * 3) * 100);
        html += `<div class="wi" style="display:flex;justify-content:space-between;align-items:center">
          <div><span class="wq">${topic.icon} ${topic.title}</span></div>
          <div style="text-align:right"><span style="color:var(--danger);font-weight:700">${pct}%</span><br>
          <button class="btn btn-sm btn-o" style="margin-top:4px" onclick="Quiz.start('${p.topic_id}')">重新测试</button></div></div>`;
      });
      html += `</div>`;
    }

    // 已掌握
    const strong = progress.filter(p => p.stars >= 2);
    if (strong.length > 0) {
      html += `<div class="wb"><h3>🟢 已掌握</h3>`;
      strong.forEach(p => {
        const topic = topics.find(t => t.id === p.topic_id);
        if (!topic) return;
        html += `<div class="wi" style="display:flex;justify-content:space-between"><span class="wq">${topic.icon} ${topic.title}</span><span class="strong-tag">${'⭐'.repeat(p.stars)}</span></div>`;
      });
      html += `</div>`;
    }

    // 未测试
    const tested = new Set(progress.filter(p => p.tests_taken > 0).map(p => p.topic_id));
    const notDone = topics.filter(t => !tested.has(t.id));
    if (notDone.length > 0) {
      html += `<div class="wb"><h3>⚪ 未测试</h3>`;
      notDone.slice(0, 8).forEach(t => {
        html += `<div class="wi" style="display:flex;justify-content:space-between;align-items:center">
          <span class="wq">${t.icon} ${t.title}</span>
          <button class="btn btn-sm btn-g" onclick="Quiz.start('${t.id}')">去测试</button></div>`;
      });
      html += `</div>`;
    }

    body.innerHTML = html;
  }
};
