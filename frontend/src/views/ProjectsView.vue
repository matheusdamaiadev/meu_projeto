<template>
  <div class="projects-page">

    <div class="page-header">

      <button
        class="create-button"
        @click="openCreate"
      >
        + Novo projeto
      </button>

    </div>


    <div
      v-if="loading"
      class="loading"
    >
      Carregando projetos...
    </div>


    <div
      v-else-if="projects.length"
      class="projects-grid"
    >

      <ProjectCard
        v-for="project in projects"
        :key="project.id"
        :project="project"
      />

    </div>


    <div
      v-else
      class="empty"
    >

      <p>
        Você ainda não possui projetos.
      </p>

    </div>



    <Modal
      v-model="showModal"
      title="Criar projeto"
    >

      <ProjectForm
        @save="create"
        @cancel="closeModal"
      />

    </Modal>


  </div>
</template>


<script setup>

import {
  computed,
  ref,
  onMounted
} from "vue";


import { useProjectStore } from "../stores/project";


import ProjectCard from "../components/project/ProjectCard.vue";

import ProjectForm from "../components/projects/ProjectForm.vue";

import Modal from "../components/ui/Modal.vue";



const projectStore = useProjectStore();


const showModal = ref(false);



const projects = computed(() => {

  return projectStore.projects;

});



const loading = computed(() => {

  return projectStore.loading;

});





onMounted(async () => {

  await projectStore.fetchProjects();

});





function openCreate(){

  showModal.value = true;

}





function closeModal(){

  showModal.value = false;

}





async function create(data){

  try {

    await projectStore.createProject(data);

    closeModal();


  } catch(error){

    throw error;

  }

}

</script>


<style scoped>

.projects-page {

  padding:32px;

}


.page-header {

  display:flex;

  justify-content:flex-start;

  align-items:center;

  margin-bottom:32px;

}


.create-button {

  background:#111;

  color:white;

  border:none;

  border-radius:10px;

  padding:12px 18px;

  cursor:pointer;

  font-weight:500;

  transition:.2s;

}


.create-button:hover {

  transform:translateY(-2px);

  background:#000;

}


.projects-grid {

  display:grid;

  grid-template-columns:repeat(auto-fill,minmax(260px,1fr));

  gap:20px;

}


.loading,
.empty {

  padding:50px;

  text-align:center;

  color:#777;

}

</style>