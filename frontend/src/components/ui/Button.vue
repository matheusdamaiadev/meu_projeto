<template>
  <button
    :type="type"
    :disabled="disabled"
    :class="[
      'button',
      variant,
      { disabled }
    ]"
  >
    <slot />
  </button>
</template>

<script setup>

defineProps({

  type: {
    type: String,
    default: "button"
  },

  variant: {
    type: String,
    default: "primary"
  },

  disabled: {
    type: Boolean,
    default: false
  }

})

</script>

<style scoped>

.button{

  height:44px;

  padding:0 20px;

  border-radius:12px;

  border:none;

  font-weight:600;

  font-size:14px;

  cursor:pointer;

  transition:.2s ease;

  display:flex;

  align-items:center;

  justify-content:center;

}

/* Primary */

.primary{

  background:#111;

  color:white;

}

.primary:hover{

  background:#2a2a2a;

}

/* Secondary */

.secondary{

  background:white;

  color:#111;

  border:1px solid #d4d4d4;

}

.secondary:hover{

  background:#f5f5f5;

}

/* Danger */

.danger{

  background:#dc2626;

  color:white;

}

.danger:hover{

  background:#b91c1c;

}

/* Ghost */

.ghost{

  background:transparent;

  color:#111;

}

.ghost:hover{

  background:#f5f5f5;

}

.button:active{

  transform:scale(.98);

}

.disabled{

  opacity:.5;

  cursor:not-allowed;

}

</style>