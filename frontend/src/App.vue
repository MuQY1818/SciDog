<template>
  <el-container class="main-container">
    <el-header class="main-header">
      <h1>
        <el-icon>
          <School />
        </el-icon>
        SciDog - 科研狗
      </h1>
      <p>一个聚合全球学术会议 DDL 的平台</p>
    </el-header>

    <el-main>
      <!-- Filter Controls -->
      <el-card class="filter-card">
        <div class="filter-controls">
          <el-input v-model="searchQuery" placeholder="搜索会议名称或描述..." clearable class="search-input">
            <template #prepend>
              <el-icon>
                <Search />
              </el-icon>
            </template>
          </el-input>

          <el-checkbox-group v-model="selectedRanks" class="rank-filter">
            <el-checkbox-button label="A">CCF-A</el-checkbox-button>
            <el-checkbox-button label="B">CCF-B</el-checkbox-button>
            <el-checkbox-button label="C">CCF-C</el-checkbox-button>
            <el-checkbox-button label="N">Non-CCF</el-checkbox-button>
          </el-checkbox-group>
        </div>

        <el-divider />

        <div class="type-filters">
          <el-checkbox v-model="showAllTypes" @change="handleShowAllTypes" class="all-types-checkbox">全部分类</el-checkbox>
          <el-checkbox-group v-model="selectedTypes">
            <el-checkbox v-for="(name, key) in types" :key="key" :label="key">{{ name }}</el-checkbox>
          </el-checkbox-group>
        </div>
      </el-card>

      <!-- Conference List -->
      <div v-if="paginatedConfs.length > 0">
        <el-row :gutter="20">
          <el-col v-for="conf in paginatedConfs" :key="conf.id" :xs="24" :sm="12" :md="8">
            <el-card class="conf-card" shadow="hover">
              <template #header>
                <div class="card-header">
                  <a :href="conf.link" target="_blank">{{ conf.title }} {{ conf.year }}</a>
                  <el-tag :type="getRankType(conf.ccfRank)">{{ conf.ccfRank === 'N' ? 'Non-CCF' : 'CCF-' + conf.ccfRank
                    }}</el-tag>
                </div>
              </template>
              <div class="conf-body">
                <p class="conf-description">{{ conf.description }}</p>
                <el-tag size="small" type="info" class="type-tag">{{ conf.subname }}</el-tag>
                <el-divider />
                <div class="deadline-info">
                  <div class="countdown-container"
                    v-if="conf.deadline.toUpperCase() !== 'TBD' && isUpcoming(conf.deadline)">
                    <div class="countdown-wrapper">
                      <el-icon color="#E6A23C">
                        <AlarmClock />
                      </el-icon>
                      <span class="countdown-text">
                        <vue-countdown :time="getTimeRemaining(conf.deadline, conf.timezone)"
                          v-slot="{ days, hours, minutes, seconds }">
                          还剩 {{ days }} 天 {{ hours }} 时 {{ minutes }} 分 {{ seconds }} 秒
                        </vue-countdown>
                      </span>
                      <div class="deadline-date">({{ formatDeadline(conf.deadline, conf.timezone) }})</div>
                    </div>
                    <div class="progress-wrapper"
                      v-if="getDeadlineProgress(conf.deadline, conf.timezone).percentage > 0">
                      <el-progress :percentage="getDeadlineProgress(conf.deadline, conf.timezone).percentage"
                        :status="getDeadlineProgress(conf.deadline, conf.timezone).status" :text-inside="true"
                        :stroke-width="14" />
                    </div>
                  </div>
                  <div class="countdown-wrapper" v-else-if="conf.deadline.toUpperCase() !== 'TBD'">
                    <el-icon color="#F56C6C">
                      <CircleCloseFilled />
                    </el-icon>
                    <span class="deadline-text">已截止</span>
                    <div class="deadline-date">({{ formatDeadline(conf.deadline, conf.timezone) }})</div>
                  </div>
                  <div class="countdown-wrapper" v-else>
                    <el-icon color="#909399">
                      <QuestionFilled />
                    </el-icon>
                    <span class="deadline-text">TBD</span>
                  </div>
                </div>
              </div>
            </el-card>
          </el-col>
        </el-row>
      </div>
      <el-empty v-else description="没有找到符合条件的会议"></el-empty>

      <!-- Pagination -->
      <el-pagination v-if="filteredConfs.length > 0" background layout="prev, pager, next" :page-size="pageSize"
        :total="filteredConfs.length" @current-change="handlePageChange" v-model:current-page="currentPage"
        class="main-pagination" />
    </el-main>
  </el-container>
</template>

<script>
import { defineComponent, ref, computed, onMounted, watch } from "vue";
import axios from "axios";
import moment from "moment-timezone";
import VueCountdown from "@chenfengyuan/vue-countdown";

export default defineComponent({
  name: "App",
  components: {
    VueCountdown,
  },
  setup() {
    // --- Reactive State ---
    const allConfs = ref([]);
    const types = ref({});
    const searchQuery = ref("");
    const selectedRanks = ref(["A", "B", "C", "N"]);
    const selectedTypes = ref([]);
    const showAllTypes = ref(true);
    const pageSize = ref(12);
    const currentPage = ref(1);

    // --- Computed Properties ---
    const filteredConfs = computed(() => {
      let confs = allConfs.value;

      if (searchQuery.value) {
        const lowerCaseQuery = searchQuery.value.toLowerCase();
        confs = confs.filter(
          (conf) =>
            conf.title.toLowerCase().includes(lowerCaseQuery) ||
            conf.description.toLowerCase().includes(lowerCaseQuery)
        );
      }

      // Filter by rank. If no ranks are selected, the list will be correctly empty.
      confs = confs.filter((conf) => selectedRanks.value.includes(conf.ccfRank));

      // Filter by type. If "All Types" is unchecked, filter by the selected types array.
      // If selectedTypes is empty, this correctly results in an empty conference list.
      if (!showAllTypes.value) {
        confs = confs.filter(conf => selectedTypes.value.includes(conf.type))
      }

      return confs;
    });

    const paginatedConfs = computed(() => {
      const start = (currentPage.value - 1) * pageSize.value;
      const end = start + pageSize.value;
      return filteredConfs.value.slice(start, end);
    });

    // --- Methods ---
    const fetchData = async () => {
      try {
        // 在生产环境 (例如 Zeabur) 会使用注入的环境变量，本地开发时则使用相对路径
        const baseURL = import.meta.env.VITE_API_BASE_URL || "";
        const res = await axios.get(`${baseURL}/api/conferences`);
        allConfs.value = res.data.conferences;
        types.value = res.data.type_mapping;
        selectedTypes.value = Object.keys(res.data.type_mapping);
      } catch (error) {
        console.error("Failed to fetch conferences:", error);
      }
    };

    const handlePageChange = (page) => {
      currentPage.value = page;
    };

    const handleShowAllTypes = (value) => {
      if (value) {
        selectedTypes.value = Object.keys(types.value);
      } else {
        selectedTypes.value = [];
      }
    };

    const getRankType = (rank) => {
      const types = { 'A': 'danger', 'B': 'warning', 'C': 'success' };
      return types[rank] || 'info';
    }

    const getDeadlineMoment = (deadline, timezone) => {
      let tz = timezone ? timezone.trim() : 'UTC';
      if (tz.toUpperCase() === 'AOE') {
        tz = 'Etc/GMT+12';
      }
      if (!moment.tz.names().includes(tz)) {
        tz = 'UTC';
      }
      return moment.tz(deadline, 'YYYY-MM-DD HH:mm:ss', tz);
    };

    const getTimeRemaining = (deadline, timezone) => {
      if (!deadline || deadline.toUpperCase() === 'TBD') return 0;
      const deadlineMoment = getDeadlineMoment(deadline, timezone);
      const now = moment();
      return Math.max(0, deadlineMoment.diff(now));
    };

    const isUpcoming = (deadline) => {
      return getTimeRemaining(deadline, 'UTC') > 0;
    };

    const formatDeadline = (deadline, timezone) => {
      if (!deadline || deadline.toUpperCase() === 'TBD') return 'TBD';
      const deadlineMoment = getDeadlineMoment(deadline, timezone);
      return deadlineMoment.tz(moment.tz.guess()).format('YYYY-MM-DD HH:mm');
    }

    const getDeadlineProgress = (deadline, timezone) => {
      const timeRemaining = getTimeRemaining(deadline, timezone);
      if (timeRemaining <= 0) {
        return { percentage: 0, status: '' };
      }

      const thirtyDaysInMs = 30 * 24 * 60 * 60 * 1000;
      if (timeRemaining > thirtyDaysInMs) {
        return { percentage: 0, status: '' };
      }

      const percentage = Math.floor(100 - (timeRemaining / thirtyDaysInMs) * 100);

      let status = 'success';
      if (percentage >= 90) {
        status = 'exception';
      } else if (percentage >= 60) {
        status = 'warning';
      }

      return { percentage, status };
    };

    // --- Watchers ---
    watch(selectedTypes, (newVal) => {
      if (newVal.length === Object.keys(types.value).length) {
        showAllTypes.value = true;
      } else {
        showAllTypes.value = false;
      }
    });

    // --- Lifecycle Hooks ---
    onMounted(() => {
      fetchData();
    });

    return {
      searchQuery,
      selectedRanks,
      selectedTypes,
      showAllTypes,
      types,
      filteredConfs,
      paginatedConfs,
      pageSize,
      currentPage,
      handlePageChange,
      handleShowAllTypes,
      getRankType,
      getTimeRemaining,
      isUpcoming,
      formatDeadline,
      getDeadlineProgress
    };
  },
});
</script>

<style>
/* Global Styles */
body {
  background-color: #f4f6f9;
  font-family: 'Helvetica Neue', Helvetica, 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', Arial, sans-serif;
  margin: 0;
}

/* Main Layout */
.main-container {
  max-width: 1280px;
  margin: 0 auto;
  padding: 20px;
}

.main-header {
  text-align: center;
  margin-bottom: 20px;
  height: auto;
  padding: 20px 0;
}

.main-header h1 {
  font-size: 2.5em;
  color: #303133;
  display: inline-flex;
  align-items: center;
  gap: 10px;
}

.main-header p {
  color: #909399;
  font-size: 1.1em;
}

/* Filters */
.filter-card {
  margin-bottom: 20px;
}

.filter-controls {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 20px;
  flex-wrap: wrap;
}

.search-input {
  max-width: 400px;
  min-width: 250px;
  flex-grow: 1;
}

.type-filters {
  display: flex;
  flex-wrap: wrap;
  gap: 15px;
  align-items: center;
}

.all-types-checkbox {
  border-right: 1px solid #dcdfe6;
  padding-right: 15px;
}


/* Conference Card */
.conf-card {
  margin-bottom: 20px;
  height: calc(100% - 20px);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-weight: bold;
}

.card-header a {
  color: #409eff;
  text-decoration: none;
}

.card-header a:hover {
  text-decoration: underline;
}

.conf-body .conf-description {
  color: #606266;
  font-size: 0.9em;
  min-height: 50px;
}

.conf-body .type-tag {
  margin-bottom: 10px;
}

.countdown-wrapper {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 0.95em;
  flex-wrap: wrap;
}

.progress-wrapper {
  margin-top: 8px;
}

.deadline-info .el-icon {
  font-size: 1.2em;
}

.countdown-text,
.deadline-text {
  font-weight: 500;
}

.deadline-date {
  color: #909399;
  font-size: 0.85em;
  margin-left: auto;
}

/* Pagination */
.main-pagination {
  justify-content: center;
  margin-top: 20px;
}
</style>