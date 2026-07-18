/**
 * 课程推导页面模块
 */
const Lesson = {
  currentTopic: null,

  async start(topicId) {
    try {
      const topic = await API.getTopic(topicId);
      this.currentTopic = topic;
      this.render(topic);
      App.showView('lesson');
    } catch (e) {
      alert('加载课程失败: ' + e.message);
    }
  },

  render(topic) {
    const body = document.getElementById('lesson-body');
    let html = `<div class="lesson"><h2>${topic.icon || '📖'} ${topic.title}</h2>`;

    topic.lesson.forEach(s => {
      switch (s.type) {
        case 'title': html += `<h3>${s.content}</h3>`; break;
        case 'text': html += `<p>${s.content}</p>`; break;
        case 'highlight': html += `<div class="hl">${s.content.replace(/\n/g, '<br>')}</div>`; break;
        case 'formula': html += `<div class="fm">${s.content.replace(/\n/g, '<br>')}</div>`; break;
        case 'ex': html += `<div class="ex">${s.content.replace(/\n/g, '<br>')}</div>`; break;
        case 'hint': html += `<div class="hl" style="border-left-color:var(--teal)">${s.content}</div>`; break;
        case 'derive': html += `<div class="derive-step"><div class="derive-num">🔬</div><div class="derive-content">${s.content.replace(/\n/g, '<br>')}</div></div>`; break;
        default: html += `<p>${s.content}</p>`;
      }
    });

    // 插入 Desmos 图形区域
    html += `<div class="gc"><div id="lesson-graph" class="desmos-container"></div></div>`;

    // 理解检查
    if (topic.quiz && topic.quiz.length > 0) {
      html += `<h3 style="margin-top:24px;color:var(--accent)">✋ 理解检查</h3>`;
      html += `<p style="font-size:0.85rem;color:var(--ink-muted);margin-bottom:12px">快速检验你是否理解了本节内容</p>`;
      const checkQs = topic.quiz.slice(0, 3);
      checkQs.forEach((q, i) => {
        const letters = ['A', 'B', 'C', 'D'];
        html += `<div class="qc"><div class="qn">理解检查 ${i + 1}</div><div class="qt">${q.question}</div><div class="opts" id="ck${i}">`;
        q.options.forEach((o, j) => {
          html += `<div class="opt" onclick="Lesson.checkAnswer(${i},${j},${q.answer})"><span class="lt">${letters[j]}</span><span>${o}</span></div>`;
        });
        html += `</div><div class="exp" id="cke${i}">💡 ${q.explanation}</div></div>`;
      });
    }

    html += `</div>`;
    html += `<button class="btn btn-g" onclick="Quiz.start('${topic.id}')" style="width:100%;margin-top:12px">📝 开始章节测试 →</button>`;

    body.innerHTML = html;

    // 创建 Desmos 图形
    setTimeout(() => this.createGraph(topic), 200);
  },

  createGraph(topic) {
    const graphConfigs = {
      '变量与函数': [{ latex: 'y=x^2' }, { latex: 'y=2x+1', color: '#1a6a6a' }],
      '一次函数': [{ latex: 'y=2x+1' }],
      '二次函数': [{ latex: 'y=x^2-4x+3' }, { latex: 'y=(x-2)^2-1', color: '#1a6a6a' }],
      '指数与对数': [{ latex: 'y=2^x' }, { latex: 'y=\\ln(x)', color: '#1a6a6a' }],
      '三角函数': [{ latex: 'y=\\sin(x)' }, { latex: 'y=\\cos(x)', color: '#1a6a6a' }],
      '斜率': [{ latex: 'y=x^2' }, { latex: 'y=2(x-1)+1', color: '#2a7a4a' }],
      '导数': [{ latex: 'y=x^3-3x' }],
      '勾股定理': [{ latex: 'x^2+y^2=25', color: '#1a6a6a' }, { latex: 'y=0', color: '#888' }, { latex: 'x=0', color: '#888' }],
      '三角形': [{ latex: 'y=0' }, { latex: 'y=2x' }, { latex: 'y=-2x+8', color: '#1a6a6a' }],
      '圆': [{ latex: 'x^2+y^2=9', color: '#c87832' }],
      '极限': [{ latex: 'y=\\sin(x)/x' }, { latex: 'y=1', color: '#888', lineStyle: 'dashed' }],
      '定积分': [{ latex: 'y=x^2' }, { latex: '0<x<1\\{0<y<x^2\\}', color: '#c87832', fill: true }],
      '泰勒展开': [{ latex: 'y=e^x', color: '#1a6a6a' }, { latex: 'y=1+x+x^2/2+x^3/6', color: '#c87832' }],
      '等差数列': [{ latex: '(n, 2n+1)', pointSize: 8, color: '#c87832' }],
      '等比数列': [{ latex: '(n, 2^n)', pointSize: 8, color: '#1a6a6a' }],
      '排列组合': [{ latex: 'y=\\binom{10}{x}', pointSize: 8, color: '#c87832' }],
    };

    const exprs = graphConfigs[topic.title] || [{ latex: 'y=x^2' }];
    Graph.create('lesson-graph', {
      expressions: exprs,
      bounds: { left: -6, right: 6, bottom: -5, top: 10 }
    });
  },

  checkAnswer(qi, oi, ans) {
    const c = document.getElementById('ck' + qi);
    if (c.querySelector('.dis')) return;
    c.querySelectorAll('.opt').forEach((o, i) => {
      o.classList.add('dis');
      if (i === ans) o.classList.add('ok');
      if (i === oi && oi !== ans) o.classList.add('no');
    });
    document.getElementById('cke' + qi).classList.add('on');

    // 记录错题
    if (oi !== ans && this.currentTopic && API.token) {
      const q = this.currentTopic.quiz[qi];
      API.addWrongAnswer({
        topic_id: this.currentTopic.id,
        question: q.question,
        user_answer: q.options[oi],
        correct_answer: q.options[ans],
        explanation: q.explanation
      }).catch(() => {});
    }
  }
};
