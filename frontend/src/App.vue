<template>
  <router-view />
  <Toast
  :message="notificationMessage"
  :type="notificationType"
  :duration="notificationDuration"
/>
</template>

<script setup>
</script>

<style scoped>
</style>
<script setup>

import { computed } from "vue";

import Toast from "./components/ui/Toast.vue";

import { useNotificationStore } from "./stores/notification";


const notificationStore = useNotificationStore();


const notificationMessage = computed(() => {

  return notificationStore.message;

});


const notificationType = computed(() => {

  return notificationStore.type;

});


const notificationDuration = computed(() => {

  return notificationStore.duration;

});

</script>