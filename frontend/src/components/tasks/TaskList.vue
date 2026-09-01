<script setup>
import { computed, onMounted, ref } from "vue";

import { useTaskStore } from "../../stores/task";

import TaskItem from "./TaskItem.vue";

const props = defineProps({
  projectId: {
    type: Number,
    required: true,
  },
});

const taskStore = useTaskStore();

const activeFilter = ref("pending");

onMounted(() => {
  taskStore.fetchTasks(props.projectId);
});

/* =========================
   BUSCA
========================= */

const searchedTasks = computed(() => {
  const search = taskStore.search.trim().toLowerCase();

  if (!search) {
    return taskStore.tasks;
  }

  return taskStore.tasks.filter((task) => {
    const title = task.title?.toLowerCase() || "";
    const description = task.description?.toLowerCase() || "";

    return title.includes(search) || description.includes(search);
  });
});

/* =========================
   FILTROS
========================= */

const pendingTasks = computed(() => {
  return searchedTasks.value.filter((task) => !task.completed);
});

const completedTasks = computed(() => {
  return searchedTasks.value.filter((task) => task.completed);
});

const visibleTasks = computed(() => {
  if (activeFilter.value === "completed") {
    return completedTasks.value;
  }

  return pendingTasks.value;
});

/* =========================
   CONTADORES
========================= */

const totalTasks = computed(() => {
  return searchedTasks.value.length;
});
</script>

<template>
  <section class="task-list">
    <!-- CABEÇALHO -->

    <div class="task-header">
      <div>
        <h2>Tarefas</h2>

        <p>Organize as tarefas deste projeto.</p>
      </div>

      <span class="task-count">
        {{ totalTasks }}

        {{ totalTasks === 1 ? "tarefa" : "tarefas" }}
      </span>
    </div>

    <!-- FILTROS -->

    <div class="filters">
      <button
        class="filter-button"
        :class="{
          active: activeFilter === 'pending',
        }"
        @click="activeFilter = 'pending'"
      >
        Pendentes

        <span>
          {{ pendingTasks.length }}
        </span>
      </button>

      <button
        class="filter-button"
        :class="{
          active: activeFilter === 'completed',
        }"
        @click="activeFilter = 'completed'"
      >
        Concluídas

        <span>
          {{ completedTasks.length }}
        </span>
      </button>
    </div>

    <!-- LOADING -->

    <div v-if="taskStore.loading" class="state">Carregando tarefas...</div>

    <!-- ERRO -->

    <div v-else-if="taskStore.error" class="state error">
      Não foi possível carregar as tarefas.
    </div>

    <!-- NENHUM RESULTADO DA BUSCA -->

    <div v-else-if="taskStore.search.trim() && searchedTasks.length === 0" class="empty">
      <div class="empty-title">Nenhuma tarefa encontrada</div>

      <div class="empty-description">
        Não encontramos tarefas para "{{ taskStore.search }}".
      </div>
    </div>

    <!-- LISTA VAZIA -->

    <div v-else-if="visibleTasks.length === 0" class="empty">
      <div class="empty-title">
        {{
          activeFilter === "pending"
            ? "Nenhuma tarefa pendente"
            : "Nenhuma tarefa concluída"
        }}
      </div>

      <div class="empty-description">
        {{
          activeFilter === "pending"
            ? "As tarefas que você criar aparecerão aqui."
            : "As tarefas concluídas aparecerão aqui."
        }}
      </div>
    </div>

    <!-- TASKS -->

    <div v-else class="tasks">
      <TaskItem v-for="task in visibleTasks" :key="task.id" :task="task" />
    </div>
  </section>
</template>

<style scoped>
.task-list {
  width: 100%;
}

/* =========================
   CABEÇALHO
========================= */

.task-header {
  display: flex;

  align-items: flex-end;

  justify-content: space-between;

  margin-bottom: 20px;
}

.task-header h2 {
  margin: 0;

  font-size: 22px;

  font-weight: 600;

  color: #111;
}

.task-header p {
  margin: 5px 0 0;

  font-size: 13px;

  color: #888;
}

.task-count {
  font-size: 12px;

  color: #999;
}

/* =========================
   FILTROS
========================= */

.filters {
  display: flex;

  gap: 4px;

  width: fit-content;

  padding: 4px;

  margin-bottom: 16px;

  border: 1px solid #e5e5e5;

  border-radius: 9px;

  background: #f8f8f8;
}

.filter-button {
  display: flex;

  align-items: center;

  gap: 7px;

  height: 32px;

  padding: 0 11px;

  border: 0;

  border-radius: 6px;

  background: transparent;

  color: #777;

  cursor: pointer;

  font-family: inherit;

  font-size: 12px;

  font-weight: 500;

  transition: 0.2s ease;
}

.filter-button span {
  min-width: 18px;

  text-align: center;

  font-size: 11px;

  color: #999;
}

.filter-button:hover {
  color: #222;
}

.filter-button.active {
  background: white;

  color: #111;

  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08);
}

.filter-button.active span {
  color: #555;
}

/* =========================
   LISTA
========================= */

.tasks {
  display: flex;

  flex-direction: column;

  gap: 8px;
}

/* =========================
   ESTADOS
========================= */

.state {
  padding: 32px 20px;

  text-align: center;

  color: #999;

  font-size: 13px;
}

.error {
  color: #999;
}

.empty {
  padding: 40px 20px;

  border: 1px dashed #ddd;

  border-radius: 10px;

  text-align: center;
}

.empty-title {
  font-size: 13px;

  font-weight: 500;

  color: #555;
}

.empty-description {
  margin-top: 5px;

  font-size: 12px;

  color: #999;
}
</style>
