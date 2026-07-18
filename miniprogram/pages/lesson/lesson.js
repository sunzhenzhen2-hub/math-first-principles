const api = require('../../utils/api');
const app = getApp();

Page({
  data: {
    topic: {},
    sections: [],
    checkQuestions: [],
    letters: ['A', 'B', 'C', 'D']
  },

  onLoad(options) {
    this.topicId = options.id;
    this.loadTopic();
  },

  async loadTopic() {
    try {
      const topic = await api.getTopic(this.topicId);
      const checkQuestions = (topic.quiz || []).slice(0, 3).map(q => ({
        ...q,
        answered: false,
        selected: -1,
        showExplanation: false
      }));

      this.setData({
        topic,
        sections: topic.lesson || [],
        checkQuestions
      });
      wx.setNavigationBarTitle({ title: topic.title });
    } catch (e) {
      wx.showToast({ title: '加载失败', icon: 'none' });
    }
  },

  checkAnswer(e) {
    const { qi, oi } = e.currentTarget.dataset;
    const questions = this.data.checkQuestions;
    if (questions[qi].answered) return;

    questions[qi].answered = true;
    questions[qi].selected = oi;
    questions[qi].showExplanation = true;
    this.setData({ checkQuestions: questions });

    // 记录错题
    if (oi !== questions[qi].answer && app.globalData.token) {
      api.addWrongAnswer({
        topic_id: this.topicId,
        question: questions[qi].question,
        user_answer: questions[qi].options[oi],
        correct_answer: questions[qi].options[questions[qi].answer],
        explanation: questions[qi].explanation
      }).catch(() => {});
    }
  },

  startQuiz() {
    wx.navigateTo({ url: '/pages/quiz/quiz?id=' + this.topicId });
  }
});
