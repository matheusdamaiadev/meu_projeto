<template>
  <div class="overlay">

    <div class="modal">

      <div class="icon">
        !
      </div>

      <h2>
        Excluir projeto?
      </h2>

      <p>
        Você está prestes a excluir:
        <strong>{{ project.name }}</strong>
      </p>


      <div class="actions">

        <button
          class="cancel"
          @click="close"
        >
          Cancelar
        </button>


        <button
          class="delete"
          @click="remove"
          :disabled="loading"
        >
          {{ loading ? "Excluindo..." : "Excluir projeto" }}
        </button>

      </div>

    </div>

  </div>
</template>


<script setup>

import { ref } from "vue";

import { useRouter } from "vue-router";

import { useProjectStore } from "../../stores/project.js";


const props = defineProps({

  project: {

    type:Object,

    required:true

  }

});


const emit = defineEmits([
  "close"
]);


const router = useRouter();

const projectStore = useProjectStore();


const loading = ref(false);



function close(){

  emit("close");

}



async function remove(){

  try {

    loading.value = true;


    await projectStore.deleteProject(
      props.project.id
    );


    await router.push("/projects");


  } catch(error){

    console.error(
      error
    );

  } finally {

    loading.value = false;

  }

}

</script>


<style scoped>

.overlay {

  position:fixed;

  inset:0;

  background:rgba(0,0,0,.35);

  backdrop-filter:blur(4px);

  display:flex;

  justify-content:center;

  align-items:center;

  z-index:100;

}


.modal {

  width:380px;

  background:white;

  border-radius:18px;

  padding:32px;

  text-align:center;

  box-shadow:0 20px 50px rgba(0,0,0,.15);

}


.icon {

  width:48px;

  height:48px;

  margin:0 auto 18px;

  display:flex;

  align-items:center;

  justify-content:center;

  border-radius:50%;

  background:#fee2e2;

  color:#dc2626;

  font-size:24px;

  font-weight:700;

}


h2 {

  margin:0;

  font-size:22px;

  color:#111;

}


p {

  margin-top:12px;

  color:#666;

  line-height:1.5;

}


strong {

  color:#111;

}


.actions {

  margin-top:28px;

  display:flex;

  justify-content:center;

  gap:12px;

}


button {

  padding:10px 18px;

  border-radius:10px;

  border:none;

  cursor:pointer;

  font-weight:500;

  transition:.2s;

}


.cancel {

  background:#f3f4f6;

  color:#333;

}


.cancel:hover {

  background:#e5e7eb;

}


.delete {

  background:#dc2626;

  color:white;

}


.delete:hover {

  background:#b91c1c;

  transform:translateY(-1px);

}


.delete:disabled {

  opacity:.6;

  cursor:not-allowed;

}

</style>