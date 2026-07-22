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



    </div>






    <p>

      {{ project.description || "Sem descrição" }}

    </p>



  </Card>


</template>





<script setup>


import { computed } from "vue";


import { useRouter } from "vue-router";


import { Folder } from "lucide-vue-next";



import Card from "../ui/Card.vue";


import { projectIcons } from "../../utils/projectIcons";







const props = defineProps({

  project: {

    type:Object,

    required:true

  }

});







const router = useRouter();







const iconComponent = computed(() => {


  return (

    projectIcons[props.project.icon]

    || null

  );


});







function openProject(){


  router.push({

    name:"project",

    params:{

      id:props.project.id

    }

  });


}





</script>





<style scoped>


.project-card {


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