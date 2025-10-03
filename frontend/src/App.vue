<template>
  <div id="app">
    <router-view />
  </div>
</template>

<script setup lang="ts">
// 这里可以添加全局的逻辑
</script>

<style>
:root {
  --primary-color: #409EFF;
  --text-color: #2c3e50;
  --background-color: #f5f5f5;
  --border-color: #dcdfe6;
  --success-color: #67c23a;
  --warning-color: #e6a23c;
  --danger-color: #f56c6c;
  --info-color: #909399;
}

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  margin: 0;
  padding: 0;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
  font-size: 14px;
  line-height: 1.5;
  color: var(--text-color);
  background: linear-gradient(135deg, #e0e5ec 0%, #a8b8d8 100%);
  width: 100%;
  height: 100vh;
  overflow-y: auto; /* 使用浏览器滚动条 */
}

#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: var(--text-color);
  width: 100%;
  height: 100%;
}
</style>
