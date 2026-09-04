<template>
  <Modal v-model="isOpen" title="Editar projeto">
    <ProjectForm :project="project" @save="update" @cancel="close" />
  </Modal>
</template>

<script setup>
import { computed } from "vue";

import Modal from "../ui/Modal.vue";
import ProjectForm from "../projects/ProjectForm.vue";

import { useProjectStore } from "../../stores/project";

const props = defineProps({
  project: {
    type: Object,
    required: true,
  },
});

const emit = defineEmits(["close"]);

const projectStore = useProjectStore();

const isOpen = computed({
  get() {
    return true;
  },

  set(value) {
    if (!value) {
      close();
    }
  },
});

async function update(data) {
  try {
    await projectStore.updateProject(props.project.id, data);

    close();
  } catch (error) {
    console.error("Erro ao atualizar projeto:", error);
  }
}

function close() {
  emit("close");
}
</script>
