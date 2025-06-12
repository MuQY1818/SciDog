# SciDog - 科研狗

一个聚合全球学术会议 DDL (Deadline) 的平台，旨在帮助科研人员轻松追踪重要学术会议的截稿日期。

![SciDog Screenshot](https://raw.githubusercontent.com/CannedShrimp/SciDog/main/screenshot.png)

## ✨ 主要功能

- **会议聚合**: 集中展示计算机科学领域的全球学术会议信息。
- **DDL 倒计时**: 直观地展示每个会议的截稿日期倒计时和提交通道开放进度。
- **分类筛选**:
  - 按 **CCF 等级** (A, B, C, Non-CCF) 筛选会议。
  - 按**研究领域** (如 AI, CV, NLP, DB 等) 筛选会议。
- **关键词搜索**: 快速搜索特定会议的名称或简称。
- **响应式设计**: 在桌面和移动设备上均有良好的浏览体验。

## 🛠️ 技术栈

- **前端**:
  - [Vue.js 3](https://vuejs.org/) (使用 Composition API)
  - [Vite](https://vitejs.dev/)
  - [Element Plus](https://element-plus.org/)
  - [axios](https://axios-http.com/)
- **后端**:
  - [Python](https://www.python.org/)
  - [Flask](https://flask.palletsprojects.com/)
  - [PyYAML](https://pyyaml.org/)

## 本地开发指南

请遵循以下步骤在您的本地环境中运行本项目。

### 1. 环境准备

- 安装 [Node.js](https://nodejs.org/en/) (版本 >= 16.x)
- 安装 [Python](https://www.python.org/downloads/) (版本 >= 3.8.x)
- 一个包管理器，如 `npm` 或 `yarn`。

### 2. 克隆项目

```bash
git clone https://github.com/CannedShrimp/SciDog.git
cd SciDog
```

### 3. 后端设置

后端服务为前端提供会议数据 API。

```bash
# 1. 进入后端目录
cd backend

# 2. (推荐) 创建并激活 Python 虚拟环境
# Windows
python -m venv venv
.\\venv\\Scripts\\activate
# macOS / Linux
python3 -m venv venv
source venv/bin/activate

# 3. 安装依赖
pip install -r requirements.txt

# 4. 运行后端服务
python scidog_backend.py
```

运行成功后，后端服务将在 `http://127.0.0.1:5000` 上监听。请保持此终端窗口的运行状态。

### 4. 前端设置

前端是用户交互的主界面。

```bash
# 1. 打开一个新的终端，进入前端目录
cd frontend

# 2. 安装依赖
npm install

# 3. 运行前端开发服务器
npm run dev
```

运行成功后，Vite 会启动一个开发服务器，通常在 `http://localhost:5173`。

### 5. 访问项目

在浏览器中打开前端开发服务器的地址 (例如 `http://localhost:5173`)，您应该能看到 SciDog 的主界面，并且所有会议数据都已成功加载。

## 📝 许可证

本项目采用 [MIT](https://opensource.org/licenses/MIT) 许可证。 