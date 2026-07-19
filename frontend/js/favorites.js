/**
 * 收藏与笔记模块
 */
const Favorites = {
  currentTab: 'favorites',

  async render() {
    if (!API.token) {
      document.getElementById('favorites-body').innerHTML = '<div class="wb"><p style="color:var(--ink-muted)">请先登录</p></div>';
      return;
    }

    const body = document.getElementById('favorites-body');
    body.innerHTML = this._renderTabs() + '<div id="favorites-content"></div>';

    this.switchTab('favorites');
  },

  _renderTabs() {
    return `
      <div class="tab-bar">
        <button class="tab-btn ${this.currentTab === 'favorites' ? 'active' : ''}" onclick="Favorites.switchTab('favorites')">❤️ 收藏</button>
        <button class="tab-btn ${this.currentTab === 'notes' ? 'active' : ''}" onclick="Favorites.switchTab('notes')">📝 笔记</button>
      </div>
    `;
  },

  async switchTab(tab) {
    this.currentTab = tab;
    const content = document.getElementById('favorites-content');
    if (!content) return;

    // 更新标签样式
    document.querySelectorAll('.tab-btn').forEach(btn => {
      btn.classList.toggle('active', btn.textContent.includes(tab === 'favorites' ? '收藏' : '笔记'));
    });

    content.innerHTML = '<div class="loading">加载中...</div>';

    try {
      if (tab === 'favorites') {
        await this._renderFavorites(content);
      } else {
        await this._renderNotes(content);
      }
    } catch (e) {
      console.error('加载失败:', e);
      content.innerHTML = '<p style="color:var(--danger)">加载失败</p>';
    }
  },

  async _renderFavorites(container) {
    const favorites = await API.getFavorites();

    if (!favorites || favorites.length === 0) {
      container.innerHTML = '<p style="color:var(--ink-muted);font-size:0.85rem">暂无收藏</p>';
      return;
    }

    let html = '<div class="favorites-list">';
    favorites.forEach(f => {
      html += `
        <div class="favorite-item">
          <div class="fav-icon">${f.icon || '📖'}</div>
          <div class="fav-info">
            <div class="fav-title">${f.title}</div>
            <div class="fav-stage">${f.stage}</div>
          </div>
          <div class="fav-actions">
            <button class="btn btn-sm btn-g" onclick="Lesson.start('${f.topic_id}')">学习</button>
            <button class="btn btn-sm btn-o" onclick="Favorites.removeFavorite('${f.topic_id}')">取消</button>
          </div>
        </div>
      `;
    });
    html += '</div>';

    container.innerHTML = html;
  },

  async _renderNotes(container) {
    const notes = await API.getNotes();

    if (!notes || notes.length === 0) {
      container.innerHTML = '<p style="color:var(--ink-muted);font-size:0.85rem">暂无笔记</p>';
      return;
    }

    let html = '<div class="notes-list">';
    notes.forEach(n => {
      const date = new Date(n.updated_at).toLocaleDateString('zh-CN');
      html += `
        <div class="note-item">
          <div class="note-header">
            <span class="note-topic">${n.topic_icon || '📖'} ${n.topic_title}</span>
            <span class="note-date">${date}</span>
          </div>
          <div class="note-content">${this._escapeHtml(n.content)}</div>
          <div class="note-actions">
            <button class="btn btn-sm" onclick="Favorites.editNote(${n.id}, '${this._escapeHtml(n.content)}')">编辑</button>
            <button class="btn btn-sm btn-o" onclick="Favorites.deleteNote(${n.id})">删除</button>
          </div>
        </div>
      `;
    });
    html += '</div>';

    container.innerHTML = html;
  },

  async removeFavorite(topicId) {
    try {
      await API.removeFavorite(topicId);
      this.switchTab('favorites');
    } catch (e) {
      alert('取消收藏失败: ' + e.message);
    }
  },

  editNote(noteId, content) {
    const newContent = prompt('编辑笔记:', content);
    if (newContent !== null && newContent.trim()) {
      API.updateNote(noteId, newContent.trim()).then(() => {
        this.switchTab('notes');
      }).catch(e => {
        alert('更新失败: ' + e.message);
      });
    }
  },

  async deleteNote(noteId) {
    if (confirm('确定删除这条笔记？')) {
      try {
        await API.deleteNote(noteId);
        this.switchTab('notes');
      } catch (e) {
        alert('删除失败: ' + e.message);
      }
    }
  },

  async toggleFavorite(topicId) {
    if (!API.token) {
      alert('请先登录');
      return;
    }

    try {
      const result = await API.checkFavorite(topicId);
      if (result.is_favorited) {
        await API.removeFavorite(topicId);
      } else {
        await API.addFavorite(topicId);
      }
      return !result.is_favorited;
    } catch (e) {
      console.error('收藏操作失败:', e);
      return null;
    }
  },

  async addNote(topicId, content, sectionId) {
    if (!API.token) {
      alert('请先登录');
      return;
    }

    try {
      await API.addNote(topicId, content, sectionId);
      return true;
    } catch (e) {
      console.error('添加笔记失败:', e);
      return false;
    }
  },

  _escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
  }
};
