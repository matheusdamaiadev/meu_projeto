<template>
  <div class="layout">
    <Sidebar />

    <div class="content">
      <Header />

      <main class="page">
        <router-view />
      </main>
    </div>
  </div>
</template>

<script setup>
import Sidebar from '../components/layout/Sidebar.vue'
import Header from '../components/layout/Header.vue'
</script>

<style scoped>
.layout {
  display: flex;
  min-height: 100vh;

  background: #f7f7f7;
}

.content {
  flex: 1;

  display: flex;
  flex-direction: column;
}

.page {
  flex: 1;

  padding: 32px;

  overflow-y: auto;
}
</style>