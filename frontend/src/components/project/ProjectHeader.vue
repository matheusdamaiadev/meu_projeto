<template>

  <section class="project-header">

    <div class="header-top">

      <h1>
        {{ project.name }}
      </h1>


      <div class="actions">

        <button
          class="button edit"
          @click="emit('edit')"
        >
          Editar
        </button>


        <button
          class="button delete"
          @click="emit('delete')"
        >
          Excluir
        </button>


        <ProjectBoardButton
          :project-id="project.id"
        />

      </div>

    </div>


    <p class="description">
      {{ project.description || "Sem descrição" }}
    </p>


  </section>

</template>


<script setup>

import ProjectBoardButton from "./ProjectBoardButton.vue";


defineProps({

  project: {

    type:Object,

    required:true

  }

});


const emit = defineEmits([

  "edit",

  "delete"

]);

</script>


<style scoped>

.project-header {

  border:1px solid #000;

  border-radius:12px;

  padding:24px;

  background:white;

}


.header-top {

  display:flex;

  justify-content:space-between;

  align-items:center;

  gap:20px;

}


h1 {

  margin:0;

  font-size:32px;

  font-weight:700;

  color:#111;

}


.description {

  margin-top:16px;

  color:#666;

  line-height:1.6;

  font-size:15px;

}


.actions {

  display:flex;

  align-items:center;

  gap:10px;

}


.button {

  padding:9px 14px;

  border-radius:8px;

  border:1px solid #ddd;

  background:white;

  cursor:pointer;

  font-size:14px;

  font-weight:500;

  transition:.2s;

}


.button:hover {

  background:#f3f4f6;

  transform:translateY(-1px);

}


.delete {

  color:#dc2626;

  border-color:#fecaca;

}


.delete:hover {

  background:#fef2f2;

}

</style>