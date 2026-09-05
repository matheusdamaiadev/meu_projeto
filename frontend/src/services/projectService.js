
import api from "./api";





export function getProjects(){


  return api.get("/projects/");


}







export function getProject(id){


  return api.get(

    `/projects/${id}/`

  );


}







export function createProject(data){


  return api.post(

    "/projects/",

    data

  );


}







export function updateProject(id,data){


  return api.put(

    `/projects/${id}/`,

    data

  );


}







export function patchProject(id,data){


  return api.patch(

    `/projects/${id}/`,

    data

  );


}







export function deleteProject(id){


  return api.delete(

    `/projects/${id}/`

  );


}
export function getProjectMembers(projectId) {
  return api.get(
    `/projects/${projectId}/members/`
  );
}

export function inviteProjectMember(projectId, username, role) {
  return api.post(
    `/projects/${projectId}/members/`,
    {
      username,
      role
    }
  );
}

export function updateProjectMember(projectId, memberId, role) {
  return api.patch(
    `/projects/${projectId}/members/${memberId}/`,
    {
      role
    }
  );
}

export function removeProjectMember(projectId, memberId) {
  return api.delete(
    `/projects/${projectId}/members/${memberId}/`
  );
}

