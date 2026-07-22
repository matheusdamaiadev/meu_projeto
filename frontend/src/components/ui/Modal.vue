<template>

  <Teleport to="body">

    <Transition name="modal">

      <div
        v-if="modelValue"
        class="overlay"
        @click.self="close"
      >

        <Card class="modal">

          <div
            v-if="title || $slots.header"
            class="header"
          >

            <slot name="header">

              <h2>{{ title }}</h2>

            </slot>

            <button
              class="close"
              @click="close"
            >
              ✕
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
    default: false
  },

  title: {
    type: String,
    default: ""
  }

})

const emit = defineEmits([
  "update:modelValue"
])

function close() {

  emit("update:modelValue", false)

}

</script>

<style scoped>

.overlay{

  position:fixed;

  inset:0;

  background:rgba(0,0,0,.45);

  display:flex;

  justify-content:center;

  align-items:center;

  z-index:999;

}

.modal{

  width:100%;

  max-width:600px;

  max-height:90vh;

  overflow:auto;

}

.header{

  display:flex;

  justify-content:space-between;

  align-items:center;

  padding-bottom:24px;

  margin-bottom:24px;

  border-bottom:1px solid #e5e5e5;

}

.header h2{

  font-size:22px;

  font-weight:600;

}

.close{

  width:40px;

  height:40px;

  border:none;

  border-radius:10px;

  background:transparent;

  cursor:pointer;

  font-size:18px;

  transition:.2s;

}

.close:hover{

  background:#f5f5f5;

}

.modal-enter-active,
.modal-leave-active{

  transition:.2s ease;

}

.modal-enter-from,
.modal-leave-to{

  opacity:0;

}

.modal-enter-from .modal,
.modal-leave-to .modal{

  transform:translateY(20px) scale(.98);

}

</style>