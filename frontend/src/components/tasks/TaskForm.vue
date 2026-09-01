<template>
  <Modal v-model="isOpen" title="Nova tarefa">
    <form class="task-form" @submit.prevent="createTask">
      <div class="field">
        <label> Título </label>

        <input
          v-model="title"
          type="text"
          placeholder="Digite o nome da tarefa..."
          autofocus
          :disabled="submitting"
        />
      </div>

      <div class="field">
        <label> Descrição </label>

        <textarea
          v-model="description"
          placeholder="Adicione uma descrição (opcional)..."
          rows="4"
          :disabled="submitting"
        ></textarea>
      </div>

      <div class="actions">
        <button type="button" class="cancel-button" @click="close" :disabled="submitting">
          Cancelar
        </button>

        <button
          type="submit"
          class="create-button"
          :disabled="!title.trim() || submitting"
        >
          {{ submitting ? "Criando..." : "Criar tarefa" }}
        </button>
      </div>
    </form>
  </Modal>
</template>

<script setup>
import { computed, ref } from "vue";

import Modal from "../ui/Modal.vue";

import { useTaskStore } from "../../stores/task";

const props = defineProps({
  projectId: {
    type: Number,
    required: true,
  },

  show: {
    type: Boolean,
    default: false,
  },
});

const emit = defineEmits(["close"]);

const taskStore = useTaskStore();

const title = ref("");

const description = ref("");

const submitting = ref(false);

const isOpen = computed({
  get() {
    return props.show;
  },

  set(value) {
    if (!value) {
      close();
    }
  },
});

async function createTask() {
  if (!title.value.trim()) {
    return;
  }

  submitting.value = true;

  try {
    await taskStore.createTask({
      project: props.projectId,

      title: title.value.trim(),

      description: description.value.trim(),

      completed: false,
    });

    title.value = "";

    description.value = "";

    emit("close");
  } catch (error) {
    console.error("Erro ao criar tarefa:", error);
  } finally {
    submitting.value = false;
  }
}

function close() {
  if (submitting.value) {
    return;
  }

  title.value = "";

  description.value = "";

  emit("close");
}
</script>

<style scoped>
.task-form {
  display: flex;

  flex-direction: column;

  gap: 20px;
}

.field {
  display: flex;

  flex-direction: column;

  gap: 7px;
}

.field label {
  font-size: 13px;

  font-weight: 500;

  color: #444;
}

.field input,
.field textarea {
  width: 100%;

  box-sizing: border-box;

  padding: 11px 12px;

  border: 1px solid #ddd;

  border-radius: 9px;

  background: white;

  color: #222;

  outline: none;

  font-family: inherit;

  font-size: 14px;

  transition: 0.2s ease;
}

.field input:focus,
.field textarea:focus {
  border-color: #999;
}

.field input::placeholder,
.field textarea::placeholder {
  color: #aaa;
}

.field textarea {
  resize: vertical;

  min-height: 100px;
}

.actions {
  display: flex;

  justify-content: flex-end;

  gap: 10px;

  margin-top: 4px;
}

.cancel-button,
.create-button {
  height: 38px;

  padding: 0 16px;

  border-radius: 9px;

  font-size: 13px;

  font-weight: 500;

  cursor: pointer;

  transition: 0.2s ease;
}

.cancel-button {
  border: 1px solid #e5e5e5;

  background: white;

  color: #555;
}

.cancel-button:hover {
  background: #f5f5f5;
}

.create-button {
  border: 1px solid #111;

  background: #111;

  color: white;
}

.create-button:hover {
  background: #333;
}

.create-button:disabled,
.cancel-button:disabled {
  opacity: 0.5;

  cursor: not-allowed;
}
</style>
