<template>

  <button
    class="board-button"
    @click="openBoard"
  >

    Abrir mural

  </button>

</template>



<script setup>

import { useRouter } from "vue-router";


const props = defineProps({

  projectId: {

    type: Number,

    required: true

  }

});



const router = useRouter();



function openBoard(){

  router.push({
    name: "project-board",
    params:{
      id: props.projectId
    }
  });

}


</script>



<style scoped>


.board-button {

  padding:10px 16px;

  border-radius:8px;

  border:none;

  cursor:pointer;

  background:#f3f4f6;

  color:#374151;

  font-weight:500;

}



.board-button:hover {

  background:#e5e7eb;

}


</style>