import { defineStore } from "pinia";
import { ref } from "vue";

export const useFriendStore = defineStore("friend", () => {
  const search = ref("");

  return {
    search,
  };
});