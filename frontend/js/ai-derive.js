/**
 * AI 推导模块 — 增强版（含图形）
 */
const AIDerive = {
  selectedTopic: null,
  graphInstances: [],

  async render() {
    await Dashboard.load();
    const topics = Dashboard.topics;
    const select = document.getElementById('ai-topic-select');
    select.innerHTML = topics.map(t =>
      `<button class="ai-topic-btn" data-id="${t.id}" onclick="AIDerive.select('${t.id}')">${t.icon} ${t.title}</button>`
    ).join('');
    document.getElementById('ai-derive-result').innerHTML = '';
    this.destroyGraphs();
  },

  select(topicId) {
    this.selectedTopic = topicId;
    document.querySelectorAll('.ai-topic-btn').forEach(b => b.classList.remove('on'));
    document.querySelector(`.ai-topic-btn[data-id="${topicId}"]`)?.classList.add('on');
    this.generate();
  },

  destroyGraphs() {
    Graph.destroyAll();
    this.graphInstances = [];
  },

  renderGraphs(steps) {
    console.log('[AIDerive] Rendering graphs...');

    steps.forEach((step, i) => {
      if (step.graph && step.graph.expressions) {
        const graphId = `graph-step-${i}`;
        const el = document.getElementById(graphId);

        if (el) {
          console.log(`[AIDerive] Creating graph for step ${i}: ${graphId}`);

          // 确保容器有正确的尺寸
          el.style.width = '100%';
          el.style.height = '360px';

          const success = Graph.create(graphId, {
            expressions: step.graph.expressions,
            bounds: step.graph.bounds || { left: -10, right: 10, bottom: -10, top: 10 },
            keypad: false,
            topbar: false
          });

          if (success) {
            this.graphInstances.push(graphId);
            console.log(`[AIDerive] Graph created successfully: ${graphId}`);
          } else {
            console.error(`[AIDerive] Failed to create graph: ${graphId}`);
          }
        } else {
          console.warn(`[AIDerive] Container not found: ${graphId}`);
        }
      }
    });
  },

  async generate() {
    if (!API.token) {
      document.getElementById('ai-derive-result').innerHTML = `<div class="hl" style="border-left-color:var(--danger)">请先登录后再使用 AI 推导功能</div>`;
      return;
    }

    this.destroyGraphs();
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
          if (step.example) html += `<div class="ex"><b>例：</b>${step.example}</div>`;

          // 渲染图形容器
          if (step.graph && step.graph.expressions) {
            const graphId = `graph-step-${i}`;
            html += `<div class="gc"><div id="${graphId}" class="desmos-container"></div>`;
            if (step.graph.description) {
              html += `<p class="graph-desc">${step.graph.description}</p>`;
            }
            html += `</div>`;
          }

          html += `</div>`;
        });
      } else if (content.error) {
        html += `<div class="hl" style="border-left-color:var(--danger)">${content.error}</div>`;
      } else {
        html += `<p>${resp.content}</p>`;
      }

      html += `</div>`;
      result.innerHTML = html;

      // 渲染图形
      this.renderGraphs(content.steps);

    } catch (e) {
      console.error('[AIDerive] Generate error:', e);
      result.innerHTML = `<div class="hl" style="border-left-color:var(--danger)">生成失败：${e.message}</div>`;
    }
  }
};
