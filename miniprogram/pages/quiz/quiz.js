const api = require('../../utils/api');
const app = getApp();

Page({
  data: {
    title: '',
    question: {},
    questions: [],
    current: 0,
    total: 0,
    correct: 0,
    answered: false,
    selected: -1,
    showExplanation: false,
    showResult: false,
    letters: ['A', 'B', 'C', 'D'],
    resultIcon: '',
    resultTitle: '',
    starsStr: '',
    pct: 0
  },

  onLoad(options) {
    this.topicId = options.id;
    this.loadQuiz();
  },

  async loadQuiz() {
    try {
      const topic = await api.getTopic(this.topicId);
      const questions = (topic.quiz || []).map(q => {
        const opts = [...q.options];
        const correctText = opts[q.answer];
        for (let i = opts.length - 1; i > 0; i--) {
          const j = Math.floor(Math.random() * (i + 1));
          [opts[i], opts[j]] = [opts[j], opts[i]];
        }
        return { ...q, options: opts, answer: opts.indexOf(correctText) };
      });

      this.setData({
        title: topic.title,
        questions,
        total: questions.length,
        question: questions[0],
        current: 0,
        correct: 0,
        answered: false,
        showResult: false
      });
    } catch (e) {
      wx.showToast({ title: '加载失败', icon: 'none' });
    }
  },

  answer(e) {
    if (this.data.answered) return;
    const oi = e.currentTarget.dataset.oi;
    const { questions, current } = this.data;
    const ans = questions[current].answer;

    this.setData({
      answered: true,
      selected: oi,
      showExplanation: true,
      correct: oi === ans ? this.data.correct + 1 : this.data.correct
    });

    // 记录错题
    if (oi !== ans && app.globalData.token) {
      api.addWrongAnswer({
        topic_id: this.topicId,
        question: questions[current].question,
        user_answer: questions[current].options[oi],
        correct_answer: questions[current].options[ans],
        explanation: questions[current].explanation
      }).catch(() => {});
    }
  },

  next() {
    const { questions, current, correct, total } = this.data;
    if (current + 1 >= total) {
      this.showResult();
    } else {
      this.setData({
        current: current + 1,
        question: questions[current + 1],
        answered: false,
        selected: -1,
        showExplanation: false
      });
    }
  },

  async showResult() {
    const { correct, total } = this.data;
    const pct = Math.round(correct / total * 100);
    const stars = pct >= 90 ? 3 : pct >= 70 ? 2 : pct >= 40 ? 1 : 0;
    const icons = ['💪', '👍', '🎉', '🏆'];
    const titles = ['再接再厉', '勉强及格', '通过！', '完美通关！'];

    // 保存进度
    if (app.globalData.token) {
      try { await api.updateProgress(this.topicId, stars, correct, total); } catch {}
    }

    this.setData({
      showResult: true,
      resultIcon: icons[stars],
      resultTitle: titles[stars],
      starsStr: '⭐'.repeat(stars) + '☆'.repeat(3 - stars),
      pct
    });
  },

  retry() {
    this.loadQuiz();
  },

  goBack() {
    wx.navigateBack();
  }
});
