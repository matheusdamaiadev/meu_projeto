
import { defineStore } from "pinia";


export const useNotificationStore = defineStore("notification", {


  state: () => ({

    message: "",

    type: "info",

    duration: 3000

  }),


  actions: {


    show(message,type = "info",duration = 3000){

      this.message = message;

      this.type = type;

      this.duration = duration;

    },


    clear(){

      this.message = "";

    }

  }


});
