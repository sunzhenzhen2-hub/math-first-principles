/**
 * AI 推导模块 — 公理 / 定理 / 证明过程（含图形）
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

  /** 优先用 proof，否则用 steps */
  getProofSteps(content) {
    if (content.proof && content.proof.length) return content.proof;
    if (content.steps && content.steps.length) return content.steps;
    return [];
  },

  renderGraphs(steps) {
    if (!steps || !steps.length) return;
    // 等布局完成后再画，避免容器宽度为 0
    const draw = () => {
      steps.forEach((step, i) => {
        if (step.graph && step.graph.expressions) {
          const graphId = `graph-step-${i}`;
          const el = document.getElementById(graphId);
          if (!el) {
            console.warn('[AIDerive] graph container missing:', graphId);
            return;
          }
          el.style.width = '100%';
          el.style.minHeight = '360px';
          el.style.height = '360px';
          const success = Graph.create(graphId, {
            expressions: step.graph.expressions,
            bounds: step.graph.bounds || { left: -10, right: 10, bottom: -10, top: 10 },
          });
          if (success) this.graphInstances.push(graphId);
        }
      });
    };
    requestAnimationFrame(() => requestAnimationFrame(draw));
  },

  escapeHtml(text) {
    if (text == null) return '';
    return String(text)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;');
  },

  buildResultHtml(content, cached) {
    let html = `<div class="lesson" style="margin-top:0">`;
    if (cached) {
      html += `<p class="ai-cache-tag">缓存内容</p>`;
    }

    // 1. 公理（正式陈述）
    if (content.axioms && content.axioms.length) {
      html += `<div class="ai-block ai-axioms">
        <h3 class="ai-block-title">公理 / 基本定义</h3>
        <ul class="ai-axiom-list">`;
      content.axioms.forEach(ax => {
        html += `<li class="ai-axiom-card">
          <strong>${this.escapeHtml(ax.name || '公理')}</strong>
          <p class="ai-axiom-stmt">${this.escapeHtml(ax.statement || '')}</p>
          ${ax.plain ? `<p class="ai-axiom-plain">说明：${this.escapeHtml(ax.plain)}</p>` : ''}
        </li>`;
      });
      html += `</ul></div>`;
    }

    // 2. 定理
    if (content.theorem) {
      const th = content.theorem;
      html += `<div class="ai-block ai-theorem">
        <h3 class="ai-block-title">定理</h3>
        <p class="ai-theorem-name">${this.escapeHtml(th.name || '')}</p>
        <p class="ai-theorem-stmt"><b>陈述：</b>${this.escapeHtml(th.statement || '')}</p>
        ${th.plain ? `<p class="ai-theorem-plain">释义：${this.escapeHtml(th.plain)}</p>` : ''}
      </div>`;
    }

    // 3. 已知 / 求证
    if (content.given || content.to_prove) {
      html += `<div class="ai-block ai-given">
        <h3 class="ai-block-title">已知与求证</h3>`;
      if (content.given) {
        html += `<p><b>已知：</b>${this.escapeHtml(content.given)}</p>`;
      }
      if (content.to_prove) {
        html += `<p><b>求证：</b>${this.escapeHtml(content.to_prove)}</p>`;
      }
      html += `</div>`;
    }

    // 4. 证明过程
    const proofSteps = this.getProofSteps(content);
    if (proofSteps.length) {
      html += `<div class="ai-block ai-steps-wrap">
        <h3 class="ai-block-title">证明</h3>`;
      proofSteps.forEach((step, i) => {
        html += `<div class="ai-step">`;
        html += `<h4>${i + 1}. ${this.escapeHtml(step.title || '')}</h4>`;
        html += `<p>${this.escapeHtml(step.content || '')}</p>`;
        if (step.formula) html += `<div class="fm">${this.escapeHtml(step.formula)}</div>`;
        if (step.reason) {
          html += `<div class="ai-reason"><b>依据：</b>${this.escapeHtml(step.reason)}</div>`;
        }
        if (step.example) {
          html += `<div class="ex"><b>验算：</b>${this.escapeHtml(step.example)}</div>`;
        }
        if (step.graph && step.graph.expressions) {
          const graphId = `graph-step-${i}`;
          html += `<div class="gc"><div id="${graphId}" class="desmos-container"></div>`;
          if (step.graph.description) {
            html += `<p class="graph-desc">${this.escapeHtml(step.graph.description)}</p>`;
          }
          html += `</div>`;
        }
        html += `</div>`;
      });
      html += `</div>`;
    } else if (content.error) {
      html += `<div class="hl" style="border-left-color:var(--danger)">${this.escapeHtml(content.error)}</div>`;
    }

    if (content.plain_summary) {
      html += `<div class="ai-block ai-summary">
        <h3 class="ai-block-title">结论</h3>
        <p>${this.escapeHtml(content.plain_summary)}</p>
      </div>`;
    }

    html += `</div>`;
    return html;
  },

  async generate() {
    if (!API.token) {
      document.getElementById('ai-derive-result').innerHTML =
        `<div class="hl" style="border-left-color:var(--danger)">请先登录</div>`;
      return;
    }

    this.destroyGraphs();
    const result = document.getElementById('ai-derive-result');
    result.innerHTML =
      `<div class="ai-loading">生成证明中…</div>`;

    try {
      const resp = await API.aiDerive(this.selectedTopic);
      const raw = resp.content;
      let content;

      if (typeof raw === 'object' && raw !== null) {
        content = raw;
      } else if (typeof raw === 'string') {
        try {
          const parsed = JSON.parse(raw);
          content = typeof parsed === 'string' ? JSON.parse(parsed) : parsed;
        } catch (e) {
          content = { steps: [{ title: '推导结果', content: raw || '无内容' }] };
        }
      } else {
        content = { steps: [{ title: '推导结果', content: '无内容' }] };
      }

      result.innerHTML = this.buildResultHtml(content, resp.cached);
      this.renderGraphs(this.getProofSteps(content));
    } catch (e) {
      console.error('[AIDerive] Generate error:', e);
      result.innerHTML =
        `<div class="hl" style="border-left-color:var(--danger)">生成失败：${this.escapeHtml(e.message)}</div>`;
    }
  }
};
