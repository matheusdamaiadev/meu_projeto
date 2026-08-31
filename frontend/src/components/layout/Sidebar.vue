```vue
<template>

  <aside class="sidebar">

    <div>

      <!-- LOGO -->

      <div class="logo">

        <div class="logo-circle"></div>

        <h1>
          Momentum
        </h1>

      </div>


      <!-- NAVEGAÇÃO -->

      <nav class="navigation">

        <RouterLink
          to="/dashboard"
          class="nav-item"
        >

          <LayoutDashboard :size="18" />

          Dashboard

        </RouterLink>


        <RouterLink
          to="/projects"
          class="nav-item"
        >

          <FolderKanban :size="18" />

          Projetos

        </RouterLink>

      </nav>


      <!-- PROJETOS FIXADOS -->

      <section class="recent-projects">

        <div class="section-header">

          <h2>
            Projetos fixados
          </h2>

          <span class="pin-limit">
            {{ pinnedProjects.length }}/5
          </span>

        </div>


        <div
          v-if="pinnedProjects.length"
          class="project-list"
        >

          <div
            v-for="project in pinnedProjects"
            :key="project.id"
            class="project-item"
          >

            <button
              class="project-link"
              @click="openProject(project.id)"
            >

              <span
                class="project-color"
                :class="project.color"
              ></span>


              <span class="project-name">
                {{ project.name }}
              </span>

            </button>


            <button
              class="pin-button"
              title="Desafixar projeto"
              @click.stop="togglePin(project)"
            >

              <Pin
                :size="14"
                :fill="'currentColor'"
              />

            </button>

          </div>

        </div>


        <div
          v-else
          class="empty-projects"
        >

          <Pin :size="15" />

          <span>
            Nenhum projeto fixado
          </span>

        </div>

      </section>

    </div>


    <!-- NOVO PROJETO -->

    <button
      class="new-project"
      @click="createProject"
    >

      <Plus :size="18" />

      Novo Projeto

    </button>

  </aside>
</template>


<script setup>

import {
  computed,
  onMounted
} from "vue";


import {
  useRouter,
  RouterLink
} from "vue-router";


import {
  LayoutDashboard,
  FolderKanban,
  Plus,
  Pin
} from "lucide-vue-next";


import { useProjectStore } from "../../stores/project";


const router = useRouter();

const projectStore = useProjectStore();


const projects = computed(() => {

  return projectStore.projects;

});


const pinnedProjects = computed(() => {

  return projects.value

    .filter(project => project.is_pinned)

    .slice(0, 5);

});


onMounted(async () => {

  if (!projects.value.length) {

    await projectStore.fetchProjects();

  }

});

async function togglePin(project) {

  try {

    await projectStore.togglePin(
      project.id,
      false
    );

  } catch (error) {

    console.error(
      "Erro ao desafixar projeto:",
      error
    );

  }

}



function openProject(projectId) {

  router.push({

    name: "project",

    params: {
      id: projectId
    }

  });

}


function createProject() {

  router.push({
    name: "projects"
  });

}

</script>


<style scoped>

.sidebar {

  width:270px;

  height:100vh;

  background:#111;

  color:white;

  display:flex;

  flex-direction:column;

  justify-content:space-between;

  padding:28px 20px;

  position:sticky;

  top:0;

  box-sizing:border-box;

}


/* LOGO */

.logo {

  display:flex;

  align-items:center;

  gap:12px;

  margin-bottom:42px;

}


.logo-circle {

  width:12px;

  height:12px;

  background:white;

  border-radius:50%;

}


.logo h1 {

  margin:0;

  font-size:24px;

}


/* NAVEGAÇÃO */

.navigation {

  display:flex;

  flex-direction:column;

  gap:6px;

}


.nav-item {

  display:flex;

  align-items:center;

  gap:12px;

  color:#d6d6d6;

  padding:12px 14px;

  border-radius:12px;

  text-decoration:none;

  transition:.2s;

}


.nav-item:hover,
.router-link-active {

  background:#1d1d1d;

  color:white;

}


/* PROJETOS */

.recent-projects {

  margin-top:38px;

}


.section-header {

  display:flex;

  align-items:center;

  justify-content:space-between;

  padding:0 8px;

  margin-bottom:10px;

}


.recent-projects h2 {

  margin:0;

  color:#777;

  font-size:12px;

  text-transform:uppercase;

  letter-spacing:1px;

}


.pin-limit {

  color:#555;

  font-size:11px;

}


.project-list {

  display:flex;

  flex-direction:column;

  gap:2px;

}


.project-item {

  width:100%;

  display:flex;

  align-items:center;

  border-radius:10px;

  transition:.2s;

}


.project-item:hover {

  background:#1d1d1d;

}


/* LINK DO PROJETO */

.project-link {

  min-width:0;

  flex:1;

  display:flex;

  align-items:center;

  gap:11px;

  padding:10px 8px 10px 14px;

  border:none;

  background:transparent;

  color:#d6d6d6;

  cursor:pointer;

  text-align:left;

}


.project-link:hover {

  color:white;

}


.project-name {

  overflow:hidden;

  text-overflow:ellipsis;

  white-space:nowrap;

  font-size:14px;

}


/* COR DO PROJETO */

.project-color {

  width:9px;

  height:9px;

  border-radius:50%;

  flex-shrink:0;

}


.blue {

  background:#3b82f6;

}


.green {

  background:#22c55e;

}


.purple {

  background:#a855f7;

}


.orange {

  background:#f97316;

}


.red {

  background:#ef4444;

}


.yellow {

  background:#eab308;

}


.gray {

  background:#737373;

}


/* BOTÃO DE FIXAR */

.pin-button {

  width:32px;

  height:32px;

  margin-right:4px;

  display:flex;

  align-items:center;

  justify-content:center;

  border:none;

  border-radius:8px;

  background:transparent;

  color:#777;

  cursor:pointer;

  opacity:0;

  transition:.2s;

}


.project-item:hover .pin-button {

  opacity:1;

}


.pin-button:hover {

  background:#292929;

  color:white;

}


/* NENHUM PROJETO */

.empty-projects {

  display:flex;

  align-items:center;

  gap:8px;

  padding:10px 8px;

  color:#555;

  font-size:12px;

}


/* NOVO PROJETO */

.new-project {

  display:flex;

  align-items:center;

  justify-content:center;

  gap:10px;

  height:40px;

  border:1px solid white;

  background:white;

  color:black;

  border-radius:9px;

  font-size:13px;

  font-weight:500;

  cursor:pointer;

  transition:.2s;

}


.new-project:hover {

  background:#f5f5f5;

  transform:translateY(-1px);

}

</style>
```
