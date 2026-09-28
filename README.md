# News App · 新闻资讯系统

> 一个前后端分离的移动端新闻资讯应用 —— 后端基于 **FastAPI + SQLAlchemy 2.0（全异步）**，前端基于 **Vue 3 + Vite + Vant**。
> 实现注册登录、新闻分类与列表浏览、新闻详情、收藏、浏览历史、多主题切换、中英双语，以及基于大模型的 AI 问答。

<p align="left">
  <img src="https://img.shields.io/badge/Python-3.11+-3776AB?logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/FastAPI-0.141-009688?logo=fastapi&logoColor=white" alt="FastAPI">
  <img src="https://img.shields.io/badge/SQLAlchemy-2.0-D71F00?logo=sqlalchemy&logoColor=white" alt="SQLAlchemy">
  <img src="https://img.shields.io/badge/MySQL-8.0-4479A1?logo=mysql&logoColor=white" alt="MySQL">
  <img src="https://img.shields.io/badge/Redis-7-DC382D?logo=redis&logoColor=white" alt="Redis">
  <img src="https://img.shields.io/badge/Vue-3-4FC08D?logo=vuedotjs&logoColor=white" alt="Vue3">
  <img src="https://img.shields.io/badge/Vite-7-646CFF?logo=vite&logoColor=white" alt="Vite">
</p>

---

## 📖 目录

- [项目简介](#-项目简介)
- [功能特性](#-功能特性)
- [技术栈](#-技术栈)
- [项目结构](#-项目结构)
- [快速开始](#-快速开始)
- [配置说明](#-配置说明)
- [API 接口文档](#-api-接口文档)
- [数据库设计](#-数据库设计)
- [缓存设计](#-缓存设计)
- [认证机制](#-认证机制)
- [开发说明](#-开发说明)
- [待办与后续计划](#-待办与后续计划)
- [License](#-license)

---

## 🧭 项目简介

本项目是一个**前后端分离**的全栈实践项目，后端提供纯 RESTful API，前端为移动端 H5 单页应用。

整体采用经典的分层架构，职责边界清晰：

```
请求 → 路由层(routers) → 数据访问层(crud) → 数据模型层(models)
              ↑                    ↕
         数据校验层(schemas)    缓存层(cache) / Redis
```

这种分层带来的好处是：

- **路由层只关心参数与响应**，不写任何 SQL；
- **CRUD 层只关心数据**，可被多个路由复用（例如新闻详情与收藏列表都用到 `News` 查询）；
- **Schema 层用 Pydantic 统一收口**输入校验与输出序列化，并用 `alias` 解决前后端命名差异（前端驼峰 / 后端下划线）。

---

## ✨ 功能特性

| 模块 | 功能 |
| --- | --- |
| 👤 用户管理 | 注册、登录、获取用户信息、修改资料（昵称 / 头像 / 性别 / 简介 / 手机号）、修改密码 |
| 📰 新闻模块 | 分类列表、新闻列表（分页 + 分页游标）、新闻详情、浏览量自增、相关新闻推荐 |
| ⭐ 收藏模块 | 添加收藏、取消收藏、收藏列表（分页）、清空收藏、收藏状态检查 |
| 🕘 浏览历史 | 添加浏览记录、历史列表（分页）、删除单条、清空历史 |
| ⚡ 缓存加速 | 分类 / 列表 / 详情 / 相关新闻 / 历史记录多级 Redis 缓存 |
| 🤖 AI 问答 | 前端对话式问答，支持 SSE 流式输出与 Markdown 渲染 |
| 🎨 前端体验 | 4 套主题（浅色 / 深色 / 蓝色 / 绿色）、中英双语 i18n、下拉刷新 + 触底加载、Pinia 状态持久化 |

---

## 🛠 技术栈

### 后端

| 分类 | 技术 | 说明 |
| --- | --- | --- |
| Web 框架 | FastAPI 0.141 | 原生支持异步、自动生成 OpenAPI 文档 |
| ASGI 服务器 | Uvicorn | 高性能 ASGI 实现 |
| ORM | SQLAlchemy 2.0 | 使用 `Mapped` / `mapped_column` 新式声明语法 |
| 数据库 | MySQL 8.0 | `utf8mb4` 编码，InnoDB 引擎 |
| 驱动 | aiomysql / PyMySQL | 异步驱动 + 同步驱动 |
| 缓存 | Redis（redis-py asyncio） | 热点数据缓存，缓存失败自动降级 |
| 数据校验 | Pydantic v2 | 请求体校验 & 响应模型序列化 |
| 密码加密 | bcrypt | `$2b$` 哈希，不可逆存储 |
| 认证 | 数据库 Token + 7 天有效期 | `Authorization` 请求头校验 |

### 前端

| 分类 | 技术 |
| --- | --- |
| 框架 | Vue 3（`<script setup>` 组合式 API） |
| 构建工具 | Vite 7 |
| UI 组件库 | Vant 4（移动端） |
| 状态管理 | Pinia + pinia-plugin-persistedstate |
| 路由 | Vue Router 4（路由懒加载） |
| 国际化 | vue-i18n 9（zh-CN / en-US） |
| HTTP | Axios |
| 富文本 | marked + DOMPurify（Markdown 渲染 + XSS 过滤） |

---

## 📂 项目结构

本项目采用**单仓库（monorepo）**结构，前后端各自独立但同处一个 Git 仓库：

```
news-app/                             # 仓库根目录
├── README.md                         # 项目总览（本文件）
├── .gitignore
│
├── backend/                          # ── FastAPI 后端 ──
│   ├── cache/                        # 缓存业务封装
│   │   └── news_cache.py             #   新闻分类 / 列表 / 详情 / 相关新闻的缓存读写
│   ├── config/                       # 配置层
│   │   ├── db_conf.py                #   数据库异步引擎、会话工厂、get_db 依赖
│   │   └── cache_conf.py             #   Redis 客户端与缓存读写工具函数
│   ├── crud/                         # 数据访问层（纯数据库操作，不含业务判断）
│   │   ├── users.py                  #   用户 & Token 相关
│   │   ├── news.py                   #   新闻相关
│   │   ├── news_cache.py             #   带缓存的新闻查询
│   │   ├── favorite.py               #   收藏相关
│   │   └── history.py                #   历史记录相关
│   ├── models/                       # ORM 数据模型（表结构定义）
│   │   ├── users.py                  #   User / UserToken
│   │   ├── news.py                   #   Category / News
│   │   ├── favorite.py               #   Favorite
│   │   └── history.py                #   History
│   ├── routers/                      # API 路由层
│   │   ├── users.py                  #   /api/user/*
│   │   ├── news.py                   #   /api/news/*
│   │   ├── favorite.py               #   /api/favorite/*
│   │   └── history.py                #   /api/history/*
│   ├── schemas/                      # Pydantic 数据校验 / 序列化模型
│   │   ├── users.py                  #   用户请求 & 响应模型
│   │   ├── news.py                   #   新闻响应模型
│   │   ├── favorite.py               #   收藏模型
│   │   ├── history.py                #   历史记录模型
│   │   └── base.py                   #   公共基类
│   ├── utils/                        # 工具层
│   │   ├── auth.py                   #   get_current_user 依赖（Token 鉴权）
│   │   ├── security.py               #   bcrypt 密码加密 / 校验
│   │   ├── response.py               #   统一响应体封装 success_response
│   │   ├── exception.py              #   各类异常处理器实现
│   │   └── exception_handlers.py     #   异常处理器注册入口
│   ├── main.py                       # 应用入口：注册中间件、异常处理器、挂载路由
│   ├── requirements.txt              # 依赖清单
│   └── test_main.http                # HTTP 接口测试文件（IDEA 可直接运行）
│
├── frontend/                         # ── Vue 3 前端 ──
│   ├── src/
│   │   ├── components/               #   公共组件：NewsItem / TabBar
│   │   ├── config/api.js             #   后端地址 & AI 接口配置
│   │   ├── i18n/                     #   多语言资源（zh-CN / en-US）
│   │   ├── router/index.js           #   路由表 + 全局前置守卫
│   │   ├── store/                    #   Pinia 状态：user / news / favorite / history / theme / language
│   │   ├── views/                    #   页面：首页 / 分类 / 详情 / 收藏 / 历史 / 登录 / 注册 / 我的 / 设置 / AI问答
│   │   ├── App.vue
│   │   └── main.js
│   ├── index.html
│   ├── vite.config.js
│   ├── package.json
│   └── README.md                     # 前端专项说明
│
└── docs/                             # ── 项目文档 ──
    ├── API接口规范文档.md             #   接口字段说明与请求 / 响应示例
    ├── 项目后端设计说明文档.md         #   后端设计思路
    └── database.sql                  #   建表脚本 + 示例数据
```

---

## 🚀 快速开始

### 环境要求

| 依赖 | 版本建议 |
| --- | --- |
| Python | 3.11+ |
| MySQL | 8.0+ |
| Redis | 6.0+（可选，未启动时接口会降级为直查数据库） |
| Node.js | 18+ |

### 1. 初始化数据库

在 MySQL 中执行仓库附带的建表脚本（含建库、8 张表与示例数据）：

```bash
mysql -u root -p < docs/database.sql
```

脚本会自动创建数据库 `news_app`（`utf8mb4` / `utf8mb4_unicode_ci`）。

### 2. 启动后端

```bash
cd backend

# 创建并激活虚拟环境
python -m venv .venv
source .venv/Scripts/activate      # Windows(Git Bash)
# source .venv/bin/activate        # macOS / Linux

# 安装依赖
pip install -r requirements.txt

# 启动开发服务器
uvicorn main:app --reload --port 8000
```

启动成功后：

| 地址 | 说明 |
| --- | --- |
| http://127.0.0.1:8000 | 服务根路径 |
| http://127.0.0.1:8000/docs | Swagger UI 交互式接口文档 |
| http://127.0.0.1:8000/redoc | ReDoc 接口文档 |

> 💡 首次启动前请先按下方 [配置说明](#-配置说明) 修改数据库连接信息。

### 3. 启动前端

```bash
cd frontend

npm install
npm run dev          # 开发模式，默认 http://localhost:5173
npm run build        # 生产构建，产物输出到 dist/
npm run preview      # 本地预览构建产物
```

> 前端默认请求 `http://127.0.0.1:8000`，如需修改请编辑 `src/config/api.js` 中的 `apiConfig.baseURL`。

---

## ⚙️ 配置说明

> 以下路径均相对于仓库根目录。

### 1. 数据库连接 `backend/config/db_conf.py`

```python
ASYNC_DATABASE_URL = "mysql+aiomysql://用户名:密码@主机:端口/数据库名?charset=utf8mb4"
```

引擎已配置连接池（`pool_size=10`、`max_overflow=20`）与 `expire_on_commit=False`，`get_db` 依赖统一负责 commit / rollback / close。

### 2. Redis 连接 `backend/config/cache_conf.py`

```python
REDIS_HOST = "localhost"
REDIS_PORT = 6379
REDIS_DB = 0
```

### 3. 前端接口地址 `frontend/src/config/api.js`

```javascript
export const apiConfig = {
  baseURL: 'http://127.0.0.1:8000',
}
```

> ⚠️ **安全提示**：请不要把数据库密码、AI API Key 等敏感信息直接硬编码后提交到公开仓库。
> 推荐改为读取环境变量，例如后端使用 `os.getenv("DB_URL")`，前端使用 `.env` + `import.meta.env.VITE_API_KEY`。

---

## 📡 API 接口文档

- **基础地址**：`http://127.0.0.1:8000`
- **统一响应格式**：

```json
{
  "code": 200,
  "message": "success",
  "data": {}
}
```

### 用户模块 `/api/user`

| 接口 | 方法 | 鉴权 | 说明 |
| --- | --- | --- | --- |
| `/api/user/register` | POST | ❌ | 用户注册（成功后直接返回 Token，自动登录） |
| `/api/user/login` | POST | ❌ | 用户登录 |
| `/api/user/info` | GET | ✅ | 获取当前用户信息 |
| `/api/user/update` | PUT | ✅ | 更新用户资料（昵称 / 头像 / 性别 / 简介 / 手机号） |
| `/api/user/password` | PUT | ✅ | 修改密码（新密码最少 6 位） |

### 新闻模块 `/api/news`

| 接口 | 方法 | 鉴权 | 参数 | 说明 |
| --- | --- | --- | --- | --- |
| `/api/news/categories` | GET | ❌ | `skip`、`limit` | 获取新闻分类列表（带缓存） |
| `/api/news/list` | GET | ❌ | `categoryId`、`page`、`pageSize` | 新闻列表，返回 `list` / `total` / `hasMore` |
| `/api/news/detail` | GET | ❌ | `id` | 新闻详情，同时浏览量 +1 并返回 `relatedNews` |

### 收藏模块 `/api/favorite`

| 接口 | 方法 | 鉴权 | 参数 | 说明 |
| --- | --- | --- | --- | --- |
| `/api/favorite/check` | GET | ✅ | `newsId` | 检查是否已收藏 |
| `/api/favorite/add` | POST | ✅ | body: `newsId` | 添加收藏 |
| `/api/favorite/remove` | DELETE | ✅ | `newsId` | 取消收藏 |
| `/api/favorite/list` | GET | ✅ | `page`、`pageSize` | 收藏列表，按收藏时间倒序 |
| `/api/favorite/clear` | DELETE | ✅ | — | 清空当前用户全部收藏 |

### 浏览历史 `/api/history`

| 接口 | 方法 | 鉴权 | 参数 | 说明 |
| --- | --- | --- | --- | --- |
| `/api/history/add` | POST | ✅ | body: `newsId` | 添加浏览记录 |
| `/api/history/list` | GET | ✅ | `page`、`pageSize` | 历史列表，按浏览时间倒序 |
| `/api/history/delete/{history_id}` | DELETE | ✅ | 路径参数 | 删除单条历史记录 |
| `/api/history/clear` | DELETE | ✅ | — | 清空浏览历史 |

> 📄 更详细的字段说明与请求 / 响应示例，见 [`docs/API接口规范文档.md`](docs/API接口规范文档.md)。
> 🗄 建表脚本与示例数据见 [`docs/database.sql`](docs/database.sql)。

---

## 🗄 数据库设计

数据库名 `news_app`，共 8 张表：

| 表名 | 说明 | 关键约束 / 索引 |
| --- | --- | --- |
| `user` | 用户信息表 | `username_UNIQUE`、`phone_UNIQUE` |
| `user_token` | 用户令牌表 | `token_UNIQUE`，外键 `user_id` → `user.id`（级联删除） |
| `news_category` | 新闻分类表 | `name_UNIQUE`，`sort_order` 控制排序 |
| `news` | 新闻表 | 外键 `category_id`；索引 `fk_news_category_idx`、`idx_publish_time` |
| `related_news` | 新闻关联表 | 用于详情页「相关新闻」推荐位 |
| `favorite` | 收藏表 | 唯一约束 `(user_id, news_id)` 保证同一新闻不重复收藏 |
| `history` | 浏览历史表 | 索引 `fk_history_user_idx`、`fk_history_news_idx`、`idx_view_time` |
| `ai_chat` | AI 聊天记录表 | 外键 `user_id` → `user.id`（级联删除）；索引 `idx_created_at` |

**ER 关系（简化）**

```
user 1 ──── n user_token
user 1 ──── n favorite   n ──── 1 news n ──── 1 news_category
user 1 ──── n history    n ──── 1 news
user 1 ──── n ai_chat
news 1 ──── n related_news
```

> 建表脚本自带 8 个新闻分类（头条 / 社会 / 国内 / 国际 / 娱乐 / 体育 / 科技 / 财经）与若干条示例新闻，仅用于本地功能演示。
> 若将项目公开发布，建议把示例数据替换为自造的中性内容，避免使用真实媒体稿件。

---

## ⚡ 缓存设计

系统以 Redis 作为缓存层，遵循一个原则：**数据越稳定，缓存越持久**。

| 缓存内容 | Key 规则 | 过期时间 |
| --- | --- | --- |
| 新闻分类 | `news:categories` | 2 小时 |
| 新闻列表 | `news_list:{categoryId\|all}:{page}:{size}` | 30 分钟 |
| 新闻详情 | `news:detail:{newsId}` | 5 分钟 |
| 相关新闻 | `news:related:{newsId}:{categoryId}` | 30 分钟 |
| 用户历史 | `history:list:{userId}` | 1 小时 |

设计要点：

- **缓存降级**：所有缓存读写都包在 `try / except` 中，Redis 不可用时打印日志并返回 `None`，自动回落到直接查库，**不会因为缓存故障导致接口 500**；
- **防雪崩**：不同数据类型的过期时间刻意错开（120s ~ 7200s），避免同一时刻大面积失效；
- **失效策略**：数据变更时删除相关 Key，采用「缓存失效」而非「主动更新」，降低写放大与不一致风险；
- **中文友好**：`json.dumps(..., ensure_ascii=False)` 保证缓存中中文可读。

---

## 🔐 认证机制

采用「数据库 Token」方案，不使用 JWT：

1. 用户注册 / 登录成功后，服务端用 `uuid4` 生成 Token，写入 `user_token` 表，有效期 **7 天**；
2. 同一用户重复登录会**复用同一条记录**并刷新 Token 与过期时间（不产生冗余数据）；
3. 需要鉴权的接口，请求头携带 Token：

```http
Authorization: <token>
```

4. 后端通过 `Depends(get_current_user)` 依赖统一校验，在 `user_token` 表中比对 Token 与 `expires_at`，失效则返回 `401`。

> 相比 JWT，数据库 Token 的优点是**可以服务端主动失效**（删表即下线），缺点是每次请求多一次数据库查询。

---

## 🧑‍💻 开发说明

**统一异常处理**（`utils/exception.py`）在 `main.py` 中一次性注册四类处理器，保证任何异常都返回统一的 JSON 结构：

| 异常类型 | HTTP 状态码 | 返回 message |
| --- | --- | --- |
| `HTTPException` | 按抛出时指定 | 业务自定义（如「该用户已存在」） |
| `IntegrityError` | 400 | 用户名已存在 / 关联数据不存在 / 数据约束冲突 |
| `SQLAlchemyError` | 500 | 数据库操作失败，请稍后重试 |
| `Exception` | 500 | 服务器内部错误 |

`DEBUG_MODE = True` 时会额外返回 `error_type`、`error_detail`、`traceback`、`path`，方便定位问题。**上线前请将其改为 `False`**，避免堆栈信息泄露。

**其他约定**

- 全部数据库操作使用异步 `AsyncSession`，会话生命周期由 `get_db` 依赖统一管理；
- 密码使用 bcrypt 加密存储，数据库中只保存 `$2b$` 哈希；
- 接口参数命名通过 Pydantic `alias` 适配前端驼峰（如 `pageSize` ↔ `page_size`）；
- `main.py` 中已配置 CORS 中间件，开发阶段 `allow_origins=["*"]`，生产环境需收敛为具体域名。

---

## 📌 待办与后续计划

- [ ] 敏感配置迁移到环境变量 / `.env`，移除代码中的硬编码密钥
- [ ] AI 问答能力从「前端直连大模型」改为「后端代理转发」，避免 API Key 暴露在浏览器
- [ ] 引入 Alembic 管理数据库迁移
- [ ] 补充 Pytest 单元测试与接口测试
- [ ] 新闻搜索、评论、点赞功能
- [ ] 使用 Docker Compose 一键拉起 MySQL + Redis + 后端服务

---

## 📄 License

本项目仅用于个人学习与技术实践，请勿用于商业用途。新闻数据版权归原作者所有。

---

<p align="center"><i>如果这个项目对你有帮助，欢迎点个 ⭐ Star 支持一下～</i></p>
