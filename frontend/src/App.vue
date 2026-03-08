<script setup lang="ts">
// App component
</script>

<template>
  <div class="app">
    <nav class="navbar">
      <div class="container">
        <h1 class="logo">智能问答系统</h1>
        <ul class="nav-links">
          <li><router-link to="/">首页</router-link></li>
          <li><router-link to="/documents">文档管理</router-link></li>
          <li><router-link to="/history">历史记录</router-link></li>
        </ul>
      </div>
    </nav>
    <div class="container">
      <router-view />
    </div>
  </div>
</template>

<style scoped>
.app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.navbar {
  background-color: #333;
  color: white;
  padding: 1rem 0;
}

.container {
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1rem;
}

.logo {
  margin: 0;
  font-size: 1.5rem;
}

.nav-links {
  list-style: none;
  display: flex;
  gap: 1rem;
  margin: 0;
  padding: 0;
}

.nav-links li a {
  color: white;
  text-decoration: none;
  padding: 0.5rem 1rem;
  border-radius: 4px;
}

.nav-links li a:hover {
  background-color: rgba(255, 255, 255, 0.1);
}

.container {
  flex: 1;
  padding: 2rem 0;
}
</style>
