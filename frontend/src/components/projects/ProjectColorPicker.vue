<template>

  <div class="color-picker">

    <button
      type="button"
      v-for="color in colors"
      :key="color.value"
      class="color-button"
      :class="{ active: modelValue === color.value }"
      :style="{ backgroundColor: color.hex }"
      @click="$emit('update:modelValue', color.value)"
    />

  </div>

</template>

<script setup>

defineProps({
  modelValue: {
    type: String,
    default: "blue"
  }
})

defineEmits([
  "update:modelValue"
])

const colors = [
  { value: "blue", hex: "#2563EB" },
  { value: "green", hex: "#16A34A" },
  { value: "purple", hex: "#9333EA" },
  { value: "orange", hex: "#EA580C" },
  { value: "red", hex: "#DC2626" },
  { value: "yellow", hex: "#CA8A04" },
  { value: "gray", hex: "#525252" }
]

</script>

<style scoped>

.color-picker {

  display: flex;

  gap: 12px;

  flex-wrap: wrap;

}

.color-button {

  width: 38px;

  height: 38px;

  border-radius: 50%;

  border: 2px solid transparent;

  cursor: pointer;

  transition: .2s;

}

.color-button:hover {

  transform: scale(1.08);

}

.color-button.active {

  border-color: #111;

  transform: scale(1.12);

}

</style>