# SciDog - 科研狗

一个聚合全球学术会议 DDL 的平台。

## ✨ 主要功能

- 聚合展示全球学术会议、期刊的 DDL 信息。
- 支持按会议等级 (CCF-A, B, C, Non-CCF) 筛选。
- 支持按技术领域 (AI, DB, NW...) 筛选。
- 支持关键词模糊搜索。
- DDL 截止日期倒计时及进度条，一目了然。
- 响应式卡片设计，在桌面和移动设备上均有良好体验。

## 🚀 一键部署 (Vercel)

本项目已为 Vercel 平台优化，您可以非常轻松地免费部署上线。

1.  **Fork 本仓库**：点击本页面右上角的 "Fork" 按钮，将此项目复制到您自己的 GitHub 账号下。
2.  **登录 Vercel**: 使用您的 GitHub 账号登录 [Vercel](https://vercel.com/)。
3.  **新建项目**: 在 Vercel 的控制面板 (Dashboard) 中，点击 "Add New..." -> "Project"。
4.  **导入仓库**: 从列表中选择您刚刚 Fork 的 `SciDog` 仓库，点击 "Import"。
5.  **部署**: Vercel 会自动识别我们配置好的 `vercel.json` 文件，您无需做任何修改，直接点击 "Deploy" 按钮。

等待1-2分钟，您的 SciDog 网站就成功部署到全球网络，并拥有一个 `.vercel.app` 的公开访问域名了！之后您对项目代码的任何 `git push` 操作，Vercel 都会自动为您重新部署。

## 本地开发

1.  克隆仓库: `git clone <your-repo-url>`
2.  配置后端:
    ```bash
    cd backend
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    pip install -r requirements.txt
    flask run
    ```
3.  配置前端:
    ```bash
    cd frontend
    npm install
    npm run dev
    ```
项目将在 `http://localhost:5173` 运行。

## 项目愿景

我们致力于提供一个集信息聚合、智能推荐、实用工具于一体的平台，让科研工作更高效、更专注。

## 核心功能

- **信息聚合与查询**:
    - [ ] **会议信息**: 自动同步全球主要学术会议的 DDL、举办地、官网链接，并根据 CCF/CORE 等常见评级进行分类。
    - [ ] **期刊信息**: 提供主流期刊的中科院/JCR 分区、影响因子、审稿周期等关键指标查询。
    - [ ] **最新论文**: 实时追踪顶会、顶刊的最新发表论文，并提供个性化订阅服务。

- **智能工具箱**:
    - [ ] DDL 订阅与日历同步功能。
    - [ ] 论文投稿智能推荐。
    - [ ] 科研工具导航（文献管理、在线 LaTex、语法检查等）。

- **个性化服务**:
    - [ ] 用户可以根据自己的研究领域定制个性化主页。
    - [ ] 追踪特定会议/期刊的动态。

## 技术架构

- **前端**: Vue.js / React
- **后端**: Python (Flask/Django)
- **数据库**: PostgreSQL / MongoDB
- **数据采集**: Scrapy / BeautifulSoup / Playwright
- **任务调度**: Celery / APScheduler
- **部署**: Docker

## 路线图 (Roadmap)

- **Phase 1 (MVP)**:
    - [ ] 完成计算机科学领域 CCF 会议信息的自动采集与展示。
    - [ ] 构建基本的前端查询页面，支持按等级和 DDL 排序。
    - [ ] 搭建后端 API 服务。

- **Phase 2**:
    - [ ] 引入期刊分区数据。
    - [ ] 开发用户系统，支持个性化关注。
    - [ ] 实现 DDL 邮件提醒功能。

- **Phase 3**:
    - [ ] 上线"最新论文"模块。
    - [ ] 丰富"工具箱"内容。
    - [ ] 探索基于内容的智能推荐功能。 