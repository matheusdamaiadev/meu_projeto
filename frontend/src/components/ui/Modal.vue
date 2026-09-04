<template>
  <Teleport to="body">
    <Transition name="modal">
      <div v-if="modelValue" class="overlay" @click.self="close">
        <Card class="modal">
          <div v-if="title || $slots.header" class="header">
            <slot name="header">
              <h2>{{ title }}</h2>
            </slot>

            <button class="close" type="button" aria-label="Fechar" @click="close">
              ×
            </button>
          </div>

          <div class="content">
            <slot />
          </div>
        </Card>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup>
import Card from "./Card.vue";

defineProps({
  modelValue: {
    type: Boolean,
    default: false,
  },

  title: {
    type: String,
    default: "",
  },
});

const emit = defineEmits(["update:modelValue"]);

function close() {
  emit("update:modelValue", false);
}
</script>

<style scoped>
.overlay {
  position: fixed;
  inset: 0;

  display: flex;
  align-items: center;
  justify-content: center;

  padding: 20px;
  box-sizing: border-box;

  background: rgba(0, 0, 0, 0.35);

  backdrop-filter: blur(4px);
  -webkit-backdrop-filter: blur(4px);

  z-index: 999;
}

.modal {
  width: 100%;
  max-width: 600px;
  max-height: 90vh;

  overflow: auto;

  box-sizing: border-box;

  box-shadow: 0 20px 50px rgba(0, 0, 0, 0.15);
}

.header {
  display: flex;
  align-items: center;
  justify-content: space-between;

  padding-bottom: 20px;
  margin-bottom: 24px;

  border-bottom: 1px solid #e5e5e5;
}

.header h2 {
  margin: 0;

  color: #111;

  font-size: 21px;
  font-weight: 600;
}

.close {
  width: 36px;
  height: 36px;

  display: flex;
  align-items: center;
  justify-content: center;

  border: none;
  border-radius: 9px;

  background: transparent;
  color: #666;

  font-family: inherit;
  font-size: 24px;
  line-height: 1;

  cursor: pointer;

  transition: 0.2s ease;
}

.close:hover {
  background: #f5f5f5;
  color: #111;
}

.content {
  width: 100%;
}

.modal-enter-active,
.modal-leave-active {
  transition: opacity 0.2s ease;
}

.modal-enter-active .modal,
.modal-leave-active .modal {
  transition: transform 0.2s ease, opacity 0.2s ease;
}

.modal-enter-from,
.modal-leave-to {
  opacity: 0;
}

.modal-enter-from .modal,
.modal-leave-to .modal {
  opacity: 0;
  transform: translateY(16px) scale(0.98);
}

@media (max-width: 600px) {
  .overlay {
    padding: 12px;
  }

  .modal {
    max-height: 94vh;
  }
}
</style>
