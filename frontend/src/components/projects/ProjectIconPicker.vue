<template>

  <div class="icon-picker">

    <button
      type="button"
      v-for="icon in icons"
      :key="icon.value"
      class="icon-button"
      :class="{ active: modelValue === icon.value }"
      @click="$emit('update:modelValue', icon.value)"
    >

      <component
        v-if="icon.component"
        :is="icon.component"
        :size="20"
      />

      <span v-else>
        Sem
      </span>

    </button>

  </div>

</template>

<script setup>

import { projectIconList } from "../../utils/projectIcons";

const icons = projectIconList;

defineProps({
  modelValue: {
    type: String,
    default: ""
  }
});

defineEmits([
  "update:modelValue"
]);


</script>

<style scoped>

.icon-picker {

  display: flex;

  flex-wrap: wrap;

  gap: 12px;

}

.icon-button {

  width: 48px;

  height: 48px;

  display: flex;

  align-items: center;

  justify-content: center;

  border: 1px solid #e5e5e5;

  border-radius: 12px;

  background: white;

  cursor: pointer;

  transition: .2s;

}

.icon-button:hover {

  background: #f5f5f5;

}

.icon-button.active {

  border-color: #111;

  background: #111;

  color: white;

}

.icon-button span {

  font-size: 11px;

  font-weight: 600;

}

</style>