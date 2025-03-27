import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

// 引入图表库
import Chart from 'chart.js/auto'
import WordCloud from 'wordcloud'

const app = createApp(App)
app.use(router)
app.config.globalProperties.$Chart = Chart
app.config.globalProperties.$WordCloud = WordCloud

app.mount('#app')
