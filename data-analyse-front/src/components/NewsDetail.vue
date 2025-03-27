<template>
  <div class="dashboard">
    <!-- 左侧新闻内容 -->
    <div class="article-panel">
      <h2 class="mb-3">{{ article.title }}</h2>
      <div class="article-meta">
        <div class="d-flex gap-4 text-muted">
          <span>作者：{{ article.author }}</span>
          <span>发布时间：{{ article.publishTime }}</span>
          <span>来源：{{ article.source }}</span>
        </div>
      </div>
      <article class="article-content">
        <p v-for="(para, index) in article.content" :key="index">{{ para }}</p>
      </article>
    </div>

    <!-- 右侧对话窗口 -->
    <div class="chat-panel">
      <div class="chat-messages" ref="chatWindow">
        <div 
          v-for="(msg, index) in messages"
          :key="index"
          :class="['message', msg.type]">
          {{ msg.text }}
        </div>
      </div>
      <div class="p-3 border-top">
        <div class="input-group">
          <input
            type="text"
            class="form-control"
            placeholder="输入您的问题..."
            v-model="inputMessage"
            @keypress.enter="sendMessage">
          <button class="btn btn-primary" @click="sendMessage">发送</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  data() {
    return {
      article: {
        title: '',
        author: '未知作者',
        source: '未知来源',
        publishTime: new Date().toLocaleDateString(),
        content: []
      },
      messages: [],
      inputMessage: ''
    }
  },
  created() {
    this.parseArticleContent()
  },
methods: {
  parseArticleContent() {
    const query = this.$route.query || {}
    this.article = {
      title: query.title || '无标题',
      author: query.author || '未知作者',
      source: query.source || '未知来源',
      publishTime: query.publishTime || new Date().toLocaleString(),
      content: this.parseContent(query.content)
    }
    console.log('解析后的内容:', this.article.content) // 调试用
  },
  async sendMessage() {
    if (!this.inputMessage.trim()) return
    
    // 添加加载状态
    const userMessage = { 
      text: this.inputMessage,
      type: 'user'
    }
    const botMessage = {
      text: '思考中...',
      type: 'bot',
      loading: true
    }
    
    this.messages = [...this.messages, userMessage, botMessage]
    this.inputMessage = ''
    
     try {
      const response = await axios.post('http://localhost:5000/api/chat', {
        message: userMessage.text,
        context: this.article.content.join('\n')
      })
      
      // 修改点：调整数据结构访问方式
      const answer = response.data.data?.answer || '暂时无法获取回答'
      
      this.messages.splice(-1, 1, {
        text: answer,
        type: 'bot'
      })
      
      // 添加滚动到底部逻辑
      this.$nextTick(() => {
        const container = this.$refs.chatWindow
        container.scrollTop = container.scrollHeight
      })
      
    } catch (error) {
      this.messages.splice(-1, 1, {
        text: `请求失败：${error.message}`,
        type: 'error'
      })
    }
  },

  // 修改原有解析方法处理纯文本
  parseContent(raw = '') {
    try {
      // 按换行符分割段落，过滤空行
      return raw.split('\n')
        .map(line => line.trim())
        .filter(line => line.length > 0)
    } catch (e) {
      return ['内容解析错误']
    }
  }

}
}
</script>

<style scoped>
/* 保持原有样式 */
body {
  background: #f0f2f5;
  min-height: 100vh;
  padding: 20px;
}

.dashboard {
  display: flex;
  gap: 20px;
  height: 95vh;
}

.article-panel {
  flex: 7;
  background: white;
  border-radius: 8px;
  padding: 25px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  overflow-y: auto;
}

.chat-panel {
  flex: 3;
  display: flex;
  flex-direction: column;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.article-meta {
  border-bottom: 1px solid #eee;
  padding-bottom: 15px;
  margin-bottom: 20px;
}

.chat-messages {
  flex: 1;
  padding: 15px;
  overflow-y: auto;
  background: #f8f9fa;
}

.message.user {
  background: #e3f2fd;
  border-radius: 15px;
  padding: 10px 15px;
  margin-bottom: 10px;
  max-width: 80%;
  margin-left: auto;
}

.message.bot {
  background: white;
  border-radius: 15px;
  padding: 10px 15px;
  margin-bottom: 10px;
  max-width: 80%;
  box-shadow: 0 1px 3px rgba(0,0,0,0.1);
}
.article-content {
  line-height: 1.8;
  p {
    margin: 1em 0;
    text-indent: 2em;
  }
}
.message {
  &::after {
    content: '';
    display: inline-block;
    animation: typing 1s steps(3) infinite;
  }
  
  &.error {
    background: #ffe3e3;
    color: #c00;
  }
}

@keyframes typing {
  0% { opacity: 0.3 }
  50% { opacity: 1 }
  100% { opacity: 0.3 }
}
</style>
