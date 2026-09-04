```vue
<template>
  <div class="task-item" :class="{ completed }">
    <!-- CHECK -->

    <button
      class="check-button"
      :class="{ updating }"
      :disabled="updating"
      @click.stop="toggleCompleted"
    >
      <Check v-if="completed" :size="15" />
    </button>

    <!-- CONTEÚDO -->

    <button class="task-content" @click="openDetails">
      <span class="task-title">
        {{ task.title }}
      </span>

      <span v-if="task.description" class="task-description">
        {{ task.description }}
      </span>
    </button>

    <!-- EXCLUIR -->

    <button
      class="delete-button"
      :class="{ confirming: deleteConfirming }"
      :disabled="deleting"
      @click.stop="handleDelete"
    >
      <Trash2 :size="16" />

      <span v-if="deleteConfirming"> Clique novamente </span>
    </button>

    <!-- DETALHES -->

    <TaskDetailsModal v-if="showDetails" v-model="showDetails" :task="task" />
  </div>
</template>

<script setup>
import { computed, ref, onBeforeUnmount } from "vue";

import { Check, Trash2 } from "lucide-vue-next";

import { useTaskStore } from "../../stores/task";

import Modal from "../ui/Modal.vue";
import TaskDetailsModal from "./TaskDetailsModal.vue";

const props = defineProps({
  task: {
    type: Object,
    required: true,
  },
});

const taskStore = useTaskStore();

const showDetails = ref(false);

const deleteConfirming = ref(false);

const updating = ref(false);

const deleting = ref(false);

let deleteConfirmTimeout = null;

const completed = computed(() => {
  return props.task.completed;
});

function openDetails() {
  showDetails.value = true;

  deleteConfirming.value = false;

  clearDeleteConfirmTimeout();
}

function openDeleteConfirm() {
  showDetails.value = true;

  deleteConfirming.value = false;

  clearDeleteConfirmTimeout();
}

/* =========================
   TIMER DA CONFIRMAÇÃO
========================= */

function startDeleteConfirmTimeout() {
  clearDeleteConfirmTimeout();

  deleteConfirmTimeout = setTimeout(() => {
    deleteConfirming.value = false;

    deleteConfirmTimeout = null;
  }, 5000);
}

function clearDeleteConfirmTimeout() {
  if (deleteConfirmTimeout) {
    clearTimeout(deleteConfirmTimeout);

    deleteConfirmTimeout = null;
  }
}

/* =========================
   CONCLUIR / DESCONCLUIR
========================= */

async function toggleCompleted() {
  if (updating.value) {
    return;
  }

  updating.value = true;

  try {
    await taskStore.updateTask(props.task.id, {
      completed: !props.task.completed,
    });
  } catch (error) {
    console.error("Erro ao alterar status da tarefa:", error);
  } finally {
    updating.value = false;
  }
}

/* =========================
   EXCLUIR
========================= */

async function handleDelete() {
  if (deleting.value) {
    return;
  }

  /*
   * PRIMEIRO CLIQUE
   */

  if (!deleteConfirming.value) {
    deleteConfirming.value = true;

    startDeleteConfirmTimeout();

    return;
  }

  /*
   * SEGUNDO CLIQUE
   */

  clearDeleteConfirmTimeout();

  deleting.value = true;

  try {
    await taskStore.deleteTask(props.task.id);

    deleteConfirming.value = false;

    showDetails.value = false;
  } catch (error) {
    console.error("Erro ao excluir tarefa:", error);

    deleteConfirming.value = false;
  } finally {
    deleting.value = false;
  }
}

/* =========================
   LIMPEZA
========================= */

onBeforeUnmount(() => {
  clearDeleteConfirmTimeout();
});
</script>

<style scoped>
/* =========================
   TASK ITEM
========================= */

.task-item {
  display: flex;

  align-items: center;

  gap: 12px;

  width: 100%;

  max-width: 100%;

  box-sizing: border-box;

  padding: 12px 14px;

  border: 1px solid #e5e5e5;

  border-radius: 10px;

  background: #fff;

  overflow: hidden;

  transition: 0.2s ease;
}

.task-item:hover {
  border-color: #000000;
}

/* =========================
   CHECK
========================= */

.check-button {
  width: 20px;

  height: 20px;

  flex-shrink: 0;

  display: flex;

  align-items: center;

  justify-content: center;

  padding: 0;

  border: 1.5px solid #aaa;

  border-radius: 6px;

  background: #fff;

  color: #fff;

  cursor: pointer;

  transition: 0.2s ease;
}

.check-button:hover {
  border-color: #777;
}

.task-item.completed .check-button {
  background: #111;

  border-color: #111;
}

.check-button:disabled {
  cursor: wait;

  opacity: 0.6;
}

/* =========================
   CONTEÚDO
========================= */

.task-content {
  flex: 1;

  min-width: 0;

  width: 0;

  display: flex;

  flex-direction: column;

  align-items: flex-start;

  gap: 3px;

  padding: 0;

  border: 0;

  background: transparent;

  text-align: left;

  cursor: pointer;

  overflow: hidden;
}

.task-title {
  display: block;

  width: 100%;

  min-width: 0;

  overflow: hidden;

  white-space: nowrap;

  text-overflow: ellipsis;

  color: #222;

  font-size: 14px;

  font-weight: 500;
}

.task-description {
  display: block;

  width: 100%;

  min-width: 0;

  overflow: hidden;

  white-space: nowrap;

  text-overflow: ellipsis;

  color: #888;

  font-size: 12px;
}

.task-item.completed .task-title {
  color: #999;

  text-decoration: line-through;
}

.task-item.completed .task-description {
  color: #aaa;
}

/* =========================
   EXCLUIR
========================= */

.delete-button {
  min-width: 32px;

  height: 32px;

  flex-shrink: 0;

  display: flex;

  align-items: center;

  justify-content: center;

  gap: 6px;

  padding: 0 8px;

  border: 1px solid transparent;

  border-radius: 8px;

  background: transparent;

  color: #dc2626;

  cursor: pointer;

  opacity: 0;

  transition: 0.2s ease;
}

.task-item:hover .delete-button {
  opacity: 1;
}

.delete-button:hover {
  background: #fef2f2;

  border-color: #fecaca;
}

/* CONFIRMAÇÃO */

.delete-button.confirming {
  opacity: 1;

  border-color: #b91c1c;

  background: #dc2626;

  color: #fff;
}

.delete-button.confirming:hover {
  border-color: #991b1b;

  background: #b91c1b;
}

.delete-button:disabled {
  cursor: wait;

  opacity: 0.7;
}

/* =========================
   MOBILE
========================= */

@media (max-width: 600px) {
  .delete-button {
    opacity: 1;
  }
}
</style>
```
