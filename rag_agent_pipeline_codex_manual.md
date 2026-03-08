---
# RAG-Agent-Pipeline 开发手册

> 本手册旨在为 AI 编程助手（如 Codex）提供完整的、可执行的开发指南，使其能够从零完成整个 `RAG-Agent-Pipeline` 项目。

---

## 1. 项目概览

**项目名称**: RAG-Agent-Pipeline

**目标**: 构建一个个人知识管理智能问答系统，用户上传文档后，系统自动提取信息、存储向量，并通过 RAG + Agent 技术提供智能问答。

**技术栈**:
- **后端**: Python 3.10+, FastAPI, LangChain / LlamaIndex, Milvus / Pinecone, OpenAI API
- **前端**: Vite + Vue3 + Pinia + Vue Router + ElementPlus/NaiveUI
- **数据库**: Milvus / Pinecone (向量数据库)
- **辅助库**: PyPDF2, Numpy, Pandas, Requests, Uvicorn

---

## 2. 文件结构

```text
RAG-Agent-Pipeline/
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── api/
│   │   │   ├── upload.py
│   │   │   ├── query.py
│   │   │   └── agent.py
│   │   ├── services/
│   │   │   ├── ingestion/doc_loader.py
│   │   │   ├── embedding/embeddings.py
│   │   │   ├── vectorstore/vector_db.py
│   │   │   ├── agent/rag_agent.py
│   │   │   └── prompts/prompt_engine.py
│   │   ├── models/schemas.py
│   │   │   └── domain.py
│   │   ├── utils/file_utils.py
│   │   ├── utils/text_utils.py
│   │   └── config/settings.py
│   └── requirements.txt
├── frontend/
│   ├── src/main.ts
│   ├── App.vue
│   ├── router/index.ts
│   ├── store/chat.ts
│   ├── store/documents.ts
│   ├── components/chat/ChatWindow.vue
│   ├── components/chat/ChatInput.vue
│   ├── components/upload/DocUpload.vue
│   ├── components/common/Modal.vue
│   └── views/Home.vue
│   └── views/History.vue
│   └── views/DocumentManagement.vue
└── docker/
    ├── Dockerfile-backend
    ├── Dockerfile-frontend
    └── docker-compose.yml
```

---

## 3. 后端开发步骤

### 3.1 环境与依赖

1. 创建虚拟环境并安装依赖：
```bash
python -m venv venv
source venv/bin/activate
pip install fastapi uvicorn pymilvus langchain openai pypdf2 numpy pandas python-dotenv
```

2. 配置 `requirements.txt`:
```
fastapi
uvicorn
pymilvus
langchain
openai
pypdf2
numpy
pandas
python-dotenv
```

3. 创建 `.env` 文件，存储 API Key 与数据库配置。

### 3.2 配置管理 (`config/settings.py`)
```python
from pydantic import BaseSettings

class Settings(BaseSettings):
    OPENAI_API_KEY: str
    MILVUS_HOST: str = 'localhost'
    MILVUS_PORT: str = '19530'
    VECTOR_DIM: int = 1536

    class Config:
        env_file = '.env'

settings = Settings()
```

### 3.3 文档抓取与预处理 (`services/ingestion/doc_loader.py`)
- 支持 PDF、TXT、Markdown
- 拆分 chunk 并清理文本
```python
from PyPDF2 import PdfReader

def load_pdf(path):
    reader = PdfReader(path)
    texts = [page.extract_text() for page in reader.pages]
    return texts

def split_text(texts, chunk_size=500):
    chunks = []
    for text in texts:
        for i in range(0, len(text), chunk_size):
            chunks.append(text[i:i+chunk_size])
    return chunks
```

### 3.4 Embeddings 生成 (`services/embedding/embeddings.py`)
```python
from langchain.embeddings import OpenAIEmbeddings
from config.settings import settings

embeddings_model = OpenAIEmbeddings(model='text-embedding-3-small', openai_api_key=settings.OPENAI_API_KEY)

def embed_chunks(chunks):
    return [embeddings_model.embed_query(c) for c in chunks]
```

### 3.5 向量数据库操作 (`services/vectorstore/vector_db.py`)
```python
from pymilvus import connections, Collection
from config.settings import settings

connections.connect('default', host=settings.MILVUS_HOST, port=settings.MILVUS_PORT)
collection = Collection('documents')

def insert_vectors(vectors, metadatas):
    collection.insert([vectors, metadatas])

def search(query_vector, top_k=5):
    return collection.search(query_vector, 'embedding', limit=top_k)
```

### 3.6 RAG + Agent 核心逻辑 (`services/agent/rag_agent.py`)
```python
from embeddings import embeddings_model
from vector_db import search
from openai import OpenAI

client = OpenAI(api_key=settings.OPENAI_API_KEY)

def answer_query(query):
    vec = embeddings_model.embed_query(query)
    results = search(vec, top_k=5)
    context = ' '.join([r.metadata['text'] for r in results])
    prompt = f"请根据以下文档回答问题：\n{context}\n问题：{query}\n回答："
    response = client.Completion.create(model='gpt-3.5-turbo', prompt=prompt, max_tokens=300)
    return response.choices[0].text
```

### 3.7 Prompt 模板管理 (`services/prompts/prompt_engine.py`)
```python
QA_TEMPLATE = """
你是一个知识问答助手。
根据文档上下文回答问题：
{context}
用户问题：{question}
回答：
"""

def format_prompt(context, question):
    return QA_TEMPLATE.format(context=context, question=question)
```

### 3.8 API 路由拆分
- `api/upload.py`: 上传文档并处理
- `api/query.py`: 用户问答接口
- `api/agent.py`: Agent 流程路由

示例 `upload.py`:
```python
from fastapi import APIRouter, UploadFile
from services.ingestion.doc_loader import load_pdf, split_text
from services.embedding.embeddings import embed_chunks
from services.vectorstore.vector_db import insert_vectors

router = APIRouter()

@router.post('/upload')
async def upload_file(file: UploadFile):
    content = await file.read()
    chunks = split_text([content.decode()])
    vectors = embed_chunks(chunks)
    insert_vectors(vectors, [{'text': c} for c in chunks])
    return {'status': 'success', 'chunks': len(chunks)}
```

### 3.9 启动文件 (`main.py`)
```python
from fastapi import FastAPI
from api import upload, query, agent

app = FastAPI()
app.include_router(upload.router)
app.include_router(query.router)
app.include_router(agent.router)
```

### 3.10 启动后端
```bash
uvicorn app.main:app --reload
```

---

## 4. 前端开发步骤

### 4.1 创建项目
```bash
npm init vite@latest frontend -- --template vue
cd frontend
npm install
```

### 4.2 文件结构
见目录结构图

### 4.3 组件开发
- `DocUpload.vue`: 文件上传
- `ChatWindow.vue` + `ChatInput.vue`: 问答聊天
- Axios 调用后端 API

示例 ChatWindow.vue:
```vue
<template>
  <div>
    <div v-for="msg in messages" :key="msg.id">
      <b>{{ msg.user }}:</b> {{ msg.text }}
    </div>
    <input v-model="query" @keyup.enter="sendQuery" placeholder="请输入问题"/>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'

const query = ref('')
const messages = ref([])

const sendQuery = async () => {
  messages.value.push({id: Date.now(), user:'你', text: query.value})
  const res = await axios.get(`/api/query?q=${query.value}`)
  messages.value.push({id: Date.now(), user:'AI', text: res.data.answer})
  query.value = ''
}
</script>
```

### 4.4 启动前端
```bash
npm run dev
```

---

## 5. Docker 部署

- `Dockerfile-backend`：FastAPI + Python 环境
- `Dockerfile-frontend`：Vite + Vue3
- `docker-compose.yml`：组合后端、前端、Milvus/向量数据库

---

## 6. 开发流程总结
1. 配置 `.env` 文件，启动向量数据库
2. 启动后端，测试上传接口
3. 上传文档并生成向量
4. 测试问答接口（RAG + Agent）
5. 启动前端，调用接口展示问答
6. 可逐步拓展功能：多文档、多用户、Agent自动任务

---

**说明**: 该手册提供完整目录结构、模块划分、核心代码示例及运行流程，Codex 可按照此手册自动生成项目直至完成。

