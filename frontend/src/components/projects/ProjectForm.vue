<template>

  <form
    class="project-form"
    @submit.prevent="submit"
  >


    <Input

      v-model="form.name"

      label="Nome"

      placeholder="Nome do projeto"

      required

    />




    <Textarea

      v-model="form.description"

      label="Descrição"

      placeholder="Descreva seu projeto..."

      :rows="4"

    />





    <div class="field">


      <label>
        Cor
      </label>



      <ProjectColorPicker

        v-model="form.color"

      />


    </div>





    <div class="field">


      <label>
        Ícone
      </label>



      <ProjectIconPicker

        v-model="form.icon"

      />


    </div>





    <div class="actions">



      <Button

        type="button"

        variant="secondary"

        @click="cancel"

      >

        Cancelar

      </Button>





      <Button

        type="submit"

      >

        Salvar

      </Button>



    </div>



  </form>


</template>





<script setup>


import {

  reactive,

  watch

} from "vue";



import Input from "../ui/Input.vue";

import Textarea from "../ui/Textarea.vue";

import Button from "../ui/Button.vue";


import ProjectColorPicker from "./ProjectColorPicker.vue";

import ProjectIconPicker from "./ProjectIconPicker.vue";







const props = defineProps({

  project: {

    type:Object,

    default:null

  }

});





const emit = defineEmits([

  "save",

  "cancel"

]);







const form = reactive({

  name:"",

  description:"",

  color:"blue",

  icon:""

});







watch(

  () => props.project,

  (value)=>{


    form.name =
      value?.name || "";



    form.description =
      value?.description || "";



    form.color =
      value?.color || "blue";



    form.icon =
      value?.icon || "";



  },

  {

    immediate:true

  }


);







function submit(){


  emit(

    "save",

    {

      name:form.name,

      description:form.description,

      color:form.color,

      icon:form.icon

    }

  );


}







function cancel(){


  emit("cancel");


}



</script>





<style scoped>


.project-form {


  display:flex;

  flex-direction:column;

  gap:24px;


}





.field {


  display:flex;

  flex-direction:column;

  gap:8px;


}





.field label {


  font-size:14px;

  font-weight:600;


}





.actions {


  display:flex;

  justify-content:flex-end;

  gap:12px;


}



</style>