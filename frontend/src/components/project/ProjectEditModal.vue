<template>

  <div class="overlay">

    <div class="modal">

      <div class="modal-header">

        <h2>
          Editar projeto
        </h2>


        <button
          class="close"
          @click="close"
        >
          ×
        </button>

      </div>


      <ProjectForm
        :project="project"
        @save="update"
        @cancel="close"
      />

    </div>

  </div>

</template>


<script setup>

import ProjectForm from "../projects/ProjectForm.vue";

import { useProjectStore } from "../../stores/project";


const props = defineProps({

  project: {

    type:Object,

    required:true

  }

});


const emit = defineEmits([

  "close"

]);


const projectStore = useProjectStore();



async function update(data){

  try {

    await projectStore.updateProject(
      props.project.id,
      data
    );


    close();


  } catch(error){

    console.error(
      error
    );

  }

}



function close(){

  emit("close");

}

</script>


<style scoped>

.overlay {

  position:fixed;

  inset:0;

  background:rgba(0,0,0,.35);

  backdrop-filter:blur(3px);

  display:flex;

  justify-content:center;

  align-items:center;

  z-index:100;

}


.modal {

  width:450px;

  max-height:90vh;

  overflow:auto;

  background:white;

  border-radius:16px;

  padding:28px;

  box-shadow:0 20px 50px rgba(0,0,0,.15);

}


.modal-header {

  display:flex;

  justify-content:space-between;

  align-items:center;

  margin-bottom:24px;

}


.modal-header h2 {

  margin:0;

  font-size:22px;

}


.close {

  border:none;

  background:none;

  font-size:26px;

  cursor:pointer;

  color:#666;

  line-height:1;

}


.close:hover {

  color:#000;

}

</style>