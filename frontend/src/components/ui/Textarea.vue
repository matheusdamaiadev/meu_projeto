<template>
  <div class="input-group">

    <label
      v-if="label"
      class="label"
    >
      {{ label }}
    </label>

    <textarea
      :value="modelValue"
      :placeholder="placeholder"
      :rows="rows"
      :disabled="disabled"
      class="textarea"
      @input="$emit('update:modelValue', $event.target.value)"
    />

  </div>
</template>

<script setup>

defineProps({

  modelValue: {
    type: String,
    default: ""
  },

  label: {
    type: String,
    default: ""
  },

  placeholder: {
    type: String,
    default: ""
  },

  rows: {
    type: Number,
    default: 4
  },

  disabled: {
    type: Boolean,
    default: false
  }

})

defineEmits([
  "update:modelValue"
])

</script>

<style scoped>

.input-group {

  display: flex;
  flex-direction: column;
  gap: 8px;

}

.label {

  font-size: 14px;
  font-weight: 600;
  color: #171717;

}

.textarea {

  width: 100%;

  min-height: 120px;

  padding: 12px 14px;

  border: 1px solid #e5e5e5;
  border-radius: 12px;

  background: white;

  font-size: 14px;
  font-family: inherit;
  color: #171717;

  resize: vertical;

  transition: all .2s ease;

}

.textarea::placeholder {

  color: #a3a3a3;

}

.textarea:hover {

  border-color: #d4d4d4;

}

.textarea:focus {

  outline: none;

  border-color: #111;

  box-shadow: 0 0 0 3px rgba(17,17,17,.08);

}

.textarea:disabled {

  background: #f5f5f5;
  cursor: not-allowed;

}

</style>