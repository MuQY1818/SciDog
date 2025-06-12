<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';

const conferences = ref([]);
const isLoading = ref(true);
const error = ref(null);

// 定义后端 API 的地址
const API_URL = 'http://localhost:5000/api/conferences';

// 组件挂载后执行的函数
onMounted(async () => {
  try {
    const response = await axios.get(API_URL);
    conferences.value = response.data;
  } catch (err) {
    console.error('获取会议数据失败:', err);
    error.value = '无法加载会议数据，请确保后端服务正在运行。';
  } finally {
    isLoading.value = false;
  }
});
</script>

<template>
  <div id="app-container">
    <header>
      <h1>科研狗 (SciDog)</h1>
      <p>CCF 会议截止日期速查</p>
    </header>

    <main>
      <div v-if="isLoading" class="loading-state">
        <p>正在努力加载会议数据中...</p>
      </div>

      <div v-else-if="error" class="error-state">
        <p>糟糕，出错了：{{ error }}</p>
      </div>

      <div v-else class="data-table-container">
        <table>
          <thead>
            <tr>
              <th>简称 (Abbr.)</th>
              <th>全称 (Full Name)</th>
              <th>截止日期 (Deadline)</th>
              <th>分类 (Rank)</th>
              <th>地点 (Location)</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="conf in conferences" :key="conf.id">
              <td>
                <a :href="conf.link" target="_blank" rel="noopener noreferrer">{{ conf.shortName }} {{ conf.year }}</a>
              </td>
              <td>{{ conf.fullName }}</td>
              <td>{{ conf.deadline }}</td>
              <td>{{ conf.ccfRank }}</td>
              <td>{{ conf.place }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </main>
  </div>
</template>

<style>
/* 全局样式和基础布局 */
#app-container {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

header {
  text-align: center;
  margin-bottom: 40px;
}

header h1 {
  font-size: 2.5rem;
  color: #34495e;
}

/* 加载和错误状态的样式 */
.loading-state, .error-state {
  text-align: center;
  padding: 50px;
  font-size: 1.2rem;
  color: #7f8c8d;
}
.error-state {
  color: #c0392b;
}

/* 表格样式 */
.data-table-container {
  width: 100%;
  overflow-x: auto; /* 在小屏幕上提供滚动条 */
}

table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 20px;
}

th, td {
  padding: 12px 15px;
  border: 1px solid #ddd;
  text-align: left;
}

thead {
  background-color: #42b983;
  color: white;
}

tbody tr:nth-child(even) {
  background-color: #f2f2f2;
}

tbody tr:hover {
  background-color: #ddd;
}

a {
  color: #3498db;
  text-decoration: none;
}

a:hover {
  text-decoration: underline;
}
</style>
