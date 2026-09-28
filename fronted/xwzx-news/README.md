# frontend · 新闻资讯移动端

> 新闻资讯 App 的移动端前端 —— 基于 **Vue 3 + Vite 7 + Vant 4** 构建的单页应用。
> 本目录是单仓库 `news-app` 的 `frontend/` 部分，配套后端在同级目录 [`../backend`](../backend)（FastAPI + MySQL + Redis）。

<p align="left">
  <img src="https://img.shields.io/badge/Vue-3-4FC08D?logo=vuedotjs&logoColor=white" alt="Vue3">
  <img src="https://img.shields.io/badge/Vite-7-646CFF?logo=vite&logoColor=white" alt="Vite">
  <img src="https://img.shields.io/badge/Vant-4-11bbff?logo=vant&logoColor=white" alt="Vant">
  <img src="https://img.shields.io/badge/Pinia-3-ffd859?logo=pinia&logoColor=black" alt="Pinia">
</p>

---

## ✨ 功能一览

| 页面 | 路由 | 说明 |
| --- | --- | --- |
| 首页 | `/home` | 分类 Tab 切换、下拉刷新、触底加载更多新闻 |
| 新闻详情 | `/news/detail/:id` | 正文展示、浏览量统计、相关新闻推荐、收藏 / 浏览记录写入 |
| 分类 | `/category` | 全部分类入口 |
| 收藏 | `/favorite` | 收藏列表、取消收藏、清空收藏 |
| 浏览历史 | `/history` | 历史列表（按时间倒序）、删除单条、清空 |
| AI 问答 | `/aichat` | 对话式问答，SSE 流式输出 + Markdown 渲染 |
| 登录 / 注册 | `/login` `/register` | 表单校验、Token 持久化、自动登录 |
| 我的 | `/my` | 个人中心入口聚合 |
| 个人信息 | `/profile` | 昵称 / 头像 / 性别 / 简介 / 手机号编辑 |
| 设置 | `/settings` | 主题切换、语言切换、修改密码、退出登录 |

**体验细节**

- 🎨 **4 套主题**：浅色 / 深色 / 蓝色 / 绿色，基于 CSS 变量动态切换并持久化到 `localStorage`
- 🌏 **中英双语**：vue-i18n 实现，语言选择持久化
- 💾 **状态持久化**：Pinia + `pinia-plugin-persistedstate`，登录态刷新不丢失
- ⚡ **路由懒加载**：所有页面按需加载，首屏更轻
- 🛡 **XSS 防护**：AI 返回的 Markdown 经 `marked` 解析后再用 `DOMPurify` 过滤

---

## 🛠 技术栈

| 分类 | 选型 | 版本 |
| --- | --- | --- |
| 框架 | Vue 3（`<script setup>` 组合式 API） | ^3.x |
| 构建工具 | Vite | ^7.1.6 |
| UI 组件库 | Vant | ^4.9.21 |
| 状态管理 | Pinia + pinia-plugin-persistedstate | ^3.0.3 / ^4.5.0 |
| 路由 | Vue Router（history 模式） | ^4.5.1 |
| 国际化 | vue-i18n | ^9.8.0 |
| HTTP 客户端 | Axios | ^1.12.2 |
| Markdown | marked + DOMPurify | ^16.3.0 / ^3.2.7 |

---

## 📂 目录结构

```
frontend/
├── public/                     # 静态资源
├── src/
│   ├── components/
│   │   ├── NewsItem.vue        # 新闻列表项（标题 / 封面 / 作者 / 时间 / 浏览量）
│   │   └── TabBar.vue          # 底部导航栏
│   ├── config/
│   │   └── api.js              # 后端 API 地址 & AI 接口配置
│   ├── i18n/
│   │   ├── index.js            # i18n 实例初始化
│   │   └── locales/            # zh-CN.js / en-US.js 语言包
│   ├── router/
│   │   └── index.js            # 路由表 + 全局前置守卫（设置页面标题）
│   ├── store/
│   │   ├── index.js            # Pinia 实例
│   │   ├── user.js             # 登录 / 注册 / 用户信息 / 修改密码
│   │   ├── theme.js            # 主题切换
│   │   ├── language.js         # 语言切换
│   │   └── modules/
│   │       ├── news.js         # 分类 / 列表 / 详情 + 分页状态
│   │       ├── favorite.js     # 收藏
│   │       └── history.js      # 浏览历史
│   ├── views/                  # 页面组件（见上方「功能一览」）
│   ├── App.vue
│   ├── main.js                 # 应用入口：挂载 Pinia / Router / i18n
│   └── style.css               # 全局样式与 CSS 变量
├── index.html
├── vite.config.js
└── package.json
```

---

## 🚀 快速开始

### 环境要求

- Node.js 18+
- 后端服务已启动（默认 `http://127.0.0.1:8000`）

### 安装与运行

```bash
cd frontend

# 安装依赖
npm install

# 启动开发服务器（默认 http://localhost:5173）
npm run dev

# 生产构建，产物输出到 dist/
npm run build

# 本地预览构建产物
npm run preview
```

### 后端地址配置

编辑 `src/config/api.js`：

```javascript
export const apiConfig = {
  baseURL: 'http://127.0.0.1:8000',   // 改成你的后端地址
}
```

---

## 🤖 关于 AI 问答

该功能直接调用兼容 OpenAI 协议的大模型接口（当前配置为阿里云百炼 DashScope 的 `qwen-plus`），并以 SSE 方式流式返回，前端逐字渲染。

```javascript
export const aiChatConfig = {
  apiEndpoint: 'https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions',
  apiKey: import.meta.env.VITE_AI_API_KEY,   // ✅ 推荐：从环境变量读取
  model: 'qwen-plus'
}
```

> ⚠️ **重要安全提示**
> 不要把 API Key 硬编码在 `api.js` 里并提交到公开仓库 —— 前端代码是**完全可见**的，Key 一旦泄漏会被人盗刷额度。
> 建议做法（按推荐程度排序）：
> 1. **由后端代理**：前端请求自己的后端，后端再去调用大模型，Key 只存在于服务器环境变量中（最安全）；
> 2. 若必须前端直连，至少改为读取 `.env` 中的 `VITE_AI_API_KEY`，并把 `.env` 加入 `.gitignore`，仓库里只提交 `.env.example`。
>
> 另外，密钥一旦被提交进 Git 历史，即使后续删除文件，**历史提交里依然可被检索到**，需要重新生成 Key。

---

## 📝 备注

- `node_modules/`、`dist/`、`.idea/` 等目录请勿提交，已在 `.gitignore` 中排除；
- 项目使用 Vue Router 的 **history 模式**，部署到静态服务器时需配置 fallback 到 `index.html`（Nginx 示例：`try_files $uri $uri/ /index.html;`）。

---

## 📄 License

本项目仅用于个人学习与技术实践，请勿用于商业用途。
