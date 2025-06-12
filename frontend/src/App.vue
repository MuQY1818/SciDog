<script setup>
import { ref, onMounted, computed } from 'vue';
import axios from 'axios';

// --- 响应式状态定义 ---
const conferences = ref([]);
const isLoading = ref(true);
const error = ref(null);

// 筛选相关的状态
const selectedTypes = ref([]); // 选中的领域
const selectedRank = ref('All'); // 选中的CCF等级
const searchQuery = ref('');   // 搜索关键词

// 从后端获取的所有会议类型
const allTypes = ref([]);

const API_URL = 'http://localhost:5000/api/conferences';

// --- 数据获取与处理 ---
onMounted(async () => {
  try {
    const response = await axios.get(API_URL);
    conferences.value = response.data;
    // 从数据中提取出所有的会议类型，并去重
    const types = new Set(response.data.map(c => c.type));
    allTypes.value = Array.from(types);
    selectedTypes.value = allTypes.value; // 默认全选
  } catch (err) {
    console.error('获取会议数据失败:', err);
    error.value = '无法加载会议数据，请确保后端服务正在运行。';
  } finally {
    isLoading.value = false;
  }
});

// --- 计算属性，用于动态过滤会议列表 ---
const filteredConferences = computed(() => {
  return conferences.value.filter(conf => {
    // 按 CCF 等级过滤
    const rankMatch = selectedRank.value === 'All' || conf.ccfRank === selectedRank.value;
    // 按领域类型过滤
    const typeMatch = selectedTypes.value.includes(conf.type);
    // 按搜索词过滤 (忽略大小写)
    const searchMatch = conf.shortName.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
                        (conf.fullName && conf.fullName.toLowerCase().includes(searchQuery.value.toLowerCase()));

    return rankMatch && typeMatch && searchMatch;
  });
});

const rankButtons = ['All', 'A', 'B', 'C'];
</script>

<template>
  <el-container id="app-container">
    <el-header class="app-header">
      <h1>科研狗 (SciDog)</h1>
      <p>会议截止日期速查</p>
    </el-header>

    <el-main>
      <!-- 筛选器区域 -->
      <el-card class="filter-card">
        <div class="filter-section">
          <el-checkbox-group v-model="selectedTypes">
            <el-checkbox v-for="type in allTypes" :key="type" :label="type" border>{{ type }}</el-checkbox>
          </el-checkbox-group>
        </div>
        <el-divider />
        <div class="filter-controls">
            <el-input
              v-model="searchQuery"
              placeholder="搜索会议简称或全称"
              clearable
              class="search-input"
            />
            <el-button-group>
              <el-button
                v-for="rank in rankButtons"
                :key="rank"
                :type="selectedRank === rank ? 'primary' : 'default'"
                @click="selectedRank = rank"
              >
                CCF {{ rank }}
              </el-button>
            </el-button-group>
        </div>
      </el-card>

      <!-- 会议列表区域 -->
      <div v-if="isLoading" class="loading-state">
        <p>正在努力加载会议数据中...</p>
      </div>
      <div v-else-if="error" class="error-state">
        <p>糟糕，出错了：{{ error }}</p>
      </div>
      <div v-else>
        <p class="result-count">共找到 {{ filteredConferences.length }} 个会议</p>
        <el-row :gutter="20">
          <el-col :span="24" v-for="conf in filteredConferences" :key="conf.id" class="conference-col">
            <el-card shadow="hover" class="conference-card">
              <div class="card-header">
                <a :href="conf.link" target="_blank" rel="noopener noreferrer" class="conference-title">
                  {{ conf.shortName }} {{ conf.year }}
                </a>
              </div>
              <div class="card-body">
                <p class="conference-fullname">{{ conf.fullName }}</p>
                <p class="conference-deadline"><b>Deadline:</b> {{ conf.deadline }} ({{ conf.timezone }})</p>
                <p class="conference-location"><b>Location:</b> {{ conf.place }}</p>
              </div>
              <div class="card-footer">
                <el-tag size="small">{{ conf.type }}</el-tag>
                <el-tag type="success" size="small">CCF {{ conf.ccfRank }}</el-tag>
              </div>
            </el-card>
          </el-col>
        </el-row>
      </div>
    </el-main>
  </el-container>
</template>

<style>
/* 基础和布局 */
body {
  background-color: #f4f6f9;
}
#app-container {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  max-width: 1200px;
  margin: 0 auto;
}
.app-header {
  text-align: center;
  padding: 20px 0;
}
.app-header h1 {
  font-size: 2.5rem;
  color: #2c3e50;
}

/* 筛选卡片 */
.filter-card {
  margin-bottom: 20px;
}
.filter-section .el-checkbox-group {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}
.filter-controls {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.search-input {
  max-width: 300px;
}

/* 结果计数 */
.result-count {
  color: #606266;
  margin-bottom: 20px;
}

/* 会议卡片 */
.conference-col {
  margin-bottom: 20px;
}
.conference-card .card-header {
  font-size: 1.25rem;
  font-weight: bold;
  margin-bottom: 10px;
}
.conference-title {
  color: #303133;
  text-decoration: none;
}
.conference-title:hover {
  color: #409eff;
}
.conference-card .card-body p {
  margin: 5px 0;
  color: #606266;
  font-size: 0.9rem;
}
.conference-card .card-footer {
  margin-top: 15px;
  padding-top: 10px;
  border-top: 1px solid #e4e7ed;
  display: flex;
  gap: 10px;
}

/* 加载和错误状态 */
.loading-state, .error-state {
  text-align: center;
  padding: 50px;
  font-size: 1.2rem;
  color: #7f8c8d;
}
.error-state {
  color: #c0392b;
}
</style>
