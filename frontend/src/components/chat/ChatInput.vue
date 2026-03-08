<template>
  <div class="chat-input">
    <input
      v-model="text"
      type="text"
      placeholder="输入问题..."
      @keyup.enter="handleSend"
    />
    <button :disabled="loading" @click="handleSend">
      {{ loading ? '发送中...' : '发送' }}
    </button>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useChatStore } from '../../store/chat'
import { queryApi } from '../../api/client'

const chatStore = useChatStore()
const text = ref('')
const loading = ref(false)

const handleSend = async () => {
  const content = text.value.trim()
  if (!content || loading.value) return

  const userMessageId = Date.now()
  chatStore.addMessage({
    id: userMessageId,
    role: 'user',
    text: content,
  })
  text.value = ''
  loading.value = true
  try {
    const res = await queryApi(content)
    chatStore.addMessage({
      id: userMessageId + 1,
      role: 'assistant',
      text: res.answer,
    })
  } catch (e: any) {
    chatStore.addMessage({
      id: userMessageId + 2,
      role: 'assistant',
      text: e?.message || '请求失败，请稍后重试',
    })
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.chat-input {
  display: flex;
  gap: 10px;
}

input {
  flex: 1;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

button {
  padding: 0 20px;
  background-color: #4caf50;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

button:disabled {
  opacity: 0.6;
  cursor: default;
}

button:hover:not(:disabled) {
  background-color: #45a049;
}
</style>