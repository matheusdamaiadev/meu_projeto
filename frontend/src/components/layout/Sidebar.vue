<template>
  <aside class="sidebar">
    <div>
      <div class="logo">
        <div class="logo-circle"></div>
        <h1>Momentum</h1>
      </div>

      <nav class="navigation">
        <RouterLink to="/dashboard" class="nav-item">
          <LayoutDashboard :size="18" />
          Dashboard
        </RouterLink>

        <RouterLink to="/projects" class="nav-item">
          <FolderKanban :size="18" />
          Projetos
        </RouterLink>
      </nav>

      <section class="recent-projects">
        <h2>Projetos recentes</h2>

        <button
          v-for="project in recentProjects"
          :key="project.id"
          class="project-item"
        >
          <span
            class="project-color"
            :style="{ backgroundColor: project.color }"
          ></span>

          {{ project.name }}
        </button>
      </section>
    </div>

    <button class="new-project">
      <Plus :size="18" />
      Novo Projeto
    </button>
  </aside>
</template>

<script setup>
import { RouterLink } from 'vue-router'
import { LayoutDashboard, FolderKanban, Plus } from 'lucide-vue-next'

const recentProjects = [
  {
    id: 1,
    name: 'Faculdade',
    color: '#3B82F6'
  },
  {
    id: 2,
    name: 'Academia',
    color: '#22C55E'
  },
  {
    id: 3,
    name: 'Casa',
    color: '#F97316'
  },
  {
    id: 4,
    name: 'Trabalho',
    color: '#A855F7'
  },
  {
    id: 5,
    name: 'Momentum',
    color: '#EF4444'
  }
]
</script>

<style scoped>
.sidebar {
  width: 270px;
  height: 100vh;

  background: #111;

  color: white;

  display: flex;
  flex-direction: column;
  justify-content: space-between;

  padding: 28px 20px;

  position: sticky;
  top: 0;
}

.logo {
  display: flex;
  align-items: center;
  gap: 12px;

  margin-bottom: 42px;
}

.logo-circle {
  width: 12px;
  height: 12px;

  background: white;

  border-radius: 50%;
}

.logo h1 {
  font-size: 24px;
}

.navigation {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 12px;

  color: #d6d6d6;

  padding: 12px 14px;

  border-radius: 12px;

  transition: .2s;
}

.nav-item:hover,
.router-link-active {
  background: #1d1d1d;

  color: white;
}

.recent-projects {
  margin-top: 38px;
}

.recent-projects h2 {
  color: #777;

  font-size: 13px;

  margin-bottom: 14px;

  text-transform: uppercase;

  letter-spacing: 1px;
}

.project-item {
  width: 100%;

  display: flex;
  align-items: center;
  gap: 12px;

  padding: 10px 14px;

  border: none;

  background: transparent;

  color: #d6d6d6;

  border-radius: 12px;

  transition: .2s;

  cursor: pointer;
}

.project-item:hover {
  background: #1d1d1d;

  color: white;
}

.project-color {
  width: 10px;
  height: 10px;

  border-radius: 50%;
}

.new-project {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;

  border: none;

  background: white;

  color: black;

  border-radius: 14px;

  padding: 14px;

  font-weight: 600;

  cursor: pointer;

  transition: .2s;
}

.new-project:hover {
  transform: translateY(-1px);
}
</style>