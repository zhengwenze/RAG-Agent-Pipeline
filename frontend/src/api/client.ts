import axios from 'axios'

// 使用 Vite 代理，将 /api 前缀转发到后端 FastAPI
export const apiClient = axios.create({
  baseURL: '/api',
})

export interface QueryResponse {
  answer: string
}

export interface AgentStep {
  step: number
  thought: string
  action: string
  observation?: string
}

export interface AgentRequest {
  goal: string
  history?: { role: 'user' | 'assistant' | 'system'; content: string }[]
  max_steps?: number
}

export interface AgentResponse {
  goal: string
  steps: AgentStep[]
  final_answer: string
}

export interface UploadResponse {
  status: string
  chunks: number
}

export type LLMProvider = 'openai' | 'ollama'

export interface LLMConfig {
  provider: LLMProvider
  openai_model: string
  ollama_model: string
}

export async function queryApi(q: string): Promise<QueryResponse> {
  const res = await apiClient.get<QueryResponse>('/query', {
    params: { q },
  })
  return res.data
}

export async function runAgentApi(payload: AgentRequest): Promise<AgentResponse> {
  const res = await apiClient.post<AgentResponse>('/agent', payload)
  return res.data
}

export async function uploadDocumentsApi(files: FileList): Promise<UploadResponse> {
  const formData = new FormData()
  // 简化：只上传第一个文件，可按需扩展为多文件
  const first = files.item(0)
  if (!first) {
    throw new Error('请选择至少一个文件')
  }
  formData.append('file', first)

  const res = await apiClient.post<UploadResponse>('/upload', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  })
  return res.data
}

export async function getLLMConfig(): Promise<LLMConfig> {
  const res = await apiClient.get<LLMConfig>('/config/llm')
  return res.data
}

export async function setLLMProvider(provider: LLMProvider): Promise<LLMConfig> {
  const res = await apiClient.post<LLMConfig>('/config/llm', {
    provider,
  })
  return res.data
}

