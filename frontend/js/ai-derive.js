/**
 * AI 推导模块
 */
const AIDerive = {
  selectedTopic: null,

  async render() {
    await Dashboard.load();
    const topics = Dashboard.topics;
    const select = document.getElementById('ai-topic-select');
    select.innerHTML = topics.map(t =>
      `<button class="ai-topic-btn" data-id="${t.id}" onclick="AIDerive.select('${t.id}')">${t.icon} ${t.title}</button>`
    ).join('');
    document.getElementById('ai-derive-result').innerHTML = '';
  },

  select(topicId) {
    this.selectedTopic = topicId;
    document.querySelectorAll('.ai-topic-btn').forEach(b => b.classList.remove('on'));
    document.querySelector(`.ai-topic-btn[data-id="${topicId}"]`)?.classList.add('on');
    this.generate();
  },

  async generate() {
    if (!API.token) {
      document.getElementById('ai-derive-result').innerHTML = `<div class="hl" style="border-left-color:var(--danger)">请先登录后再使用 AI 推导功能</div>`;
      return;
    }

    const result = document.getElementById('ai-derive-result');
    result.innerHTML = `<div class="ai-loading">🤖 AI 正在从第一性原理推导中...<br><small>这可能需要几秒钟</small></div>`;

    try {
      const resp = await API.aiDerive(this.selectedTopic);
      let content;
      try { content = JSON.parse(resp.content); } catch { content = { steps: [{ title: '推导结果', content: resp.content }] }; }

      let html = `<div class="lesson" style="margin-top:0">`;
      if (resp.cached) html += `<p style="font-size:0.75rem;color:var(--ink-muted);margin-bottom:12px">📦 缓存内容</p>`;

      if (content.steps) {
        content.steps.forEach((step, i) => {
          html += `<div class="ai-step">`;
          html += `<h4>步骤 ${i + 1}：${step.title}</h4>`;
          html += `<p>${step.content}</p>`;
          if (step.formula) html += `<div class="fm">${step.formula}</div>`;
          if (step.hint) html += `<div class="hl" style="border-left-color:var(--teal)">${step.hint}</div>`;
          html += `</div>`;
        });
      } else if (content.error) {
        html += `<div class="hl" style="border-left-color:var(--danger)">${content.error}</div>`;
      } else {
        html += `<p>${resp.content}</p>`;
      }

      html += `</div>`;
      result.innerHTML = html;
    } catch (e) {
      result.innerHTML = `<div class="hl" style="border-left-color:var(--danger)">生成失败：${e.message}</div>`;
    }
  }
};
