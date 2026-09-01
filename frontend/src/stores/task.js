import { defineStore } from "pinia";
import taskService from "../services/taskService";

export const useTaskStore = defineStore("task", {
  state: () => ({
    tasks: [],
    loading: false,
    error: null,
    search: "",
  }),

  actions: {
    async fetchTasks(projectId) {
      this.loading = true;
      this.error = null;

      try {
        this.tasks = await taskService.getTasks(projectId);
      } catch (error) {
        this.error = error;

        console.error(
          "Erro ao buscar tasks:",
          error
        );
      } finally {
        this.loading = false;
      }
    },

    async fetchAllTasks() {
      this.loading = true;
      this.error = null;

      try {
        this.tasks = await taskService.getTasks();
      } catch (error) {
        this.error = error;

        console.error(
          "Erro ao buscar todas as tasks:",
          error
        );
      } finally {
        this.loading = false;
      }
    },

    async createTask(task) {
      this.error = null;

      try {
        const newTask =
          await taskService.createTask(task);

        this.tasks.push(newTask);

        return newTask;
      } catch (error) {
        console.error(
          "Erro ao criar task:",
          error
        );

        throw error;
      }
    },

    async updateTask(id, task) {
      this.error = null;

      try {
        const updatedTask =
          await taskService.updateTask(
            id,
            task
          );

        const index =
          this.tasks.findIndex(
            (task) => task.id === id
          );

        if (index !== -1) {
          this.tasks[index] = updatedTask;
        }

        return updatedTask;
      } catch (error) {
        console.error(
          "Erro ao atualizar task:",
          error
        );

        throw error;
      }
    },

    async deleteTask(id) {
      this.error = null;

      try {
        await taskService.deleteTask(id);

        this.tasks =
          this.tasks.filter(
            (task) => task.id !== id
          );
      } catch (error) {
        console.error(
          "Erro ao excluir task:",
          error
        );

        throw error;
      }
    },

    clearSearch() {
      this.search = "";
    },
  },
}); 