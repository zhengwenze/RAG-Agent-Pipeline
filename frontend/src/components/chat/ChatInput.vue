<template>
  <div class="chat-input">
    <input type="text" placeholder="输入问题..." />
    <button>发送</button>
  </div>
</template>

<script setup lang="ts">
// ChatInput component
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
  background-color: #4CAF50;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

button:hover {
  background-color: #45a049;
}
</style>