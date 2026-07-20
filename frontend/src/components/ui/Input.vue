<template>
  <div class="field">

    <label v-if="label">
      {{ label }}
    </label>

    <div class="input-wrapper">

      <input
        :type="currentType"
        :placeholder="placeholder"
        :value="modelValue"
        @input="updateValue"
      />

      <button
        v-if="type === 'password'"
        type="button"
        class="eye-button"
        @click="showPassword = !showPassword"
      >

        <EyeOff
          v-if="showPassword"
          :size="18"
        />

        <Eye
          v-else
          :size="18"
        />

      </button>

    </div>

  </div>
</template>


<script setup>

import { computed, ref } from 'vue'

import {
  Eye,
  EyeOff
} from 'lucide-vue-next'


const props = defineProps({

  label: {
    type: String,
    default: ''
  },

  type: {
    type: String,
    default: 'text'
  },

  placeholder: {
    type: String,
    default: ''
  },

  modelValue: {
    type: String,
    default: ''
  }

})


const emit = defineEmits([
  'update:modelValue'
])


const showPassword = ref(false)


const currentType = computed(() => {

  if (props.type === 'password') {

    return showPassword.value
      ? 'text'
      : 'password'

  }

  return props.type

})


function updateValue(event) {

  emit(
    'update:modelValue',
    event.target.value
  )

}

</script>


<style scoped>

.field {

  display: flex;

  flex-direction: column;

  gap: 8px;

}


label {

  font-size: 14px;

  font-weight: 500;

  color: #111;

}


.input-wrapper {

  position: relative;

}


input {

  width: 100%;

  height: 46px;


  background: #fff;


  border: 1px solid #e5e5e5;


  border-radius: 12px;


  padding: 0 45px 0 14px;


  font-size: 14px;


  color: #111;


  outline: none;


  transition: .2s;

}


input::placeholder {

  color: #a3a3a3;

}



input:hover {

  border-color: #d4d4d4;

}



input:focus {

  border-color: #111;

  box-shadow:

    0 0 0 3px rgba(0,0,0,.05);

}



.eye-button {

  position: absolute;


  right: 14px;

  top: 50%;


  transform: translateY(-50%);


  display: flex;

  align-items: center;

  justify-content: center;


  background: transparent;


  border: none;


  color: #737373;


  padding: 4px;


  cursor: pointer;


  transition: .2s;

}



.eye-button:hover {

  color: #111;

}

</style>