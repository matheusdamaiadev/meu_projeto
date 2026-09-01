```vue
<template>
  <Modal v-model="isOpen" title="Detalhes da tarefa">
    <div class="details">
      <!-- VISUALIZAÇÃO -->

      <template v-if="!editing">
        <div class="detail-section">
          <span class="detail-label"> Título </span>

          <h3 class="detail-title" :class="{ completed: task.completed }">
            {{ task.title }}
          </h3>
        </div>

        <div class="detail-section">
          <span class="detail-label"> Descrição </span>

          <p v-if="task.description" class="detail-description">
            {{ task.description }}
          </p>

          <p v-else class="no-description">Sem descrição</p>
        </div>

        <div class="detail-section">
          <span class="detail-label"> Status </span>

          <span class="status" :class="{ completed: task.completed }">
            {{ task.completed ? "Concluída" : "Pendente" }}
          </span>
        </div>

        <div class="actions">
          <button class="edit-button" @click="startEditing">Editar</button>

          <button class="complete-button" @click="toggleCompleted">
            {{ task.completed ? "Marcar como pendente" : "Marcar como concluída" }}
          </button>

          <button
            class="delete-button"
            :class="{ confirming: deleteConfirming }"
            @click="handleDelete"
          >
            <Trash2 :size="15" />

            {{ deleteConfirming ? "Clique novamente para excluir" : "Excluir tarefa" }}
          </button>
        </div>
      </template>

      <!-- EDIÇÃO -->

      <template v-else>
        <div class="form">
          <div class="form-group">
            <label> Título </label>

            <input
              v-model="editTitle"
              type="text"
              maxlength="200"
              placeholder="Título da tarefa"
            />
          </div>

          <div class="form-group">
            <label> Descrição </label>

            <textarea
              v-model="editDescription"
              rows="7"
              placeholder="Descrição da tarefa"
            ></textarea>
          </div>

          <p v-if="error" class="error">Não foi possível salvar a tarefa.</p>

          <div class="actions">
            <button class="cancel-button" @click="cancelEditing">Cancelar</button>

            <button
              class="save-button"
              :disabled="saving || !editTitle.trim()"
              @click="saveChanges"
            >
              {{ saving ? "Salvando..." : "Salvar alterações" }}
            </button>
          </div>
        </div>
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

watch(
  isOpen,

  (value) => {
    emit("update:modelValue", value);
  }
);

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
    await taskStore.updateTask(
      props.task.id,

      {
        completed: !props.task.completed,
      }
    );
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

/* SEÇÕES */

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

/* TÍTULO */

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

/* DESCRIÇÃO */

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

/* STATUS */

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

/* AÇÕES */

.actions {
  display: flex;

  flex-wrap: wrap;

  gap: 8px;

  padding-top: 4px;
}

.actions button {
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

/* EDITAR */

.edit-button {
  border: 1px solid #e5e5e5;

  background: #fff;

  color: #333;
}

.edit-button:hover {
  background: #f5f5f5;

  border-color: #d4d4d4;
}

/* CONCLUIR */

.complete-button {
  border: 1px solid #e5e5e5;

  background: #fff;

  color: #333;
}

.complete-button:hover {
  background: #f5f5f5;

  border-color: #d4d4d4;
}

/* EXCLUIR */

.delete-button {
  border: 1px solid #fecaca;

  background: #fff;

  color: #dc2626;
}

.delete-button:hover {
  background: #fef2f2;

  border-color: #fca5a5;
}

.delete-button.confirming {
  border-color: #b91c1c;

  background: #dc2626;

  color: #fff;
}

.delete-button.confirming:hover {
  border-color: #991b1b;

  background: #b91c1c;
}

/* FORMULÁRIO */

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

  padding: 11px 12px;

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
}

.form-group textarea {
  resize: vertical;

  line-height: 1.5;
}

.form-group input:focus,
.form-group textarea:focus {
  border-color: #111;

  box-shadow: 0 0 0 3px rgba(0, 0, 0, 0.05);
}

/* ERRO */

.error {
  margin: 0;

  color: #dc2626;

  font-size: 12px;
}

/* CANCELAR */

.cancel-button {
  border: 1px solid #e5e5e5;

  background: #fff;

  color: #555;
}

.cancel-button:hover {
  background: #f5f5f5;
}

/* SALVAR */

.save-button {
  border: 1px solid #111;

  background: #111;

  color: #fff;
}

.save-button:hover {
  background: #333;
}

.save-button:disabled {
  opacity: 0.5;

  cursor: not-allowed;
}

/* MOBILE */

@media (max-width: 600px) {
  .actions {
    flex-direction: column;
  }

  .actions button {
    width: 100%;
  }
}
</style>
```
