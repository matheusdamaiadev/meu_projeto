```vue
<template>

  <div class="projects-page">

    <div class="page-header">

      <button
        class="create-button"
        @click="openCreate"
      >

        <Plus :size="17" />

        <span>
          Novo projeto
        </span>

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

      <p v-if="search">

        Nenhum projeto encontrado para
        "{{ search }}".

      </p>


      <p v-else>

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


import {
  Plus
} from "lucide-vue-next";


import { useProjectStore } from "../stores/project";


import ProjectCard from "../components/project/ProjectCard.vue";

import ProjectForm from "../components/projects/ProjectForm.vue";

import Modal from "../components/ui/Modal.vue";


const projectStore = useProjectStore();


const showModal = ref(false);


const search = computed(() => {

  return projectStore.search;

});


const projects = computed(() => {

  const term = search.value
    .toLowerCase()
    .trim();


  return [...projectStore.projects]

    .filter(project => {

      if (!term) {

        return true;

      }


      return (

        project.name
          ?.toLowerCase()
          .includes(term)

        ||

        project.description
          ?.toLowerCase()
          .includes(term)

      );

    })

    .sort((a, b) => {

      if (
        a.is_pinned &&
        !b.is_pinned
      ) {

        return -1;

      }


      if (
        !a.is_pinned &&
        b.is_pinned
      ) {

        return 1;

      }


      return 0;

    });

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

  display:inline-flex;

  align-items:center;

  justify-content:center;

  gap:8px;

  height:38px;

  padding:0 14px;

  border:1px solid #111;

  border-radius:9px;

  background:#111;

  color:#fff;

  cursor:pointer;

  font-size:13px;

  font-weight:500;

  transition:
    background .2s ease,
    border-color .2s ease,
    transform .2s ease;

}


.create-button:hover {

  background:#000;

  border-color:#000;

  transform:translateY(-1px);

}


.create-button:active {

  transform:translateY(0);

}


.projects-grid {

  display:grid;

  grid-template-columns:repeat(
    auto-fill,
    minmax(260px,1fr)
  );

  gap:20px;

}


.loading,
.empty {

  padding:50px;

  text-align:center;

  color:#777;

}

</style>
```
