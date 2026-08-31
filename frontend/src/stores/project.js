
import { defineStore } from "pinia";


import {

  getProjects,

  getProject,

  createProject,

  updateProject,

  patchProject,

  deleteProject

} from "../services/projectService";





export const useProjectStore = defineStore("project", {


  state: () => ({


    projects: [],


    currentProject: null,


    loading: false,


    error: null,

    search: ""


  }),







  actions:{





    async fetchProjects(){


      this.loading = true;

      this.error = null;



      try {



        const response = await getProjects();



        this.projects = response.data;



      } catch(error){



        this.error =

          error.response?.data ||

          "Erro ao buscar projetos";



      } finally {



        this.loading = false;



      }


    },









    async fetchProject(id){



      this.loading = true;

      this.error = null;



      try {



        const response = await getProject(id);



        this.currentProject = response.data;



      } catch(error){



        this.currentProject = null;



        this.error =

          error.response?.data ||

          "Erro ao buscar projeto";



      } finally {



        this.loading = false;



      }



    },









    async createProject(data){



      this.error = null;



      try {



        const response = await createProject(data);



        this.projects.push(response.data);



        return response.data;



      } catch(error){



        this.error =

          error.response?.data ||

          "Erro ao criar projeto";



        throw error;



      }



    },









    async updateProject(id,data){



      this.error = null;



      try {



        const response = await updateProject(

          id,

          data

        );





        const index = this.projects.findIndex(

          project => project.id === id

        );





        if(index !== -1){



          this.projects[index] = response.data;



        }







        if(

          this.currentProject &&

          this.currentProject.id === id

        ){



          this.currentProject = response.data;



        }





        return response.data;



      } catch(error){



        this.error =

          error.response?.data ||

          "Erro ao atualizar projeto";



        throw error;



      }



    },









    async togglePin(id,isPinned){



      this.error = null;



      try {



        const response = await patchProject(

          id,

          {

            is_pinned: isPinned

          }

        );





        const index = this.projects.findIndex(

          project => project.id === id

        );





        if(index !== -1){



          this.projects[index] = response.data;



        }







        if(

          this.currentProject &&

          this.currentProject.id === id

        ){



          this.currentProject = response.data;



        }





        return response.data;



      } catch(error){



        this.error =

          error.response?.data ||

          "Erro ao alterar projeto fixado";



        throw error;



      }



    },









    async deleteProject(id){



      this.error = null;



      try {



        await deleteProject(id);





        this.projects = this.projects.filter(

          project => project.id !== id

        );







        if(

          this.currentProject &&

          this.currentProject.id === id

        ){



          this.currentProject = null;



        }





      } catch(error){



        this.error =

          error.response?.data ||

          "Erro ao excluir projeto";



        throw error;



      }



    }



  }


});
