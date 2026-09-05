```vue
<template>
  <div class="project-page">
    <button class="back-button" @click="goBack">
      <ArrowLeft :size="16" />

      <span> Projetos </span>
    </button>

    <div v-if="loading">
      <div class="loading">Carregando projeto...</div>
    </div>

    <div v-else-if="project">
      <ProjectHeader :project="project" @edit="openEdit" @delete="openDelete" />

      <!-- MEMBROS DO PROJETO -->

      <ProjectMembers :project="project" />

      <!-- PROGRESSO DO PROJETO -->

      <ProjectProgress :project-id="Number(route.params.id)" />

      <!-- TAREFAS -->

      <section class="tasks-section">
        <TaskList :project-id="Number(route.params.id)" />
      </section>

      <!-- BOTÃO FLUTUANTE -->

      <button
        class="floating-add-button"
        @click="showTaskForm = true"
        aria-label="Criar tarefa"
      >
        +
      </button>

      <!-- MODAL DE CRIAÇÃO -->

      <TaskForm
        :project-id="Number(route.params.id)"
        :show="showTaskForm"
        @close="showTaskForm = false"
      />

      <!-- EDITAR PROJETO -->

      <ProjectEditModal v-if="showEdit" :project="project" @close="showEdit = false" />

      <!-- EXCLUIR PROJETO -->

      <ProjectDeleteDialog
        v-if="showDelete && project"
        :project="project"
        @close="showDelete = false"
      />
    </div>
  </div>
</template>

<script setup>
import { computed, ref, watch } from "vue";

import { useRoute, useRouter } from "vue-router";

import { ArrowLeft } from "lucide-vue-next";

import { useProjectStore } from "../stores/project";

import ProjectHeader from "../components/project/ProjectHeader.vue";

import ProjectMembers from "../components/project/ProjectMembers.vue";

import ProjectEditModal from "../components/project/ProjectEditModal.vue";

import ProjectDeleteDialog from "../components/project/ProjectDeleteDialog.vue";

import ProjectProgress from "../components/project/ProjectProgress.vue";

import TaskForm from "../components/tasks/TaskForm.vue";

import TaskList from "../components/tasks/TaskList.vue";

const route = useRoute();

const router = useRouter();

const projectStore = useProjectStore();

const project = computed(() => {
  return projectStore.currentProject;
});

const loading = computed(() => {
  return projectStore.loading;
});

const showEdit = ref(false);

const showDelete = ref(false);

const showTaskForm = ref(false);

/* =========================
   CARREGAR PROJETO
========================= */

watch(
  () => route.params.id,

  async (id) => {
    if (!id) {
      return;
    }

    showEdit.value = false;
    showDelete.value = false;
    showTaskForm.value = false;

    await projectStore.fetchProject(id);
  },

  {
    immediate: true,
  }
);

/* =========================
   VOLTAR
========================= */

function goBack() {
  router.push({
    name: "projects",
  });
}

/* =========================
   EDITAR
========================= */

function openEdit() {
  showEdit.value = true;
}

/* =========================
   EXCLUIR
========================= */

function openDelete() {
  showDelete.value = true;
}

/* =========================
   PROJETO EXCLUÍDO
========================= */

async function handleDeleted() {
  showDelete.value = false;

  await router.push({
    name: "projects",
  });
}
</script>

<style scoped>
.project-page {
  padding: 32px;
}

/* =========================
   BOTÃO VOLTAR
========================= */

.back-button {
  display: inline-flex;

  align-items: center;

  gap: 8px;

  height: 36px;

  padding: 0 12px;

  margin-bottom: 24px;

  border: 1px solid #e5e5e5;

  border-radius: 9px;

  background: white;

  color: #555;

  cursor: pointer;

  font-size: 13px;

  font-weight: 500;

  transition: 0.2s ease;
}

.back-button:hover {
  background: #f5f5f5;

  border-color: #d4d4d4;

  color: #111;
}

.back-button svg {
  transition: 0.2s ease;
}

.back-button:hover svg {
  transform: translateX(-2px);
}

/* =========================
   TAREFAS
========================= */

.tasks-section {
  margin-top: 40px;
}

/* =========================
   BOTÃO FLUTUANTE
========================= */

.floating-add-button {
  position: fixed;

  right: 32px;
  bottom: 32px;

  width: 52px;
  height: 52px;

  display: flex;
  align-items: center;
  justify-content: center;

  padding: 0;

  border: 0;
  border-radius: 50%;

  background: #111;
  color: white;

  font-family: inherit;
  font-size: 28px;
  font-weight: 300;
  line-height: 1;

  cursor: pointer;

  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.15);

  transition: 0.2s ease;

  z-index: 100;
}

.floating-add-button:hover {
  transform: translateY(-2px);

  background: #333;

  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.2);
}

/* =========================
   LOADING
========================= */

.loading {
  padding: 40px;

  text-align: center;

  color: #777;
}

/* =========================
   MOBILE
========================= */

@media (max-width: 700px) {
  .project-page {
    padding: 20px;
  }

  .floating-add-button {
    right: 20px;

    bottom: 20px;
  }
}
</style>
