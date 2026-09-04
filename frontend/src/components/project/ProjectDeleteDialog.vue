<template>
  <Modal v-model="isOpen">
    <div class="confirmation">
      <div class="icon">
        <span>!</span>
      </div>

      <h2>Excluir projeto?</h2>

      <p>
        Você está prestes a excluir:
        <strong>{{ project.name }}</strong>
      </p>

      <p class="warning">Essa ação não pode ser desfeita.</p>

      <div class="actions">
        <button type="button" class="button cancel" :disabled="loading" @click="close">
          Cancelar
        </button>

        <button type="button" class="button delete" :disabled="loading" @click="remove">
          {{ loading ? "Excluindo..." : "Excluir projeto" }}
        </button>
      </div>
    </div>
  </Modal>
</template>

<script setup>
import { computed, ref } from "vue";
import { useRouter } from "vue-router";

import Modal from "../ui/Modal.vue";
import { useProjectStore } from "../../stores/project.js";

const props = defineProps({
  project: {
    type: Object,
    required: true,
  },
});

const emit = defineEmits(["close"]);

const router = useRouter();
const projectStore = useProjectStore();

const loading = ref(false);

const isOpen = computed({
  get() {
    return true;
  },

  set(value) {
    if (!value && !loading.value) {
      close();
    }
  },
});

function close() {
  if (loading.value) {
    return;
  }

  emit("close");
}

async function remove() {
  if (loading.value) {
    return;
  }

  try {
    loading.value = true;

    await projectStore.deleteProject(props.project.id);

    await router.push({
      name: "projects",
    });
  } catch (error) {
    console.error("Erro ao excluir projeto:", error);
  } finally {
    loading.value = false;
  }
}
</script>

<style scoped>
.confirmation {
  display: flex;
  flex-direction: column;
  align-items: center;

  text-align: center;
}

.icon {
  width: 48px;
  height: 48px;

  display: flex;
  align-items: center;
  justify-content: center;

  margin-bottom: 18px;

  border-radius: 50%;

  background: #fee2e2;
  color: #dc2626;

  font-size: 22px;
  font-weight: 700;
}

.confirmation h2 {
  margin: 0;

  color: #111;

  font-size: 21px;
  font-weight: 600;
}

.confirmation p {
  max-width: 360px;

  margin: 12px 0 0;

  color: #666;

  font-size: 14px;
  line-height: 1.5;
}

.confirmation strong {
  color: #111;
  font-weight: 600;
}

.warning {
  font-size: 12px !important;
  color: #999 !important;
}

.actions {
  width: 100%;

  display: flex;
  justify-content: center;
  gap: 8px;

  margin-top: 28px;
}

.button {
  height: 38px;

  padding: 0 16px;

  border-radius: 9px;

  font-family: inherit;
  font-size: 13px;
  font-weight: 500;

  cursor: pointer;

  transition: 0.2s ease;
}

.cancel {
  border: 1px solid #e5e5e5;

  background: #fff;
  color: #444;
}

.cancel:hover {
  background: #f5f5f5;
  border-color: #d4d4d4;
}

.delete {
  border: 1px solid #dc2626;

  background: #dc2626;
  color: #fff;
}

.delete:hover {
  border-color: #b91c1c;
  background: #b91c1c;
}

.button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

@media (max-width: 500px) {
  .actions {
    flex-direction: column-reverse;
  }

  .button {
    width: 100%;
  }
}
</style>
