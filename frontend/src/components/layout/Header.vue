<template>
  <header class="header">

    <div class="page-info">
      <h1>{{ pageTitle }}</h1>
      <p>{{ pageDescription }}</p>
    </div>


    <div class="actions">

      <button class="icon-button">
        <Search :size="18" />
      </button>

      <button class="icon-button">
        <Bell :size="18" />
      </button>


      <div class="profile-wrapper">

        <button
          class="profile"
          @click="open = !open"
        >

          <div class="avatar">
            {{ userInitial }}
          </div>


          <div class="user-info">
            <strong>{{ username }}</strong>
            <span>Usuário</span>
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

import { ref, computed } from 'vue'
import { useRoute, useRouter, RouterLink } from 'vue-router'

import { useAuthStore } from '../../stores/auth'

import {
  Search,
  Bell,
  ChevronDown
} from 'lucide-vue-next'



const route = useRoute()

const router = useRouter()


const authStore = useAuthStore()


const open = ref(false)



const username = computed(() => {

  return authStore.user?.username || ''

})


const userInitial = computed(() => {

  return username.value
    ? username.value.charAt(0).toUpperCase()
    : 'U'

})



function logout() {

  authStore.logout()

  router.push('/login')

}



const pages = {

  dashboard: {
    title: 'Dashboard',
    description: 'Visão geral dos seus projetos'
  },

  projects: {
    title: 'Projetos',
    description: 'Gerencie todos os seus projetos'
  },

  project: {
    title: 'Projeto',
    description: 'Detalhes e tarefas do projeto'
  },

  profile: {
    title: 'Perfil',
    description: 'Informações da sua conta'
  },

  settings: {
    title: 'Configurações',
    description: 'Personalize sua experiência'
  }

}



const pageData = computed(() => {

  return pages[route.name] || {

    title: 'Momentum',

    description: ''

  }

})


const pageTitle = computed(() => pageData.value.title)


const pageDescription = computed(() => pageData.value.description)


</script>

<style scoped>

.header {

  height: 80px;

  background: white;

  border-bottom: 1px solid #e5e5e5;


  display: flex;

  align-items: center;

  justify-content: space-between;


  padding: 0 32px;

}


.page-info h1 {

  font-size: 24px;

  font-weight: 600;

}


.page-info p {

  color: #737373;

  font-size: 14px;

  margin-top: 4px;

}



.actions {

  display: flex;

  align-items: center;

  gap: 12px;

}


.icon-button {

  width: 40px;

  height: 40px;


  display: flex;

  justify-content: center;

  align-items: center;


  border-radius: 12px;

  border: 1px solid #e5e5e5;

  background:white;


  cursor:pointer;

}


.icon-button:hover {

  background:#f5f5f5;

}



.profile-wrapper {

  position:relative;

}



.profile {

  display:flex;

  align-items:center;

  gap:10px;


  background:none;

  border:none;

  cursor:pointer;

}



.avatar {

  width:42px;

  height:42px;


  border-radius:50%;


  background:#111;

  color:white;


  display:flex;

  align-items:center;

  justify-content:center;


  font-weight:600;

}



.user-info {

  display:flex;

  flex-direction:column;

  text-align:left;

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


  background:white;


  border:1px solid #e5e5e5;

  border-radius:14px;


  padding:8px;


  box-shadow:0 10px 30px rgba(0,0,0,.08);

}



.dropdown a,
.dropdown button {

  width:100%;

  display:block;


  padding:12px;


  border:none;

  background:none;


  text-align:left;

  border-radius:10px;


  cursor:pointer;
  transition: 0.2s ease-in-out;

}


.dropdown a:hover,
.dropdown button:hover {

  background:#f5f5f5;

}



.dropdown button:last-child:hover {

  background: #dc2626;

  color: white;

}

</style>