```vue
<template>

  <header class="header">

    <div class="page-info">

      <h1>
        {{ pageTitle }}
      </h1>

      <p>
        {{ pageDescription }}
      </p>

    </div>


    <div class="actions">


      <!-- PESQUISA -->

      <div
        v-if="searchOpen"
        class="search-box"
      >

        <Search :size="17" />

        <input
          ref="searchInput"
          v-model="projectStore.search"
          type="text"
          placeholder="Buscar projetos..."
        />

        <button
          class="close-search"
          @click="closeSearch"
        >

          ×

        </button>

      </div>


      <button
        v-else
        class="icon-button"
        title="Pesquisar"
        @click="openSearch"
      >

        <Search :size="18" />

      </button>


      <!-- NOTIFICAÇÕES -->

      <button
        class="icon-button"
        title="Notificações"
      >

        <Bell :size="18" />

      </button>


      <!-- PERFIL -->

      <div class="profile-wrapper">

        <button
          class="profile"
          @click="open = !open"
        >

          <div class="avatar">

            {{ userInitial }}

          </div>


          <div class="user-info">

            <strong>
              {{ username }}
            </strong>

            <span>
              Usuário
            </span>

          </div>


          <ChevronDown :size="16" />

        </button>


        <div
          v-if="open"
          class="dropdown"
        >

          <RouterLink to="/profile">

            Meu Perfil

          </RouterLink>


          <RouterLink to="/settings">

            Configurações

          </RouterLink>


          <button @click="logout">

            Sair

          </button>

        </div>

      </div>

    </div>

  </header>

</template>


<script setup>

import {
  ref,
  computed,
  nextTick
} from "vue";


import {
  useRoute,
  useRouter,
  RouterLink
} from "vue-router";


import {
  Search,
  Bell,
  ChevronDown
} from "lucide-vue-next";


import { useAuthStore } from "../../stores/auth";


import { useProjectStore } from "../../stores/project";


const route = useRoute();

const router = useRouter();


const authStore = useAuthStore();

const projectStore = useProjectStore();


const open = ref(false);

const searchOpen = ref(false);

const searchInput = ref(null);


const username = computed(() => {

  return authStore.user?.username || "";

});


const userInitial = computed(() => {

  return username.value

    ? username.value
        .charAt(0)
        .toUpperCase()

    : "U";

});


function openSearch() {

  searchOpen.value = true;


  nextTick(() => {

    searchInput.value?.focus();

  });

}


function closeSearch() {

  searchOpen.value = false;

  projectStore.search = "";

}


function logout() {

  authStore.logout();

  router.push("/login");

}


const pages = {

  dashboard: {

    title: "Dashboard",

    description: "Visão geral dos seus projetos"

  },


  projects: {

    title: "Projetos",

    description: "Gerencie todos os seus projetos"

  },


  project: {

    title: "Projeto",

    description: "Detalhes e tarefas do projeto"

  },


  profile: {

    title: "Perfil",

    description: "Informações da sua conta"

  },


  settings: {

    title: "Configurações",

    description: "Personalize sua experiência"

  }

};


const pageData = computed(() => {

  return pages[route.name] || {

    title: "Momentum",

    description: ""

  };

});


const pageTitle = computed(() => {

  return pageData.value.title;

});


const pageDescription = computed(() => {

  return pageData.value.description;

});

</script>


<style scoped>

.header {

  height:80px;

  background:white;

  border-bottom:1px solid #e5e5e5;

  display:flex;

  align-items:center;

  justify-content:space-between;

  padding:0 32px;

}


.page-info h1 {

  margin:0;

  font-size:24px;

  font-weight:600;

}


.page-info p {

  margin-top:4px;

  color:#737373;

  font-size:14px;

}


.actions {

  display:flex;

  align-items:center;

  gap:12px;

}


/* PESQUISA */

.search-box {

  width:260px;

  height:40px;

  display:flex;

  align-items:center;

  gap:9px;

  padding:0 10px 0 13px;

  border:1px solid #d4d4d4;

  border-radius:12px;

  background:white;

  color:#737373;

  box-sizing:border-box;

  transition:.2s ease;

}


.search-box:focus-within {

  border-color:#111;

  box-shadow:0 0 0 3px rgba(0,0,0,.05);

}


.search-box input {

  flex:1;

  min-width:0;

  border:none;

  outline:none;

  background:transparent;

  color:#111;

  font-size:14px;

}


.search-box input::placeholder {

  color:#999;

}


.close-search {

  width:24px;

  height:24px;

  display:flex;

  align-items:center;

  justify-content:center;

  border:none;

  border-radius:6px;

  background:transparent;

  color:#777;

  cursor:pointer;

  font-size:18px;

  line-height:1;

}


.close-search:hover {

  background:#f5f5f5;

  color:#111;

}


/* BOTÕES */

.icon-button {

  width:40px;

  height:40px;

  display:flex;

  align-items:center;

  justify-content:center;

  border:1px solid #e5e5e5;

  border-radius:12px;

  background:white;

  cursor:pointer;

}


.icon-button:hover {

  background:#f5f5f5;

}


/* PERFIL */

.profile-wrapper {

  position:relative;

}


.profile {

  display:flex;

  align-items:center;

  gap:10px;

  border:none;

  background:none;

  cursor:pointer;

}


.avatar {

  width:42px;

  height:42px;

  display:flex;

  align-items:center;

  justify-content:center;

  border-radius:50%;

  background:#111;

  color:white;

  font-weight:600;

}


.user-info {

  display:flex;

  flex-direction:column;

  text-align:left;

}


.user-info strong {

  font-size:14px;

}


.user-info span {

  font-size:12px;

  color:#777;

}


.dropdown {

  position:absolute;

  right:0;

  top:55px;

  width:200px;

  padding:8px;

  border:1px solid #e5e5e5;

  border-radius:14px;

  background:white;

  box-shadow:0 10px 30px rgba(0,0,0,.08);

  z-index:10;

}


.dropdown a,
.dropdown button {

  width:100%;

  display:block;

  padding:12px;

  border:none;

  border-radius:10px;

  background:none;

  text-align:left;

  cursor:pointer;

  transition:.2s ease-in-out;

}


.dropdown a:hover,
.dropdown button:hover {

  background:#f5f5f5;

}


.dropdown button:last-child:hover {

  background:#dc2626;

  color:white;

}

</style>
```
