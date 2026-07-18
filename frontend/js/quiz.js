/**
 * 测验系统模块
 */
const Quiz = {
  state: null,

  async start(topicId) {
    try {
      const topic = await API.getTopic(topicId);
      const questions = topic.quiz.map(q => {
        const opts = [...q.options];
        const correctText = opts[q.answer];
        // 打乱选项
        for (let i = opts.length - 1; i > 0; i--) {
          const j = Math.floor(Math.random() * (i + 1));
          [opts[i], opts[j]] = [opts[j], opts[i]];
        }
        return { ...q, options: opts, answer: opts.indexOf(correctText) };
      });

      this.state = { topicId, title: topic.title, questions, current: 0, correct: 0 };
      this.renderQuestion();
      App.showView('quiz');
    } catch (e) {
      alert('加载测验失败: ' + e.message);
    }
  },

  renderQuestion() {
    const { questions, current, title } = this.state;
    const q = questions[current];
    const total = questions.length;
    const idx = current + 1;
    const letters = ['A', 'B', 'C', 'D'];

    let html = `<div class="qc"><div class="qn">${title} · 第 ${idx}/${total} 题</div><div class="qt">${q.question}</div><div class="opts" id="qopts">`;
    q.options.forEach((o, i) => {
      html += `<div class="opt" onclick="Quiz.answer(${i})"><span class="lt">${letters[i]}</span><span>${o}</span></div>`;
    });
    html += `</div><div class="exp" id="qexp">💡 <b>解析：</b>${q.explanation}</div></div>`;
    html += `<button class="nxt" id="qnxt" onclick="Quiz.next()">${idx < total ? '下一题 →' : '查看结果 🏆'}</button>`;

    document.getElementById('quiz-body').innerHTML = html;
    this.state.answered = false;
  },

  answer(oi) {
    if (this.state.answered) return;
    this.state.answered = true;
    const { questions, current } = this.state;
    const ans = questions[current].answer;

    document.querySelectorAll('#qopts .opt').forEach((o, i) => {
      o.classList.add('dis');
      if (i === ans) o.classList.add('ok');
      if (i === oi && oi !== ans) o.classList.add('no');
    });

    if (oi === ans) this.state.correct++;
    document.getElementById('qexp').classList.add('on');
    document.getElementById('qnxt').classList.add('on');

    // 记录错题
    if (oi !== ans && API.token) {
      const q = questions[current];
      API.addWrongAnswer({
        topic_id: this.state.topicId,
        question: q.question,
        user_answer: q.options[oi],
        correct_answer: q.options[ans],
        explanation: q.explanation
      }).catch(() => {});
    }
  },

  next() {
    this.state.current++;
    if (this.state.current >= this.state.questions.length) {
      this.showResult();
    } else {
      this.renderQuestion();
    }
  },

  async showResult() {
    const { topicId, correct, questions, title } = this.state;
    const total = questions.length;
    const pct = Math.round(correct / total * 100);
    const stars = pct >= 90 ? 3 : pct >= 70 ? 2 : pct >= 40 ? 1 : 0;
    const icon = stars >= 3 ? '🏆' : stars >= 2 ? '🎉' : stars >= 1 ? '👍' : '💪';
    const titleText = stars >= 3 ? '完美通关！' : stars >= 2 ? '通过！' : stars >= 1 ? '勉强及格' : '再接再厉';

    // 保存进度
    if (API.token) {
      try { await API.updateProgress(topicId, stars, correct, total); } catch (e) { console.error(e); }
    }

    let html = `
      <div class="result-icon">${icon}</div>
      <div class="result-title">${titleText}</div>
      <div class="result-sub">${title}</div>
      <div class="result-stars">${'⭐'.repeat(stars)}${'☆'.repeat(3 - stars)}</div>
      <div class="result-score">${correct} / ${total}</div>
      <div class="wb">
        <div class="wi"><span class="wq">正确率</span> <span style="color:var(--accent);font-weight:700">${pct}%</span></div>
        <div class="wi"><span class="wq">星星</span> <span>${'⭐'.repeat(stars)}</span></div>
      </div>
      <div class="rb">
        <button class="btn btn-o" onclick="Quiz.start('${topicId}')">🔄 重做</button>
        <button class="btn btn-g" onclick="App.showView('dash')">📊 返回总览</button>
      </div>
    `;

    document.getElementById('result-body').innerHTML = html;
    App.showView('result');
    Dashboard.load().then(() => Dashboard.render());
  }
};
