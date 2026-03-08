<template>
  <div class="chat-window">
    <h2>聊天窗口</h2>
    <div class="messages">
      <!-- 消息列表 -->
    </div>
  </div>
</template>

<script setup lang="ts">
// ChatWindow component
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
}
</style>