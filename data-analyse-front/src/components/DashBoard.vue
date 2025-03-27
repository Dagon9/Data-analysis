<template>
  <div class="dashboard-container">
    <!-- 导航栏 -->
    <nav class="bg-white shadow-sm" style="height: 10vh; z-index: 1000">
      <div class="h-100 container-fluid d-flex align-items-center">
        <h4 class="mb-0 me-4 text-primary">数据看板</h4>
        <div class="d-flex align-items-center w-100">
          <div class="input-group" style="max-width: 600px">
            <span class="input-group-text bg-transparent border-end-0">
              <i class="bi bi-search text-secondary"></i>
            </span>
            <input
              type="search"
              class="form-control rounded-pill border-start-0"
              placeholder="输入关键词搜索..."
              style="height: 40px; padding-left: 0"
              v-model="searchKeyword"
            >
          </div>
          <div class="ms-auto d-flex gap-3">
            <button class="btn btn-link text-dark">
              <i class="bi bi-gear"></i>
            </button>
            <button class="btn btn-link text-dark">
              <i class="bi bi-person-circle"></i>
            </button>
          </div>
        </div>
      </div>
    </nav>

    <!-- 主内容区 -->
    <div class="dashboard">
      <!-- 左侧面板 -->
      <div class="left-panel">
        <div class="ranking-box">
          <h5>热点话题排行榜</h5>
            <div class="list-group">
              <a
                  v-for="(item, index) in rankingList"
                  :key="index"
                  href="#"
                  class="list-group-item list-group-item-action d-flex justify-content-between align-items-center" 
                  @click.prevent="navigateToNews(item)">
                  <div class="d-flex align-items-center flex-fill me-3">  <!-- 添加flex-fill -->
                      <span class="fw-bold">{{ index + 1 }}.</span> 
                      <span class="ms-2">{{ item.topic || item }}</span>  <!-- 添加左侧间距 -->
                  </div>
                  <span class="badge bg-primary rounded-pill ms-auto">  <!-- 添加ms-auto -->
                      {{ (item.heat || 0).toLocaleString() }}
                  </span>
              </a>
            </div>
        </div>
        <div class="wordcloud-box">
          <h5>关键词云图</h5>
          <canvas ref="wordcloudCanvas" style="width: 100%; height: 300px;"></canvas>
        </div>
      </div>

      <!-- 右侧面板 -->
      <div class="right-panel">
        <div class="controls bg-white p-3 rounded shadow-sm">
          <div class="d-flex gap-3">
            <input
              type="date"
              class="form-control"
              style="width: 200px"
              v-model="startDate"
            >
            <input
              type="date"
              class="form-control"
              style="width: 200px"
              v-model="endDate"
            >
              <!-- 新增主题选择框 -->
            <select
              class="form-select"
              style="width: 200px"
              v-model="selectedChartTheme"
            >
              <option>新闻类别</option>
              <option>热点趋势</option>
              <option>新闻来源</option>
            </select>
            <select
              class="form-select"
              style="width: 200px"
              v-model="selectedChartType"
            >
              <option>柱状图</option>
              <option>饼图</option>
              <option>折线图</option>
            </select>

            <button class="btn btn-primary" @click="updateChart">更新图表</button>
          </div>
        </div>
        <div class="chart-box">
          <canvas ref="chartCanvas"></canvas>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { onMounted, ref } from 'vue'
import Chart from 'chart.js/auto'
import WordCloud from 'wordcloud'
import { useRouter } from 'vue-router'  
import axios from 'axios'


export default {
  setup() {
    const router = useRouter()
    // 响应式数据
    const searchKeyword = ref('')
    const startDate = ref('2024-01-01')
    const endDate = ref('2024-01-07')
    const selectedChartType = ref('柱状图')
    const selectedChartTheme = ref('新闻类别')
    const rankingList = ref([]) 

    // DOM 引用
    const chartCanvas = ref(null)
    const wordcloudCanvas = ref(null)

    // 数据获取方法
    const fetchHotTopics = async () => {
      try {
        const response = await axios.get('http://localhost:5000/api/hot-topics')
        // 修改映射方式保留完整数据
        rankingList.value = response.data.data.hot_topics.map(item => ({
          ...item,
          //topic: `${index + 1}. ${item.topic}` // 保留原话题数据
        }))
      } catch (error) {
        console.error('获取热点话题失败:', error)
        rankingList.value = [{ topic: '数据加载失败，请稍后重试', heat: 0 }]
      }
    }
    const fetchKeywords = async () => {
      try {
        const response = await axios.get('http://localhost:5000/api/keywords')
        return response.data.data.keywords
      } catch (error) {
        console.error('获取关键词失败:', error)
        return [
          { keyword: '示例1', count: 12 },
          { keyword: '示例2', count: 8 }
        ]
      }
    }

    // 图表初始化
    let chartInstance = null
    const initChart = () => {
  if (chartInstance) chartInstance.destroy()


  
  // 根据主题生成不同数据
  const themeData = {
    '新闻类别': {
      labels: ['政治', '经济', '科技', '娱乐'],
      data: [25, 30, 15, 30]
    },
    '热点趋势': {
      labels: ['周一', '周二', '周三', '周四'],
      data: [65, 59, 80, 81]
    },
    '新闻来源': {
      labels: ['门户网站', '社交媒体', '官方渠道', '自媒体'],
      data: [40, 35, 15, 10]
    }
  }[selectedChartTheme.value]

  const ctx = chartCanvas.value.getContext('2d')
  // 修改图表类型判断逻辑
  const chartType = {
    '柱状图': 'bar',
    '折线图': 'line',
    '饼图': 'pie'
  }[selectedChartType.value]

  chartInstance = new Chart(ctx, {
    type: chartType,
    data: {
      labels: themeData.labels,
      datasets: [{
        label: '数据量',
        data: themeData.data,
        backgroundColor: chartType === 'line' ? 
          'rgba(54, 162, 235, 0.8)' :  // 折线图使用单一颜色
          [
            'rgba(255, 99, 132, 0.8)',
            'rgba(54, 162, 235, 0.8)',
            'rgba(255, 206, 86, 0.8)',
            'rgba(75, 192, 192, 0.8)'
          ]
      }]
    },
    // 添加折线图专用配置
    options: chartType === 'line' ? {
      elements: {
        line: {
          tension: 0.4  // 使折线更平滑
        }
      }
    } : {}
  })
}


    // 词云初始化
    const initWordCloud = async () => {
      try {
        const keywords = await fetchKeywords()
        if (!wordcloudCanvas.value) return
        
        // 清空画布
        const ctx = wordcloudCanvas.value.getContext('2d')
        ctx.clearRect(0, 0, wordcloudCanvas.value.width, wordcloudCanvas.value.height)

        // 添加尺寸适配
        wordcloudCanvas.value.width = wordcloudCanvas.value.offsetWidth
        wordcloudCanvas.value.height = wordcloudCanvas.value.offsetHeight

        WordCloud(wordcloudCanvas.value, {
          list: keywords.map(k => [k.keyword, k.count]),
          backgroundColor: '#ffffff',
          minSize: 14,          // 增加最小字号
          weightFactor: size => Math.sqrt(size) * 5, // 调整缩放系数
          color: 'random-dark',
          rotateRatio: 0.3,
          gridSize: 12,         // 添加网格尺寸
          drawOutOfBound: false,
          shrinkToFit: true     // 确保适应容器
        })
      } catch (error) {
        console.error('词云初始化失败:', error)
      }
    }

    // 生命周期钩子
    onMounted(async () => {
      await fetchHotTopics()
      if (chartCanvas.value) {  // 添加保护
        await initChart()
      }
      await initWordCloud()
    })

    // 方法
    const updateChart = () => {
      initChart()
    }
const navigateToNews = async (topic) => {
  try {
    const response = await axios.post('http://localhost:5000/api/topic-click', {
      topic: topic.topic || topic,  // 兼容两种数据结构
      timestamp: new Date().toISOString(),
      heat: topic.heat || 0
    })
    
    console.log('话题点击数据已发送:', response.data)
    
    router.push({
      path: '/news-ranking',
      query: { 
        selectedTopic: topic.topic || topic,
        heat: topic.heat || 0
      }
    })
    
  } catch (error) {
    console.error('发送点击数据失败:', error)
    // 失败时仍进行跳转
    router.push({
      path: '/news-ranking',
      query: { selectedTopic: '未知话题' }
    })
  }
}
    return {
      searchKeyword,
      startDate,
      endDate,
      selectedChartType,
      rankingList,
      chartCanvas,
      wordcloudCanvas,
      selectedChartTheme,
      updateChart,
      navigateToNews
    }

  }

}
</script>

<style scoped>
/* 布局容器 */
.dashboard-container {
  background: #f0f2f5;
  min-height: 100vh;
  padding: 20px;
}

.dashboard {
  display: flex;
  gap: 20px;
  height: 90vh;
}

/* 左右面板公共样式 */
.left-panel, .right-panel {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.left-panel { flex: 4; }
.right-panel { flex: 6; }

/* 组件盒子样式 */
.ranking-box,
.wordcloud-box,
.chart-box {
  background: white;
  border-radius: 8px;
  padding: 15px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.ranking-box {
  flex: 5;
  overflow-y: auto;
}

.chart-box {
  flex: 1;
}

/* 词云盒子 */
.wordcloud-box {
  flex: 5;
  position: relative;
  overflow: hidden;
  
  canvas {
    width: 100% !important;
    height: 100% !important;
    transition: transform 0.3s;
    
    &:hover {
      transform: scale(1.02);
    }
  }
}

/* 导航栏 */
nav {
  padding: 0 2rem;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

/* 响应式设计 */
@media (max-width: 768px) {
  nav { padding: 0 1rem; }
  h4.text-primary { display: none; }
}

/* 表单聚焦样式 */
.form-control:focus {
  box-shadow: none;
  border-color: #86b7fe;
}
</style>


