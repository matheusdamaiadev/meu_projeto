import api from "./api";

export default {
  async getTasks(projectId = null) {
    const url = projectId
      ? `/tasks/?project=${projectId}`
      : "/tasks/";

    const response = await api.get(url);

    return response.data;
  },

  async createTask(task) {
    const response = await api.post(
      "/tasks/",
      task
    );

    return response.data;
  },

  async updateTask(id, task) {
    const response = await api.patch(
      `/tasks/${id}/`,
      task
    );

    return response.data;
  },

  async deleteTask(id) {
    await api.delete(
      `/tasks/${id}/`
    );
  },
};