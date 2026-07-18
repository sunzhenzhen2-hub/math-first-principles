/**
 * 总览页面模块
 */
const Dashboard = {
  topics: [],
  progress: [],

  async load() {
    try {
      this.topics = await API.getTopics();
      if (API.token) {
        this.progress = await API.getProgress().catch(() => []);
      }
    } catch (e) {
      console.error('加载数据失败:', e);
    }
  },

  getProgress(topicId) {
    return this.progress.find(p => p.topic_id === topicId) || { stars: 0, tests_taken: 0, best_score: 0 };
  },

  isUnlocked(index) {
    if (index === 0) return true;
    const prevTopic = this.topics[index - 1];
    if (!prevTopic) return true;
    const prevProg = this.getProgress(prevTopic.id);
    return prevProg.stars > 0;
  },

  render() {
    const all = this.topics;
    const done = all.filter(t => this.getProgress(t.id).stars > 0).length;
    const totalQ = this.progress.reduce((s, p) => s + p.tests_taken, 0);
    const totalCorrect = this.progress.reduce((s, p) => s + p.best_score, 0);
    const acc = totalQ > 0 ? Math.round(totalCorrect / (totalQ * 3) * 100) : 0;
    const totalStars = this.progress.reduce((s, p) => s + p.stars, 0);

    document.getElementById('stats').innerHTML = `
      <div class="st"><div class="sv2">${done}/${all.length}</div><div class="sl">已完成</div></div>
      <div class="st"><div class="sv2">${acc}%</div><div class="sl">总正确率</div></div>
      <div class="st"><div class="sv2">${'⭐'.repeat(Math.min(totalStars, 5)) || '☆'}</div><div class="sl">累计星星</div></div>
      <div class="st"><div class="sv2">${totalQ}</div><div class="sl">总做题数</div></div>
    `;

    const stages = {};
    all.forEach(t => {
      if (!stages[t.stage]) stages[t.stage] = [];
      stages[t.stage].push(t);
    });

    let html = '';
    Object.entries(stages).forEach(([stageName, topics]) => {
      html += `<div class="stage-title">${stageName}</div><div class="ch-list">`;
      topics.forEach((ch, i) => {
        const globalIndex = all.findIndex(t => t.id === ch.id);
        const prog = this.getProgress(ch.id);
        const unlocked = this.isUnlocked(globalIndex);
        const cls = !unlocked ? 'locked' : prog.stars > 0 ? 'done' : '';
        const starStr = prog.stars > 0 ? '⭐'.repeat(prog.stars) + '☆'.repeat(3 - prog.stars) : '☆☆☆';
        const pct = prog.tests_taken > 0 ? Math.round(prog.best_score / (prog.tests_taken * 3) * 100) + '%' : '—';
        html += `
          <div class="ch ${cls}" onclick="${unlocked ? `Lesson.start('${ch.id}')` : ''}">
            <div class="ch-icon">${ch.icon || '📖'}</div>
            <div class="ch-info">
              <h3>${ch.title}</h3>
              <p>${ch.description || ''}</p>
              <div class="ch-stars">${starStr}</div>
            </div>
            <div class="ch-prog">${pct}</div>
          </div>
        `;
      });
      html += '</div>';
    });

    document.getElementById('stage-list').innerHTML = html;
    this.updateXP();
  },

  updateXP() {
    const total = this.topics.length;
    const done = this.topics.filter(t => this.getProgress(t.id).stars > 0).length;
    const pct = total > 0 ? Math.round(done / total * 100) : 0;
    document.getElementById('xp-t').textContent = pct + '%';
    document.getElementById('xp-f').style.width = pct + '%';
  }
};
