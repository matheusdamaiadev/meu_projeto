
<template>

  <Card
    class="project-card"
    @click="openProject"
  >

    <div class="project-header">

      <div
        class="icon"
        :class="project.color"
      >

        <component
          v-if="iconComponent"
          :is="iconComponent"
          :size="22"
        />

        <Folder
          v-else
          :size="22"
        />

      </div>


      <h2>
        {{ project.name }}
      </h2>


      <button
        class="pin-button"
        :class="{ pinned: project.is_pinned }"
        :title="project.is_pinned ? 'Desafixar projeto' : 'Fixar projeto'"
        @click.stop="togglePin"
      >

        <Pin
          :size="17"
          :fill="project.is_pinned ? 'currentColor' : 'none'"
        />

      </button>

    </div>


    <p>
      {{ project.description || "Sem descrição" }}
    </p>

  </Card>

</template>


<script setup>
  import {
  useNotificationStore
} from "../../stores/notification";

import {
  computed
} from "vue";


import {
  useRouter
} from "vue-router";


import {
  Folder,
  Pin
} from "lucide-vue-next";


import Card from "../ui/Card.vue";


import {
  projectIcons
} from "../../utils/projectIcons";


import {
  useProjectStore
} from "../../stores/project";



const props = defineProps({

  project: {

    type: Object,

    required: true

  }

});


const router = useRouter();

const projectStore = useProjectStore();
const notificationStore = useNotificationStore();


const iconComponent = computed(() => {

  return (
    projectIcons[props.project.icon]
    || null
  );

});

async function togglePin() {

  const willPin = !props.project.is_pinned;


  try {

    if (
      willPin &&
      projectStore.projects.filter(
        project => project.is_pinned
      ).length >= 5
    ) {

      notificationStore.show(
        "Só é possível fixar 5 projetos na sidebar.",
        "warning"
      );

      return;

    }


    await projectStore.togglePin(

      props.project.id,

      willPin

    );


    notificationStore.show(

      willPin
        ? "Projeto fixado na sidebar."
        : "Projeto desafixado da sidebar.",

      "success"

    );

  } catch (error) {

    console.error(

      "Erro ao alterar projeto fixado:",

      error

    );


    notificationStore.show(

      "Não foi possível alterar o projeto.",

      "error"

    );

  }

}



function openProject() {

  router.push({

    name: "project",

    params: {

      id: props.project.id

    }

  });

}

</script>


<style scoped>

.project-card {

  position:relative;

  display:flex;

  flex-direction:column;

  gap:16px;

  height:100%;

  cursor:pointer;

  transition:.2s ease;

}


.project-card:hover {

  transform:translateY(-3px);

  box-shadow:0 10px 25px rgba(0,0,0,.08);

}


.project-header {

  display:flex;

  align-items:center;

  gap:14px;

  padding-right:32px;

}


.icon {

  width:48px;

  height:48px;

  display:flex;

  align-items:center;

  justify-content:center;

  border-radius:12px;

  flex-shrink:0;

}


h2 {

  margin:0;

  font-size:18px;

  font-weight:600;

  overflow:hidden;

  text-overflow:ellipsis;

  white-space:nowrap;

}


p {

  margin:0;

  color:#737373;

  font-size:14px;

  line-height:1.5;

  display:-webkit-box;

  -webkit-line-clamp:2;

  -webkit-box-orient:vertical;

  overflow:hidden;

}


/* BOTÃO DE FIXAR */

.pin-button {

  position:absolute;

  top:16px;

  right:16px;

  width:32px;

  height:32px;

  display:flex;

  align-items:center;

  justify-content:center;

  border:1px solid #e5e5e5;

  border-radius:8px;

  background:white;

  color:#999;

  cursor:pointer;

  opacity:0;

  transition:.2s ease;

}


.project-card:hover .pin-button {

  opacity:1;

}


.pin-button:hover {

  background:#f5f5f5;

  color:#111;

  border-color:#d4d4d4;

}


.pin-button.pinned {

  opacity:1;

  color:#111;

  background:#f5f5f5;

  border-color:#d4d4d4;

}


/* CORES */

.blue {

  background:#dbeafe;

  color:#2563eb;

}


.green {

  background:#dcfce7;

  color:#16a34a;

}


.purple {

  background:#f3e8ff;

  color:#9333ea;

}


.orange {

  background:#ffedd5;

  color:#ea580c;

}


.red {

  background:#fee2e2;

  color:#dc2626;

}


.yellow {

  background:#fef9c3;

  color:#ca8a04;

}


.gray {

  background:#e5e5e5;

  color:#525252;

}

</style>