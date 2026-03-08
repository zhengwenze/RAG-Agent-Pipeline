<template>
  <div class="doc-upload">
    <h2>文档上传</h2>
    <input type="file" multiple />
    <button>上传</button>
  </div>
</template>

<script setup lang="ts">
// DocUpload component
</script>

<style scoped>
.doc-upload {
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 20px;
  text-align: center;
}

input[type="file"] {
  margin-bottom: 10px;
}

button {
  padding: 10px 20px;
  background-color: #2196F3;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

button:hover {
  background-color: #0b7dda;
}
</style>