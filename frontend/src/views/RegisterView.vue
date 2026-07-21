<template>
  <div class="register-page">

    <div class="background-logo">

      <div class="logo-circle"></div>

      <h1>
        Momentum
      </h1>

    </div>


    <div class="register-card">


      <div class="header">

        <h2>
          Crie sua conta
        </h2>


        <p>
          Comece a organizar seus projetos hoje.
        </p>

      </div>



      <form
        class="form"
        @submit.prevent="register"
      >


        <Input
          label="Nome de usuário"
          placeholder="Digite seu nome"
          v-model="username"
        />



        <Input
          label="Email"
          placeholder="seu@email.com"
          v-model="email"
        />



        <Input
          label="Senha"
          type="password"
          placeholder="Crie uma senha"
          v-model="password"
        />



        <Input
          label="Confirmar senha"
          type="password"
          placeholder="Repita sua senha"
          v-model="confirmPassword"
        />


        <p
          v-if="error"
          class="error"
        >
          {{ error }}
        </p>


        <Button type="submit">
          Criar conta
        </Button>


      </form>



      <p class="login">

        Já possui uma conta?


        <RouterLink to="/login">
          Entrar
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


const username = ref('')
const email = ref('')
const password = ref('')
const confirmPassword = ref('')

const error = ref('')


const router = useRouter()

const authStore = useAuthStore()



async function register() {

  error.value = ''


  if (password.value !== confirmPassword.value) {

    error.value = 'As senhas não coincidem'

    return

  }


  try {

    await authStore.register({

      username: username.value,

      email: email.value,

      password: password.value

    })


    router.push('/login')


  } catch (err) {

    console.error(err)

    error.value = 'Erro ao criar conta'

  }

}

</script>



<style scoped>


.register-page {

  min-height:100vh;


  background:#0f0f0f;


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




.register-card {


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


  gap:16px;

}



.error {

  color:#dc2626;

  text-align:center;

  font-size:14px;

}



.login {


  margin-top:30px;


  text-align:center;


  color:#737373;


  font-size:14px;

}



.login a {


  color:#111;


  font-weight:600;

}


</style>