## RAG-Agent-Pipeline

一个面向「个人知识管理」场景的智能问答系统。  
用户可以上传本地文档，系统自动完成文本解析、切分与向量化存储，在问答阶段通过 RAG（Retrieval-Augmented Generation）+ Agent 流程，从向量数据库中检索相关片段，并调用大模型生成上下文感知的答案。

---

### 项目简介

- **项目名称**：RAG-Agent-Pipeline  
- **核心目标**：  
  - 管理个人或团队的文档知识库（PDF/TXT/Markdown 等）；  
  - 利用 RAG 技术，将检索到的文档上下文与大模型结合，给出有依据的回答；  
  - 通过多步 Agent，将复杂目标拆解成多个子任务，结合 RAG 逐步完成并给出总结。

---

### 技术栈总览

- **后端**
  - **框架**：FastAPI
  - **语言 & 运行环境**：Python 3.10+
  - **向量数据库**：Milvus（推荐使用 Docker standalone 模式）
  - **Embedding & LLM**
    - 本地：Ollama（默认示例模型：`qwen2.5-coder:7b`，用于 Embedding 和 LLM）
    - 云端（可选）：OpenAI（保留兼容接口）
  - **关键依赖**：
    - `fastapi`, `uvicorn`
    - `pymilvus`
    - `ollama`, `openai`
    - `pydantic-settings`, `python-dotenv`
    - `PyPDF2`, `numpy`, `pandas`

- **前端**
  - **构建工具**：Vite
  - **框架**：Vue 3（`<script setup>`），TypeScript
  - **状态管理**：Pinia
  - **路由**：Vue Router
  - **HTTP 客户端**：Axios

---

### 目录结构（简要）

```text
RAG-Agent-Pipeline/
├── backend/
│   ├── app/
│   │   ├── main.py                 # FastAPI 入口
│   │   ├── api/
│   │   │   ├── upload.py           # 上传文档并入库
│   │   │   ├── query.py            # 单轮问答（RAG）
│   │   │   ├── agent.py            # 多步 Agent 流程
│   │   │   ├── health.py           # 健康检查
│   │   │   └── config.py           # LLM 运行时配置（前端可切换）
│   │   ├── services/
│   │   │   ├── ingestion/
│   │   │   │   └── doc_loader.py   # PDF 文档加载与切分
│   │   │   ├── embedding/
│   │   │   │   └── embeddings.py   # 使用 Ollama 生成 Embedding
│   │   │   ├── vectorstore/
│   │   │   │   └── vector_db.py    # Milvus 连接与检索封装
│   │   │   ├── agent/
│   │   │   │   └── rag_agent.py    # RAG + 多步 Agent 核心逻辑
│   │   │   └── prompts/
│   │   │       └── prompt_engine.py# Prompt 模板管理
│   │   ├── models/
│   │   │   ├── domain.py           # 领域模型（文档分片等）
│   │   │   └── schemas.py          # Pydantic 接口模型（请求/响应）
│   │   ├── utils/
│   │   │   ├── file_utils.py       # 文件保存目录等工具
│   │   │   └── text_utils.py       # 文本归一化/截断等
│   │   └── config/
│   │       ├── settings.py         # 静态配置（.env）
│   │       └── runtime.py          # 运行时 LLM provider 切换
│   └── requirements.txt            # 后端依赖
│
├── frontend/
│   ├── index.html
│   ├── vite.config.ts              # Vite 配置（含 /api 代理到后端）
│   ├── package.json
│   └── src/
│       ├── main.ts                 # Vue 入口，挂载 Pinia & Router
│       ├── App.vue                 # 全局布局与导航
│       ├── api/
│       │   └── client.ts           # Axios 封装：/query、/upload、/agent、/config/llm
│       ├── router/
│       │   └── index.ts            # 路由：Home / Documents / History
│       ├── store/
│       │   ├── chat.ts             # 聊天消息状态
│       │   └── documents.ts        # 文档上传记录状态
│       ├── components/
│       │   ├── chat/
│       │   │   ├── ChatWindow.vue  # 消息列表展示
│       │   │   └── ChatInput.vue   # 输入问题并发起 /query
│       │   ├── upload/
│       │   │   └── DocUpload.vue   # 文档上传并调用 /upload
│       │   └── common/
│       │       └── Modal.vue       # 通用模态框组件
│       └── views/
│           ├── Home.vue            # 首页：简介 + LLM 切换 + 聊天
│           ├── DocumentManagement.vue # 文档管理与列表
│           └── History.vue         # 历史记录占位
│
├── rag_agent_pipeline_codex_manual.md  # 面向 AI 助手的开发手册（设计文档）
├── LICENSE                             # Apache-2.0 许可证
└── .gitignore
```

---

### 项目启动流程

#### 1. 准备环境

- **必要条件**
  - 已安装 Python 3.10+
  - 已安装 Node.js + npm
  - 已安装 Docker，并可正常运行容器
  - 已安装并能运行 Ollama（且已拉取所需模型，例如 `qwen2.5-coder:7b`）

#### 2. 启动 Milvus（向量数据库）

以最简 Docker standalone 方式为例：

```powershell
docker run -d --name milvus-standalone `
  -p 19530:19530 `
  -p 9091:9091 `
  milvusdb/milvus:cpu-latest
```

确认容器正常运行：

```powershell
docker ps
docker logs -f milvus-standalone
```

> **注意**：需要在 Milvus 中创建名为 `documents` 的集合，向量维度必须与 Ollama embedding 返回的维度一致。  
> 可以编写一个 `init_milvus.py` 脚本使用 `pymilvus` 创建包含 `id`、`embedding`、`text` 字段的集合并建立索引。

#### 3. 配置后端环境变量（`.env`）

在 `backend` 目录下创建 `.env` 文件，例如：

```env
# LLM 相关（可选，默认使用 Ollama）
LLM_PROVIDER=ollama               # openai / ollama
OPENAI_API_KEY=你的OpenAIKey或留空
OPENAI_MODEL=gpt-3.5-turbo
OLLAMA_MODEL=qwen2.5-coder:7b     # 本地 OLLAMA 模型名称

# Milvus 配置
MILVUS_HOST=localhost
MILVUS_PORT=19530

# 向量维度（需和实际 embedding 维度一致）
VECTOR_DIM=你的实际维度
```

> 如需确认 Ollama embedding 维度，可在 Python REPL 中运行：
> ```python
> import ollama
> resp = ollama.embeddings(model="qwen2.5-coder:7b", prompt="hello")
> len(resp["embedding"])
> ```

#### 4. 安装并启动后端

```bash
cd backend
pip install -r requirements.txt

uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

校验后端是否正常：

- 访问 `http://127.0.0.1:8000/health` → 应返回 `{"status": "ok"}`  
- 访问 `http://127.0.0.1:8000/docs` → 可查看自动生成的接口文档

#### 5. 安装并启动前端

```bash
cd frontend
npm install
npm run dev
```

前端开发服默认运行在 `http://localhost:5173`（以终端输出为准）。  
前端通过 Vite 代理，将 `/api` 前缀的调用转发到 `http://127.0.0.1:8000`：

```ts
// vite.config.ts
server: {
  proxy: {
    '/api': {
      target: 'http://localhost:8000',
      changeOrigin: true,
      rewrite: (path) => path.replace(/^\/api/, ''),
    },
  },
},
```

---

### 核心功能说明

- **文档上传与向量入库**
  - 前端 `DocUpload.vue` 选择本地文件，通过 `/api/upload` 上传到后端；
  - 后端：
    - 将文档读入内存，按固定长度切分为片段；
    - 使用 Ollama embedding 模型将每个片段转成向量；
    - 将向量与对应的文本元数据写入 Milvus 的 `documents` 集合。

- **RAG 问答（/query）**
  - 前端 `ChatInput.vue` 在首页输入问题，通过 `/api/query?q=...` 调用后端；
  - 后端 `rag_agent.answer_query`：
    1. 使用 Ollama embedding 将用户问题编码为向量；
    2. 调用 Milvus 搜索最相近的文档片段；
    3. 聚合检索到的文本片段，拼成上下文；
    4. 使用 Prompt 模板构造提示词；
    5. 通过统一的 LLM 客户端（OpenAI 或 Ollama）生成答案并返回。

- **多步 Agent（/agent）**
  - 接口：`POST /api/agent`，请求体包含目标 `goal`、历史对话 `history`、最大步数 `max_steps`；
  - 后端流程：
    1. 先让 LLM 对最终目标做「子任务规划」；
    2. 对每个子任务调用上面的 RAG 问答，记录中间「思考（thought）、行动（action）、观察结果（observation）」；
    3. 最后汇总所有子任务结果，再由 LLM 做一次总结，返回最终答案；
  - 响应包含：
    - 多个 `steps`（每一步的 thought/action/observation）；
    - 一个 `final_answer`（面向用户的总结答案）。

- **LLM 提供方切换（OpenAI / Ollama）**
  - 运行时状态由后端 `runtime.py` 维护；
  - 通过 `/config/llm` 接口：
    - `GET`：获取当前 provider 和默认模型名称；
    - `POST`：设置 provider（`openai` / `ollama`）。
  - 前端首页 `Home.vue` 提供一个下拉选择框，可在 UI 上直接切换使用的 LLM 提供方，而无需修改 `.env`。

- **前端界面**
  - 首页：
    - 项目简介；
    - 当前 LLM 提供方切换；
    - 聊天窗口（消息展示 + 输入框）。
  - 文档管理：
    - 上传文档；
    - 查看上传历史（文件名 / 切分片数 / 状态）。
  - 历史记录：目前为占位页，可扩展为展示历史会话或任务记录。

---

### 使用教程（端到端）

1. **启动基础服务**
   - 启动 Milvus 容器；
   - 确认 Ollama 运行正常，并拉取所需模型；
   - 在 Milvus 中创建 `documents` 集合（字段：`id`、`embedding`、`text`）。

2. **配置并启动后端**
   - 在 `backend/.env` 中配置 Milvus 主机与端口、Ollama 模型名称和向量维度；
   - `pip install -r backend/requirements.txt`；
   - 启动 FastAPI：`uvicorn app.main:app --reload`。

3. **启动前端**
   - 在 `frontend` 中执行 `npm install && npm run dev`；
   - 打开前端地址（例如 `http://localhost:5173`）。

4. **在网页中体验**
   - 在首页：
     - 选择 LLM 提供方（推荐先试 `Ollama（本地）`）；
     - 在聊天框输入一个问题（如果尚未上传文档，可以先问一些通用问题，主要测试 LLM 通路是否正常）。
   - 在「文档管理」页：
     - 上传一份 PDF 或文本文件；
     - 确认界面显示「上传成功，切分为 N 个片段」；
   - 回到首页再次提问与文档相关的问题，观察回答是否引用到文档中的信息。

---

### 许可证

本项目使用 **Apache License 2.0** 开源协议，详细条款见仓库中的 `LICENSE` 文件。