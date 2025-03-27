<template>
  <div class="news-ranking">
    <div class="main-container">
      <h3 class="title">热点新闻排行榜</h3>
      
      <!-- 新闻条目列表 -->
      <div 
        v-for="(news, index) in newsList" 
        :key="index"
        class="news-item" 
        @click="showModal(news)">
        <div class="rank-badge">{{ index + 1 }}</div>
        <div class="content">
          <h4 class="news-title">{{ news.title }}</h4>
          <div class="meta">
            <span class="heat">热度值：{{ news.heat }}</span>
            <span class="time">{{ news.time }}</span>
          </div>
        </div>
      </div>
    </div>

    <!-- 模态弹窗 -->
    <div v-if="showModalFlag" class="modal-overlay" @click.self="closeModal">
      <div class="modal-content">
        <span class="modal-close" @click="closeModal">&times;</span>
        <h4 class="modal-title">{{ currentNews.title }}</h4>
        <div class="modal-meta">
          <span class="author">作者：{{ currentNews.author }}</span>
          <span class="source">来源：{{ currentNews.source }}</span>
        </div>
        <div class="modal-body">
          <p class="summary">{{ currentNews.summary }}</p>
          <div class="keywords">
            <span 
              v-for="(keyword, idx) in currentNews.keywords" 
              :key="idx"
              class="keyword-tag">
              {{ keyword }}
            </span>
          </div>
        </div>
        <div class="modal-footer">
          <button class="btn secondary">收藏文章</button>
          <button class="btn primary" @click="readFullArticle(currentNews)">阅读全文</button>
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
      showModalFlag: false,
      currentNews: {},
      newsList: []  // 清空初始数据
    }
  },
  created() {
    this.loadNewsData()
  },
  methods: {
     // 新增数据加载方法
    async loadNewsData() {
      try {
        // 从路由参数获取话题
        const topic = this.$route.query.selectedTopic
        if (topic) {
          const response = await axios.post('http://localhost:5000/api/topic-click', {
            topic: topic,
            timestamp: new Date().toISOString()
          })
          
          // 转换数据格式
          this.newsList = response.data.data.related_news.map(news => ({
            ...news,
            keywords: news.keywords.split(', '),  // 将字符串转为数组
            heat: Math.floor(Math.random() * 10000), // 生成随机热度值
            time: '1小时内更新'  // 添加时间信息
          }))
        }
      } catch (error) {
        console.error('加载新闻数据失败:', error)
        // 保留默认示例数据作为后备
        this.newsList = [{
          title: '数据加载失败，请稍后重试',
          author: '系统',
          source: '数据服务',
          keywords: ['错误'],
          summary: '无法从服务器获取实时数据'
        }]
      }
    },

    showModal(news) {
      this.currentNews = news
      this.showModalFlag = true
    },
    closeModal() {
      this.showModalFlag = false
    },
async readFullArticle(news) {
  try {
    const response = await axios.post('http://localhost:5000/api/generate-article', {
      title: news.title,
      author: news.author,
      source: news.source
    }, {
      timeout: 5000, // 添加超时控制
      headers: {
        'Content-Type': 'application/json' // 明确指定请求头
      }
    })
    
// 修改点1：修正响应数据结构判断
    if (response.data.status !== 'success') {
      throw new Error('后端服务异常: ' + (response.data.message || '未知错误'))
    }

    // 修改点2：添加内容安全处理
    const sanitizedContent = response.data.data.content.replace(/[<>&]/g, '') || '暂无内容'
    
    this.$router.push({
      path: '/news-detail',
      query: { 
        ...news,
        content: sanitizedContent.substring(0, 1000) // 限制内容长度
      }
    })
  } catch (error) {
    // 修改点3：增强错误信息分类处理
    const errorType = error.code === 'ECONNABORTED' ? '请求超时' : 
                    error.response ? '服务端错误' : '网络异常'
    
    console.error(`[${errorType}] 新闻详情请求失败:`, error.message)
    
    this.$router.push({
      path: '/news-detail',
      query: {
        ...news,
        content: `服务暂时不可用（${errorType}），错误码：${error.response?.status || 'N/A'}`
      }
    })
  }
  this.closeModal()
}
  }

}
</script>

<style scoped>
/* 主容器样式 */
.news-ranking {
  padding: 2rem;
  max-width: 1200px;
  margin: 0 auto;
}

.title {
  font-size: 1.5rem;
  color: #2c3e50;
  margin-bottom: 1.5rem;
  padding-bottom: 0.75rem;
  border-bottom: 2px solid #4dabf7;
}

/* 新闻条目样式 */
.news-item {
  display: flex;
  align-items: center;
  padding: 1rem;
  margin-bottom: 1rem;
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  transition: transform 0.2s ease;
  cursor: pointer;
  
  &:hover {
    transform: translateX(8px);
  }
}

.rank-badge {
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #4dabf7;
  color: white;
  border-radius: 8px;
  font-weight: 600;
  margin-right: 1rem;
}

.content {
  flex: 1;
}

.news-title {
  margin: 0;
  font-size: 1.1rem;
  color: #2c3e50;
}

.meta {
  display: flex;
  gap: 1rem;
  margin-top: 0.5rem;
  color: #6c757d;
  font-size: 0.9rem;
}

/* 模态弹窗样式 */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0,0,0,0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 999;
}

.modal-content {
  background: white;
  border-radius: 12px;
  padding: 2rem;
  width: 90%;
  max-width: 600px;
  position: relative;
}

.modal-close {
  position: absolute;
  top: 1rem;
  right: 1rem;
  font-size: 1.5rem;
  cursor: pointer;
  color: #6c757d;
}

.modal-title {
  margin: 0 0 1rem;
  color: #2c3e50;
}

.modal-meta {
  display: flex;
  gap: 1rem;
  margin-bottom: 1rem;
  color: #6c757d;
  font-size: 0.9rem;
}

.keywords {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
  margin-top: 1rem;
}

.keyword-tag {
  background: #e9ecef;
  padding: 0.25rem 0.75rem;
  border-radius: 20px;
  font-size: 0.85rem;
}

.modal-footer {
  margin-top: 1.5rem;
  display: flex;
  gap: 1rem;
  justify-content: flex-end;
}

.btn {
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.2s ease;
  
  &.primary {
    background: #4dabf7;
    color: white;
  }
  
  &.secondary {
    background: #e9ecef;
    color: #2c3e50;
  }
}
</style>