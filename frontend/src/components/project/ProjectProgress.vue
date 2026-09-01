```vue
<template>
  <section class="progress-section">
    <div class="progress-header">
      <div>
        <h2>Progresso</h2>

        <p>{{ completedTasks }} de {{ totalTasks }} tarefas concluídas</p>
      </div>

      <span class="percentage"> {{ progress }}% </span>
    </div>

    <div class="progress-bar">
      <div class="progress-fill" :style="{ width: `${progress}%` }"></div>
    </div>
  </section>
</template>

<script setup>
import { computed } from "vue";

import { useTaskStore } from "../../stores/task";

const props = defineProps({
  projectId: {
    type: Number,

    required: true,
  },
});

const taskStore = useTaskStore();

const totalTasks = computed(() => {
  return taskStore.tasks.filter((task) => task.project === props.projectId).length;
});

const completedTasks = computed(() => {
  return taskStore.tasks.filter(
    (task) => task.project === props.projectId && task.completed
  ).length;
});

const progress = computed(() => {
  if (totalTasks.value === 0) {
    return 0;
  }

  return Math.round((completedTasks.value / totalTasks.value) * 100);
});
</script>

<style scoped>
.progress-section {
  margin-top: 28px;

  padding: 20px 22px;

  border: 1px solid #e5e5e5;

  border-radius: 12px;

  background: #fff;
}

.progress-header {
  display: flex;

  align-items: center;

  justify-content: space-between;

  gap: 20px;

  margin-bottom: 14px;
}

.progress-header h2 {
  margin: 0;

  color: #222;

  font-size: 15px;

  font-weight: 600;
}

.progress-header p {
  margin: 5px 0 0;

  color: #888;

  font-size: 12px;
}

.percentage {
  color: #222;

  font-size: 18px;

  font-weight: 600;
}

.progress-bar {
  width: 100%;

  height: 8px;

  overflow: hidden;

  border-radius: 999px;

  background: #eeeeee;
}

.progress-fill {
  height: 100%;

  border-radius: inherit;

  background: #111;

  transition: width 0.3s ease;
}
</style>
```
