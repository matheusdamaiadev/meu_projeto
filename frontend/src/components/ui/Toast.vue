
<template>

  <Transition name="toast">

    <div
      v-if="visible"
      class="toast"
      :class="type"
    >

      <div class="toast-content">

        <div class="toast-icon">

          <Info
            v-if="type === 'info'"
            :size="18"
          />

          <Check
            v-else-if="type === 'success'"
            :size="18"
          />

          <AlertTriangle
            v-else-if="type === 'warning'"
            :size="18"
          />

          <XCircle
            v-else-if="type === 'error'"
            :size="18"
          />

        </div>


        <span>
          {{ message }}
        </span>

      </div>


      <button
        class="close-button"
        @click="close"
      >

        <X :size="16" />

      </button>

    </div>

  </Transition>

</template>


<script setup>

import {
  ref,
  watch
} from "vue";


import {
  Info,
  Check,
  AlertTriangle,
  XCircle,
  X
} from "lucide-vue-next";


const props = defineProps({

  message: {

    type: String,

    default: ""

  },


  type: {

    type: String,

    default: "info"

  },


  duration: {

    type: Number,

    default: 3000

  }

});


const visible = ref(false);

let timeout = null;


watch(

  () => props.message,

  (value) => {

    if (!value) {

      visible.value = false;

      return;

    }


    visible.value = true;


    clearTimeout(timeout);


    timeout = setTimeout(() => {

      visible.value = false;

    }, props.duration);

  },

  {
    immediate: true
  }

);


function close() {

  visible.value = false;

}

</script>


<style scoped>

.toast {

  position:fixed;

  top:24px;

  right:24px;

  min-width:280px;

  max-width:380px;

  display:flex;

  align-items:center;

  justify-content:space-between;

  gap:20px;

  padding:14px 16px;

  background:white;

  border:1px solid #e5e5e5;

  border-radius:12px;

  box-shadow:0 10px 30px rgba(0,0,0,.10);

  z-index:9999;

}


.toast-content {

  display:flex;

  align-items:center;

  gap:12px;

  color:#222;

  font-size:14px;

}


.toast-icon {

  display:flex;

  align-items:center;

  justify-content:center;

}


.success {

  border-color:#bbf7d0;

}


.success .toast-icon {

  color:#16a34a;

}


.warning {

  border-color:#fde68a;

}


.warning .toast-icon {

  color:#ca8a04;

}


.error {

  border-color:#fecaca;

}


.error .toast-icon {

  color:#dc2626;

}


.info {

  border-color:#bfdbfe;

}


.info .toast-icon {

  color:#2563eb;

}


.close-button {

  width:28px;

  height:28px;

  display:flex;

  align-items:center;

  justify-content:center;

  border:none;

  background:transparent;

  color:#999;

  border-radius:7px;

  cursor:pointer;

}


.close-button:hover {

  background:#f5f5f5;

  color:#111;

}


/* ANIMAÇÃO */

.toast-enter-active,
.toast-leave-active {

  transition:.25s ease;

}


.toast-enter-from,
.toast-leave-to {

  opacity:0;

  transform:translateY(-10px);

}

</style>
