<template>
  <div class="chat-window">
    <h2>聊天窗口</h2>
    <div class="messages">
      <div
        v-for="msg in messages"
        :key="msg.id"
        class="message"
        :class="msg.role"
      >
        <strong>{{ msg.role === 'user' ? '你' : 'AI' }}：</strong>
        <span>{{ msg.text }}</span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useChatStore } from '../../store/chat'

const chatStore = useChatStore()
const messages = computed(() => chatStore.messages)
</script>

<style scoped>
.chat-window {
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 10px;
  height: 400px;
  display: flex;
  flex-direction: column;
}

.messages {
  flex: 1;
  overflow-y: auto;
  margin-bottom: 10px;
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.message {
  padding: 4px 8px;
  border-radius: 4px;
}

.message.user {
  align-self: flex-end;
  background-color: #e3f2fd;
}

.message.assistant {
  align-self: flex-start;
  background-color: #f1f8e9;
}
</style>