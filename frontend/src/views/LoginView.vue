<template>
  <div class="login-page">

    <div class="background-logo">

      <div class="logo-circle"></div>

      <h1>
        Momentum
      </h1>

    </div>


    <div class="login-card">


      <div class="header">

        <h2>
          Entre na sua conta
        </h2>


        <p>
          Gerencie seus projetos e tarefas em um só lugar.
        </p>

      </div>



      <form
        class="form"
        @submit.prevent="login"
      >


        <Input
          label="Email"
          placeholder="seu@email.com"
          v-model="email"
        />



        <Input
          label="Senha"
          type="password"
          placeholder="Digite sua senha"
          v-model="password"
        />


        <p
          v-if="error"
          class="error"
        >
          {{ error }}
        </p>



        <Button type="submit">
          Entrar
        </Button>


      </form>



      <p class="register">

        Ainda não possui uma conta?


        <RouterLink to="/register">
          Criar conta
        </RouterLink>


      </p>


    </div>


  </div>
</template>



<script setup>

import { ref } from 'vue'

import { RouterLink, useRouter } from 'vue-router'

import { useAuthStore } from '../stores/auth'

import Input from '../components/ui/Input.vue'
import Button from '../components/ui/Button.vue'


const email = ref('')
const password = ref('')

const error = ref('')


const router = useRouter()

const authStore = useAuthStore()



async function login() {

  error.value = ''


  try {

    await authStore.login({

      username: email.value,

      password: password.value

    })


    router.push('/dashboard')


  } catch (err) {

    console.error(err)

    error.value = 'Usuário ou senha incorretos'

  }

}

</script>



<style scoped>


.login-page {

  min-height: 100vh;


  background: #0f0f0f;


  display:flex;

  align-items:center;

  justify-content:center;


  padding:20px;


  position:relative;

}



.background-logo {

  position:absolute;


  top:35px;

  left:40px;


  display:flex;

  align-items:center;


  gap:12px;


  color:white;

}



.background-logo h1 {

  font-size:28px;

  font-weight:700;


  letter-spacing:-1px;

}



.logo-circle {

  width:16px;

  height:16px;


  background:white;


  border-radius:50%;

}




.login-card {

  width:420px;


  background:white;


  border-radius:24px;


  padding:40px;


  box-shadow:

    0 20px 60px rgba(0,0,0,.25);


  animation:show .4s ease;

}



@keyframes show {


  from {

    opacity:0;

    transform:translateY(20px);

  }


  to {

    opacity:1;

    transform:translateY(0);

  }


}




.header {

  text-align:center;


  margin-bottom:32px;

}



.header h2 {

  font-size:26px;


  font-weight:600;


  letter-spacing:-.5px;


  margin-bottom:10px;

}



.header p {

  color:#737373;


  font-size:14px;


  line-height:1.5;

}




.form {

  display:flex;


  flex-direction:column;


  gap:18px;

}



.error {

  color:#dc2626;

  text-align:center;

  font-size:14px;

}




.register {

  margin-top:30px;


  text-align:center;


  color:#737373;


  font-size:14px;

}



.register a {

  color:#111;


  font-weight:600;

}



</style>    