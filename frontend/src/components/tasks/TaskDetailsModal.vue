<template>
  <Modal v-model="isOpen" title="Detalhes da tarefa">
    <div class="details">
      <template v-if="!editing">
        <div class="detail-section">
          <span class="detail-label">Título</span>

          <h3 class="detail-title" :class="{ completed: task.completed }">
            {{ task.title }}
          </h3>
        </div>

        <div class="detail-section">
          <span class="detail-label">Descrição</span>

          <p v-if="task.description" class="detail-description">
            {{ task.description }}
          </p>

          <p v-else class="no-description">Sem descrição</p>
        </div>

        <div class="detail-section">
          <span class="detail-label">Status</span>

          <span class="status" :class="{ completed: task.completed }">
            {{ task.completed ? "Concluída" : "Pendente" }}
          </span>
        </div>

        <div class="actions">
          <button type="button" class="button secondary" @click="startEditing">
            Editar
          </button>

          <button type="button" class="button secondary" @click="toggleCompleted">
            {{ task.completed ? "Marcar como pendente" : "Marcar como concluída" }}
          </button>

          <button
            type="button"
            class="button danger"
            :class="{ confirming: deleteConfirming }"
            @click="handleDelete"
          >
            <Trash2 :size="15" />

            {{ deleteConfirming ? "Clique novamente para excluir" : "Excluir tarefa" }}
          </button>
        </div>
      </template>

      <template v-else>
        <form class="form" @submit.prevent="saveChanges">
          <div class="form-group">
            <label for="edit-task-title">Título</label>

            <input
              id="edit-task-title"
              v-model="editTitle"
              type="text"
              maxlength="200"
              placeholder="Título da tarefa"
              :disabled="saving"
            />
          </div>

          <div class="form-group">
            <label for="edit-task-description">Descrição</label>

            <textarea
              id="edit-task-description"
              v-model="editDescription"
              rows="7"
              placeholder="Descrição da tarefa"
              :disabled="saving"
            ></textarea>
          </div>

          <p v-if="error" class="error">Não foi possível salvar a tarefa.</p>

          <div class="actions">
            <button
              type="button"
              class="button secondary"
              :disabled="saving"
              @click="cancelEditing"
            >
              Cancelar
            </button>

            <button
              type="submit"
              class="button primary"
              :disabled="saving || !editTitle.trim()"
            >
              {{ saving ? "Salvando..." : "Salvar alterações" }}
            </button>
          </div>
        </form>
      </template>
    </div>
  </Modal>
</template>

<script setup>
import { ref, watch } from "vue";
import { Trash2 } from "lucide-vue-next";

import Modal from "../ui/Modal.vue";
import { useTaskStore } from "../../stores/task";

const props = defineProps({
  modelValue: {
    type: Boolean,
    default: false,
  },

  task: {
    type: Object,
    required: true,
  },
});

const emit = defineEmits(["update:modelValue", "deleted"]);

const taskStore = useTaskStore();

const isOpen = ref(props.modelValue);
const editing = ref(false);
const saving = ref(false);
const error = ref(false);
const deleteConfirming = ref(false);

const editTitle = ref("");
const editDescription = ref("");

watch(
  () => props.modelValue,
  (value) => {
    isOpen.value = value;

    if (value) {
      editing.value = false;
      deleteConfirming.value = false;
      error.value = false;
    }
  }
);

watch(isOpen, (value) => {
  emit("update:modelValue", value);
});

function startEditing() {
  editTitle.value = props.task.title;
  editDescription.value = props.task.description || "";

  editing.value = true;
  deleteConfirming.value = false;
  error.value = false;
}

function cancelEditing() {
  editing.value = false;
  error.value = false;
}

async function saveChanges() {
  if (!editTitle.value.trim()) {
    return;
  }

  saving.value = true;
  error.value = false;

  try {
    await taskStore.updateTask(props.task.id, {
      title: editTitle.value.trim(),
      description: editDescription.value,
    });

    editing.value = false;
  } catch (err) {
    console.error("Erro ao editar tarefa:", err);
    error.value = true;
  } finally {
    saving.value = false;
  }
}

async function toggleCompleted() {
  try {
    await taskStore.updateTask(props.task.id, {
      completed: !props.task.completed,
    });
  } catch (err) {
    console.error("Erro ao alterar status:", err);
  }
}

async function handleDelete() {
  if (!deleteConfirming.value) {
    deleteConfirming.value = true;
    return;
  }

  try {
    await taskStore.deleteTask(props.task.id);

    deleteConfirming.value = false;
    isOpen.value = false;

    emit("deleted");
  } catch (err) {
    console.error("Erro ao excluir tarefa:", err);
  }
}
</script>

<style scoped>
.details {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.detail-section {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.detail-label {
  color: #999;

  font-size: 11px;
  font-weight: 500;

  text-transform: uppercase;
  letter-spacing: 0.04em;
}

.detail-title {
  margin: 0;

  color: #111;

  font-size: 22px;
  font-weight: 600;
  line-height: 1.4;

  overflow-wrap: anywhere;
  word-break: break-word;
}

.detail-title.completed {
  color: #999;
  text-decoration: line-through;
}

.detail-description {
  margin: 0;

  color: #555;

  font-size: 14px;
  line-height: 1.7;

  white-space: pre-wrap;
  overflow-wrap: anywhere;
  word-break: break-word;
}

.no-description {
  margin: 0;

  color: #aaa;
  font-size: 14px;
}

.status {
  width: fit-content;

  padding: 5px 9px;

  border: 1px solid #ddd;
  border-radius: 6px;

  color: #666;

  font-size: 12px;
}

.status.completed {
  background: #f5f5f5;
  color: #222;
}

.actions {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;

  padding-top: 4px;
}

.button {
  height: 38px;

  display: flex;
  align-items: center;
  justify-content: center;
  gap: 7px;

  padding: 0 14px;

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
  color: #333;
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

.button.danger {
  border: 1px solid #fecaca;

  background: #fff;
  color: #dc2626;
}

.button.danger:hover {
  background: #fef2f2;
  border-color: #fca5a5;
}

.button.danger.confirming {
  border-color: #b91c1c;

  background: #dc2626;
  color: #fff;
}

.button.danger.confirming:hover {
  background: #b91c1c;
}

.form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 7px;
}

.form-group label {
  color: #444;

  font-size: 13px;
  font-weight: 500;
}

.form-group input,
.form-group textarea {
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

.form-group input {
  height: 42px;
  padding: 0 12px;
}

.form-group textarea {
  padding: 11px 12px;

  resize: vertical;
  line-height: 1.5;
}

.form-group input:focus,
.form-group textarea:focus {
  border-color: #111;
  box-shadow: 0 0 0 3px rgba(0, 0, 0, 0.05);
}

.error {
  margin: 0;

  color: #dc2626;
  font-size: 12px;
}

.button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

@media (max-width: 600px) {
  .actions {
    flex-direction: column;
  }

  .button {
    width: 100%;
  }
}
</style>
