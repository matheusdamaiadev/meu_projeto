<template>
  <button
    class="button"
    :type="type"
  >
    <slot />
  </button>
</template>

<script setup>
defineProps({
  type: {
    type: String,
    default: 'button'
  }
})
</script>

<style scoped>
.button {
  height: 44px;

  padding: 0 20px;

  border: none;

  border-radius: 12px;

  background: #111;

  color: white;

  font-weight: 600;

  display: flex;
  align-items: center;
  justify-content: center;

  transition: .2s;

  cursor: pointer;
}

.button:hover {
  background: #2a2a2a;
}

.button:active {
  transform: scale(.98);
}
</style>