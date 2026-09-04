<template>
  <Modal v-model="isOpen" title="Nova tarefa">
    <form class="task-form" @submit.prevent="createTask">
      <div class="field">
        <label for="task-title">Título</label>

        <input
          id="task-title"
          v-model="title"
          type="text"
          placeholder="Digite o nome da tarefa..."
          autofocus
          :disabled="submitting"
        />
      </div>

      <div class="field">
        <label for="task-description">Descrição</label>

        <textarea
          id="task-description"
          v-model="description"
          placeholder="Adicione uma descrição (opcional)..."
          rows="4"
          :disabled="submitting"
        ></textarea>
      </div>

      <div class="actions">
        <button
          type="button"
          class="button secondary"
          :disabled="submitting"
          @click="close"
        >
          Cancelar
        </button>

        <button
          type="submit"
          class="button primary"
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
  color: #444;

  font-size: 13px;
  font-weight: 500;
}

.field input,
.field textarea {
  width: 100%;

  box-sizing: border-box;

  border: 1px solid #ddd;
  border-radius: 9px;

  outline: none;

  background: #fff;
  color: #111;

  font-family: inherit;
  font-size: 14px;

  transition: 0.2s ease;
}

.field input {
  height: 42px;
  padding: 0 12px;
}

.field textarea {
  min-height: 100px;
  padding: 11px 12px;

  resize: vertical;
  line-height: 1.5;
}

.field input:focus,
.field textarea:focus {
  border-color: #111;
  box-shadow: 0 0 0 3px rgba(0, 0, 0, 0.05);
}

.field input::placeholder,
.field textarea::placeholder {
  color: #aaa;
}

.actions {
  display: flex;
  justify-content: flex-end;
  gap: 8px;

  padding-top: 4px;
}

.button {
  height: 38px;

  display: flex;
  align-items: center;
  justify-content: center;

  padding: 0 15px;

  border-radius: 9px;

  font-family: inherit;
  font-size: 13px;
  font-weight: 500;

  cursor: pointer;

  transition: 0.2s ease;
}

.button.secondary {
  border: 1px solid #e5e5e5;

  background: #fff;
  color: #444;
}

.button.secondary:hover {
  background: #f5f5f5;
  border-color: #d4d4d4;
}

.button.primary {
  border: 1px solid #111;

  background: #111;
  color: #fff;
}

.button.primary:hover {
  background: #333;
}

.button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

@media (max-width: 600px) {
  .actions {
    flex-direction: column-reverse;
  }

  .button {
    width: 100%;
  }
}
</style>
