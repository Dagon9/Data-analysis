<template>
  <div class="data-container">
    <h2>新闻数据统计</h2>
    <table v-if="statsData" class="data-table">
      <thead>
        <tr>
          <th>统计维度</th>
          <th>详细数据</th>
        </tr>
      </thead>
      <tbody>
        <!-- 总新闻数 -->
        <tr>
          <td>总新闻数量</td>
          <td>{{ statsData.total }}</td>
        </tr>

            <!-- 修改后的按日期统计 -->
    <tr>
      <td>最近7天新闻分布</td>
      <td>
        <div class="date-tags">
          <span v-for="[date, count] in Object.entries(statsData.by_date || {})" 
                :key="date" 
                class="date-tag">
            {{ date.slice(5) }}日: {{ count }}篇
          </span>
        </div>
      </td>
    </tr>

    <!-- 修改后的按分类统计 -->
    <tr>
      <td>分类分布</td>
      <td>
        <div class="category-bars">
          <div v-for="[category, count] in Object.entries(statsData.by_category || {})" 
               :key="category" 
               class="category-item">
            <div class="category-info">
              <span class="category-name">{{ category }}</span>
              <span class="category-count">{{ count }}篇</span>
            </div>
            <div class="progress-bar" :style="{ width: (count / statsData.total * 100) + '%' }"></div>
          </div>
        </div>
      </td>
    </tr>
      </tbody>
    </table>
    <div v-else class="loading">加载数据中...</div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      statsData: {  // 初始化默认结构
        total: 0,
        by_date: {},
        by_category: {}
      }
    }
  },
  mounted() {
    axios.get('http://localhost:5000/api/stats')
      .then(response => {

          // 添加数据合并逻辑
          this.statsData = {
            total: 0,
            by_date: {},
            by_category: {},
            ...response.data.data
        };
      })
  }
}
</script>

<style scoped>
.data-container {
  padding: 20px;
  max-width: 600px;
  margin: 0 auto;
}

.data-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 20px;
}

.data-table th, .data-table td {
  border: 1px solid #ddd;
  padding: 12px;
  text-align: left;
}

.data-table th {
  background-color: #f5f5f5;
}

.loading {
  text-align: center;
  padding: 20px;
  color: #666;
}
.sub-data {
  padding-left: 20px;
  margin: 5px 0;
  list-style-type: none;
}

.sub-data li {
  padding: 4px 0;
  background-color: #f8f9fa;
  margin: 2px 0;
}


/* 新增样式 */
.date-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.date-tag {
  background: #e8f4ff;
  border-radius: 4px;
  padding: 4px 8px;
  font-size: 0.9em;
}

.category-bars {
  width: 100%;
}

.category-item {
  margin: 8px 0;
}

.category-info {
  display: flex;
  justify-content: space-between;
  margin-bottom: 4px;
  font-size: 0.9em;
}

.progress-bar {
  height: 8px;
  background: #409eff;
  border-radius: 4px;
  transition: width 0.3s ease;
}
</style>
