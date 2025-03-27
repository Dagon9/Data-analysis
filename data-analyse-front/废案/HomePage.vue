<template>
  <div class="dashboard-container">
    <!-- 左侧区域 -->
    <div class="left-panel">
      <div class="hot-list">
        <h3>热点新闻排行榜</h3>
        <ul>
          <li v-for="(item, index) in hotList" :key="item.id">
            <span class="rank">{{ index + 1 }}.</span>
            {{ item.title }}
            <span class="heat">{{ item.heat }}℃</span>
          </li>
        </ul>
      </div>
      <div class="wordcloud-container">
        <div ref="wordcloudChart" class="chart"></div>
      </div>
    </div>

    <!-- 右侧区域 -->
    <div class="right-panel">
      <div class="control-bar">
        <div class="time-picker">
          <label>开始时间：</label>
          <input type="date" v-model="startDate">
          <label>结束时间：</label>
          <input type="date" v-model="endDate">
        </div>
        <select v-model="selectedChartType" class="chart-select">
          <option value="bar">柱状图</option>
          <option value="pie">饼图</option>
        </select>
        <button class="refresh-btn" @click="refreshData">刷新数据</button>
      </div>
      
      <div class="chart-container">
        <div class="chart-header">
          <h3>{{ selectedChartType === 'bar' ? '分类数据统计' : '数据分布比例' }}</h3>
          <div class="chart-legend">
            <span v-for="item in chartLegend" :key="item.name">
              <span class="legend-color" :style="{backgroundColor: item.color}"></span>
              {{ item.name }}
            </span>
          </div>
        </div>
        <div v-show="selectedChartType === 'bar'" ref="barChart" class="chart"></div>
        <div v-show="selectedChartType === 'pie'" ref="pieChart" class="chart"></div>
      </div>
    </div>
  </div>
</template>

<script>
import * as echarts from 'echarts';
import 'echarts-wordcloud';

export default {
  data() {
    return {
      startDate: '2024-01-01',
      endDate: '2024-01-07',
      selectedChartType: 'bar',
      hotList: [
        { id: 1, title: '人工智能新突破', heat: 985 },
        { id: 2, title: '量子计算机进展', heat: 872 },
        // ...更多示例数据...
      ],
      wordcloudData: [
        { name: '科技创新', value: 100 },
        { name: '数字经济', value: 1 },
        { name: '数字经济', value: 50 },
        { name: '数字经济', value: 20 },
        { name: '数字经济', value: 85 },
        { name: '数字经济', value: 85 },
        { name: '数字经济', value: 85 },
        // ...更多示例数据...
      ]
    }
  },
  mounted() {
    this.initWordcloud();
    this.initBarChart();
    this.initPieChart();
  },
  methods: {
    initWordcloud() {
      const chart = echarts.init(this.$refs.wordcloudChart);
      chart.setOption({
        series: [{
          type: 'wordCloud',
          data: this.wordcloudData,
          sizeRange: [20, 60]
        }]
      });
    },
    initBarChart() {
      const chart = echarts.init(this.$refs.barChart);
      chart.setOption({
        xAxis: { data: ['科技', '经济', '体育', '娱乐', '社会'] },
        yAxis: {},
        series: [{ type: 'bar', data: [120, 200, 150, 80, 70] }]
      });
    },
    initPieChart() {
      const chart = echarts.init(this.$refs.pieChart);
      chart.setOption({
        series: [{
          type: 'pie',
          data: [
            { value: 335, name: '科技' },
            { value: 310, name: '经济' },
            // ...更多示例数据...
          ]
        }]
      });
    },
    refreshData() {
      // 这里可以添加数据刷新逻辑
    }
  }
}
</script>

<style scoped>
/* ====================
   全局样式
   ==================== */
:root {
  --primary-color: #4dabf7;
  --text-dark: #2c3e50;
  --text-light: #495057;
  --heat-color: #ff6b6b;
}

/* 过渡动画 */
* {
  transition: background-color 0.3s, box-shadow 0.3s;
}

h3 {
  color: var(--text-light);
  margin-bottom: 1rem;
}

/* ====================
   布局结构
   ==================== */
.dashboard-container {
  display: flex;
  height: 100vh;
  padding: 20px;
  background: #f5f6fa;
}

.left-panel {
  flex: 4;
  margin-right: 20px;
  display: flex;
  flex-direction: column;
}

.right-panel {
  flex: 6;
  display: flex;
  flex-direction: column;
}

/* ====================
   通用组件样式
   ==================== */
/* 阴影效果 */
.hot-list,
.wordcloud-container,
.control-bar,
.chart-container {
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 
              0 2px 4px -1px rgba(0, 0, 0, 0.06);
  background: white;
  border-radius: 8px;
}

/* ====================
   排行榜样式
   ==================== */
.hot-list {
  flex: 7;
  padding: 15px;
  
  ul {
    list-style: none;
    padding: 0;
    margin: 0;
  }

  li {
    padding: 12px 15px;
    margin: 8px 0;
    display: flex;
    align-items: center;
    transition: all 0.3s ease;
    background: rgba(255, 255, 255, 0.9);
    box-shadow: 0 2px 4px rgba(0,0,0,0.05);

    &:hover {
      transform: translateX(5px);
      box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
  }
}

.rank {
  font-weight: 600;
  color: var(--text-dark);
  margin-right: 12px;
  min-width: 30px;
}

.heat {
  margin-left: auto;
  color: var(--heat-color);
  font-weight: 500;
  background: rgba(255,107,107,0.1);
  padding: 2px 8px;
  border-radius: 12px;
}
/********* */

/* ====================
   控制栏样式
   ==================== */
.control-bar {
  display: flex;
  align-items: center;
  gap: 18px;
  padding: 12px 20px;
  background: rgba(255, 255, 255, 0.9);
  border: 1px solid rgba(var(--primary-color), 0.1);
  border-radius: 12px;
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px); /* 兼容Safari */
}

.time-picker {
  display: flex;
  align-items: center;
  gap: 12px;
  position: relative;
  
  &::after {
    content: "⏳";
    position: absolute;
    right: -18px;
    color: var(--primary-color);
    font-size: 1.1em;
  }
}

/* 通用输入控件 */
input[type="date"], .chart-select {
  padding: 8px 15px;
  border: 2px solid #59acff;
  background: rgba(180, 180, 180, 0.3);
  border-radius: 8px;
  font-size: 14px;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  
  &:hover {
    border-color: rgba(var(--primary-color), 0.3);
  }
  &:focus {
    box-shadow: 0 0 0 3px rgba(var(--primary-color), 0.1);
  }
}

.chart-select {
  background-image: url("data:image/svg+xml;utf8,...");
  padding-right: 35px;
}

/* 刷新按钮 */
.refresh-btn {
  --gradient-from: #169aff;
  --gradient-to: var(--primary-color);
  
  background: linear-gradient(135deg, 
    var(--gradient-from) 0%, 
    var(--gradient-to) 100%);
  border-radius: 10px;
  padding: 10px 25px;
  font-weight: 600;
  transition: all 0.3s ease;
  will-change: transform; /* 优化动画性能 */

  &::after {
    content: "↻";
    margin-left: 8px;
    transition: transform 0.3s ease;
  }
  
  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 5px 15px rgba(var(--primary-color), 0.3);
    
    &::after {
      transform: rotate(360deg);
    }
  }
}

/* ====================
   图表区域样式
   ==================== */
.chart-container {
  position: relative;
  padding: 20px;
  margin-top: 20px;

  .chart-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;

    h3 {
      color: var(--text-dark);
      margin: 0;
      font-size: 1.2em;
    }
  }

  .chart-legend {
    display: flex;
    gap: 15px;
    font-size: 0.9em;
  }
}

.legend-color {
  --size: 12px;
  width: var(--size);
  height: var(--size);
  border-radius: 50%;
  margin-right: 6px;
}

.chart {
  height: 450px;
  background: #ffffff;
  border-radius: 8px;
  padding: 15px;
}
</style>