<template>
  <div class="home">
    <h1>智能问答系统</h1>
    <p>
      上传文档或笔记，系统自动解析、存储向量，用户提问时通过 RAG 检索上下文，生成个性化回答。
    </p>

    <div class="llm-switch">
      <label>
        当前模型提供方：
        <select v-model="llmProvider" @change="onProviderChange">
          <option value="ollama">Ollama（本地）</option>
          <option value="openai">OpenAI（云端）</option>
        </select>
      </label>
      <span class="hint">切换仅影响当前后端进程，重启后按默认配置恢复。</span>
    </div>

    <div class="chat-section">
      <ChatWindow />
      <ChatInput />
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'
import ChatWindow from '../components/chat/ChatWindow.vue'
import ChatInput from '../components/chat/ChatInput.vue'
import { getLLMConfig, setLLMProvider, type LLMProvider } from '../api/client'

const llmProvider = ref<LLMProvider>('ollama')
const switching = ref(false)

onMounted(async () => {
  try {
    const cfg = await getLLMConfig()
    llmProvider.value = cfg.provider
  } catch (e) {
    // 忽略配置加载错误，保持默认值
  }
})

const onProviderChange = async () => {
  if (switching.value) return
  switching.value = true
  try {
    await setLLMProvider(llmProvider.value)
  } catch (e) {
    // 失败时不改变当前显示的值
  } finally {
    switching.value = false
  }
}
</script>

<style scoped>
.home {
  padding: 20px;
}

h1 {
  color: #333;
}

p {
  color: #666;
  margin-top: 10px;
}

.llm-switch {
  margin-top: 16px;
  margin-bottom: 8px;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.llm-switch select {
  margin-left: 8px;
}

.hint {
  font-size: 12px;
  color: #999;
}

.chat-section {
  margin-top: 24px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}
</style>