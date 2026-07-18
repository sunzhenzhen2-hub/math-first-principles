/**
 * 定位测试模块
 */
const Placement = {
  questions: [],
  current: 0,
  answers: [],
  done: false,

  async start() {
    try {
      this.questions = await this.fetchQuestions();
      this.current = 0;
      this.answers = [];
      this.done = false;
      this.renderQuestion();
      App.showView('placement');
    } catch (e) {
      alert('加载定位测试失败: ' + e.message);
    }
  },

  async fetchQuestions() {
    const res = await fetch(API.BASE + '/api/placement/questions');
    if (!res.ok) throw new Error('获取题目失败');
    return res.json();
  },

  renderQuestion() {
    const { questions, current } = this;
    const q = questions[current];
    const total = questions.length;
    const idx = current + 1;
    const letters = ['A', 'B', 'C', 'D'];
    const stages = ['数的起源', '代数语言', '几何直觉', '函数世界', '变化的科学', '抽象与推理', '高等数学'];

    let html = `
      <div class="qc">
        <div class="place-progress">
          <div class="place-bar"><div class="place-fill" style="width:${Math.round(idx/total*100)}%"></div></div>
          <span class="place-count">${idx} / ${total}</span>
        </div>
        <div class="place-stage-tag">${stages[q.stage_index]}</div>
        <div class="qt">${q.question}</div>
        <div class="opts" id="popts">
    `;
    q.options.forEach((o, i) => {
      html += `<div class="opt" onclick="Placement.answer(${i})"><span class="lt">${letters[i]}</span><span>${o}</span></div>`;
    });
    html += `</div>
        <div class="exp" id="pexp">💡 <b>解析：</b>${q.explanation}</div>
        <button class="nxt" id="pnxt" onclick="Placement.next()">${idx < total ? '下一题 →' : '查看结果 🏆'}</button>
      </div>
    `;

    document.getElementById('placement-body').innerHTML = html;
    this.answered = false;
  },

  answer(oi) {
    if (this.answered) return;
    this.answered = true;
    const { questions, current } = this;
    const q = questions[current];
    const ans = q.answer;

    document.querySelectorAll('#popts .opt').forEach((o, i) => {
      o.classList.add('dis');
      if (i === ans) o.classList.add('ok');
      if (i === oi && oi !== ans) o.classList.add('no');
    });

    this.answers.push({ question_id: q.id, selected: oi });

    // 显示解析和下一题按钮
    const expEl = document.getElementById('pexp');
    const nxtEl = document.getElementById('pnxt');
    if (expEl) expEl.classList.add('on');
    if (nxtEl) nxtEl.classList.add('on');
  },

  next() {
    this.current++;
    if (this.current >= this.questions.length) {
      this.showResult();
    } else {
      this.renderQuestion();
    }
  },

  async showResult() {
    try {
      const res = await fetch(API.BASE + '/api/placement/submit', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${API.token}`
        },
        body: JSON.stringify({ answers: this.answers })
      });
      if (!res.ok) throw new Error('提交失败');
      const result = await res.json();
      this.renderResult(result);
    } catch (e) {
      // 未登录也能看结果
      this.renderLocalResult();
    }
  },

  renderResult(result) {
    const stages = ['数的起源', '代数语言', '几何直觉', '函数世界', '变化的科学', '抽象与推理', '高等数学'];
    const stageIcons = ['🔢', '📐', '📏', '📈', '🔄', '🧩', '🎓'];

    let detailsHtml = '';
    result.stage_details.forEach(d => {
      const icon = d.passed ? '✅' : '❌';
      detailsHtml += `
        <div class="place-detail ${d.passed ? 'passed' : 'failed'}">
          <span class="pd-icon">${icon}</span>
          <span class="pd-name">${d.stage}</span>
          <span class="pd-score">${d.correct}/${d.total}</span>
        </div>
      `;
    });

    let html = `
      <div class="place-result">
        <div class="result-icon">🎯</div>
        <div class="result-title">定位测试完成！</div>
        <div class="result-sub">你答对了 ${result.correct_count}/${result.total_answered} 道题</div>

        <div class="place-recommend">
          <div class="pr-label">推荐从以下阶段开始：</div>
          <div class="pr-stage">
            <span class="pr-icon">${stageIcons[result.recommended_stage]}</span>
            <span class="pr-name">${result.stage_name}</span>
          </div>
        </div>

        <div class="place-details">
          <h4>答题详情</h4>
          ${detailsHtml}
        </div>

        <div class="rb">
          <button class="btn btn-g" onclick="Placement.acceptRecommendation(${result.recommended_stage})">
            🚀 从「${result.stage_name}」开始
          </button>
          <button class="btn btn-o" onclick="Placement.acceptRecommendation(0)">
            📖 从头开始
          </button>
        </div>
      </div>
    `;

    document.getElementById('placement-body').innerHTML = html;
  },

  renderLocalResult() {
    // 本地计算结果（未登录时）
    const stages = ['数的起源', '代数语言', '几何直觉', '函数世界', '变化的科学', '抽象与推理', '高等数学'];
    const stageCorrect = {};
    const stageTotal = {};

    this.answers.forEach((a, i) => {
      const q = this.questions[i];
      const si = q.stage_index;
      stageTotal[si] = (stageTotal[si] || 0) + 1;
      if (a.selected === q.answer) {
        stageCorrect[si] = (stageCorrect[si] || 0) + 1;
      }
    });

    let recommended = 0;
    for (let i = 0; i < stages.length; i++) {
      if (stageTotal[i] && stageCorrect[i] === stageTotal[i]) {
        recommended = i + 1;
      } else if (stageTotal[i]) {
        recommended = i;
        break;
      }
    }
    recommended = Math.min(recommended, stages.length - 1);

    let detailsHtml = '';
    for (let i = 0; i < stages.length; i++) {
      if (stageTotal[i]) {
        const passed = stageCorrect[i] === stageTotal[i];
        detailsHtml += `
          <div class="place-detail ${passed ? 'passed' : 'failed'}">
            <span class="pd-icon">${passed ? '✅' : '❌'}</span>
            <span class="pd-name">${stages[i]}</span>
            <span class="pd-score">${stageCorrect[i] || 0}/${stageTotal[i]}</span>
          </div>
        `;
      }
    }

    const totalCorrect = Object.values(stageCorrect).reduce((s, v) => s + v, 0);
    const totalAnswered = this.answers.length;

    let html = `
      <div class="place-result">
        <div class="result-icon">🎯</div>
        <div class="result-title">定位测试完成！</div>
        <div class="result-sub">你答对了 ${totalCorrect}/${totalAnswered} 道题</div>

        <div class="place-recommend">
          <div class="pr-label">推荐从以下阶段开始：</div>
          <div class="pr-stage">
            <span class="pr-icon">📐</span>
            <span class="pr-name">${stages[recommended]}</span>
          </div>
        </div>

        <div class="place-details">
          <h4>答题详情</h4>
          ${detailsHtml}
        </div>

        <div class="rb">
          <button class="btn btn-g" onclick="Placement.acceptRecommendation(${recommended})">
            🚀 从「${stages[recommended]}」开始
          </button>
          <button class="btn btn-o" onclick="Placement.acceptRecommendation(0)">
            📖 从头开始
          </button>
        </div>
      </div>
    `;

    document.getElementById('placement-body').innerHTML = html;
  },

  acceptRecommendation(stageIndex) {
    // 跳转到总览页面，滚动到推荐阶段
    Dashboard.load().then(() => {
      Dashboard.render();
      App.showView('dash');

      // 滚动到推荐阶段
      setTimeout(() => {
        const stageNames = ['数的起源', '代数语言', '几何直觉', '函数世界', '变化的科学', '抽象与推理', '高等数学'];
        const stageEl = document.querySelector(`.stage-title:nth-of-type(${stageIndex + 1})`);
        if (stageEl) {
          stageEl.scrollIntoView({ behavior: 'smooth', block: 'start' });
          stageEl.style.background = 'var(--accent)';
          stageEl.style.color = '#fff';
          setTimeout(() => {
            stageEl.style.background = '';
            stageEl.style.color = '';
          }, 2000);
        }
      }, 100);
    });
  }
};
