<template>
  <div class="project-page">

    <button
      class="back-button"
      @click="goBack"
    >
      ← Voltar para projetos
    </button>


    <div v-if="loading">

      <div class="loading">
        Carregando projeto...
      </div>

    </div>


    <div v-else-if="project">


      <ProjectHeader
        :project="project"
        @edit="openEdit"
        @delete="openDelete"
      />



      <section class="tasks-section">

        <h2>
          Tarefas
        </h2>


        <div class="tasks-placeholder">

          <p>
            Tarefas serão implementadas futuramente.
          </p>

        </div>


      </section>




      <ProjectEditModal

        v-if="showEdit"

        :project="project"

        @close="showEdit = false"

      />




      <ProjectDeleteDialog
  v-if="showDelete && project"
  :project="project"
  @close="showDelete = false"
/>



    </div>


  </div>
</template>


<script setup>

import {
  onMounted,
  computed,
  ref
} from "vue";


import {
  useRoute,
  useRouter
} from "vue-router";


import { useProjectStore } from "../stores/project";


import ProjectHeader from "../components/project/ProjectHeader.vue";

import ProjectEditModal from "../components/project/ProjectEditModal.vue";

import ProjectDeleteDialog from "../components/project/ProjectDeleteDialog.vue";



const route = useRoute();

const router = useRouter();


const projectStore = useProjectStore();



const project = computed(() => {

  return projectStore.currentProject;

});


const loading = computed(() => {

  return projectStore.loading;

});


const showEdit = ref(false);

const showDelete = ref(false);





onMounted(async () => {

  await projectStore.fetchProject(
    route.params.id
  );

});





function goBack(){

  router.push({
    name:"projects"
  });

}





function openEdit(){

  showEdit.value = true;

}





function openDelete(){

  showDelete.value = true;

}





async function handleDeleted(){

  showDelete.value = false;

  await router.push({
    name:"projects"
  });

}


</script>


<style scoped>

.project-page {

  padding:32px;

}


.back-button {

  background:none;

  border:none;

  cursor:pointer;

  font-size:14px;

  color:#555;

  margin-bottom:24px;

  padding:0;

}


.back-button:hover {

  color:#000;

}


.tasks-section {

  margin-top:40px;

}


.tasks-section h2 {

  font-size:24px;

  margin-bottom:16px;

}


.tasks-placeholder {

  min-height:200px;

  border:1px dashed #aaa;

  border-radius:12px;

  display:flex;

  justify-content:center;

  align-items:center;

  color:#777;

}


.loading {

  padding:40px;

  text-align:center;

  color:#777;

}

</style>