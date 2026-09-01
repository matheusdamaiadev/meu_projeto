```vue
<template>
  <section class="project-header">
    <div class="header-content">
      <div class="project-info">
        <div class="project-title-row">
          <div class="icon" :class="project.color">
            <component v-if="iconComponent" :is="iconComponent" :size="24" />

            <Folder v-else :size="24" />
          </div>

          <h1>
            {{ project.name }}
          </h1>
        </div>

        <p class="description">
          {{ project.description || "Sem descrição" }}
        </p>
      </div>

      <div class="actions">
        <button class="action-button" @click="emit('edit')">Editar</button>

        <button class="action-button delete" @click="emit('delete')">Excluir</button>

        <ProjectBoardButton :project-id="project.id" />
      </div>
    </div>
  </section>
</template>

<script setup>
import { computed } from "vue";

import { Folder } from "lucide-vue-next";

import ProjectBoardButton from "./ProjectBoardButton.vue";

import { projectIcons } from "../../utils/projectIcons";

const props = defineProps({
  project: {
    type: Object,

    required: true,
  },
});

const emit = defineEmits(["edit", "delete"]);

const iconComponent = computed(() => {
  return projectIcons[props.project.icon] || null;
});
</script>

<style scoped>
.project-header {
  border: 1px solid #e5e5e5;

  border-radius: 16px;

  padding: 28px 30px;

  background: #fff;

  box-shadow: 0 3px 12px rgba(0, 0, 0, 0.04);
}

.header-content {
  display: flex;

  justify-content: space-between;

  align-items: flex-start;

  gap: 30px;
}

.project-info {
  min-width: 0;
}

.project-title-row {
  display: flex;

  align-items: center;

  gap: 15px;
}

.icon {
  width: 50px;

  height: 50px;

  display: flex;

  align-items: center;

  justify-content: center;

  border-radius: 13px;

  flex-shrink: 0;
}

h1 {
  margin: 0;

  color: #111;

  font-size: 30px;

  font-weight: 700;

  letter-spacing: -0.5px;
}

.description {
  max-width: 700px;

  margin: 17px 0 0 65px;

  color: #737373;

  font-size: 14px;

  line-height: 1.6;
}

.actions {
  display: flex;

  align-items: center;

  gap: 8px;

  flex-shrink: 0;
}

.action-button {
  height: 38px;

  padding: 0 14px;

  border: 1px solid #e5e5e5;

  border-radius: 9px;

  background: #fff;

  color: #333;

  cursor: pointer;

  font-size: 13px;

  font-weight: 500;

  transition: 0.2s ease;
}

.action-button:hover {
  background: #f5f5f5;

  border-color: #d4d4d4;
}

.delete {
  color: #dc2626;

  border-color: #fecaca;
}

.delete:hover {
  background: #fef2f2;

  border-color: #fca5a5;
}

/* Cores dos projetos */

.blue {
  background: #dbeafe;

  color: #2563eb;
}

.green {
  background: #dcfce7;

  color: #16a34a;
}

.purple {
  background: #f3e8ff;

  color: #9333ea;
}

.orange {
  background: #ffedd5;

  color: #ea580c;
}

.red {
  background: #fee2e2;

  color: #dc2626;
}

.yellow {
  background: #fef9c3;

  color: #ca8a04;
}

.gray {
  background: #e5e5e5;

  color: #525252;
}

@media (max-width: 700px) {
  .project-header {
    padding: 22px;
  }

  .header-content {
    flex-direction: column;
  }

  .actions {
    width: 100%;

    flex-wrap: wrap;
  }

  .description {
    margin-left: 0;
  }
}
</style>
```
