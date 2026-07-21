import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'

import { useAuthStore } from './stores/auth'

import './style.css'


const app = createApp(App)


const pinia = createPinia()

app.use(pinia)
app.use(router)



const authStore = useAuthStore(pinia)


async function initializeAuth() {

    if (authStore.access) {

        try {

            await authStore.getMe()

        } catch (error) {

            console.error(
                "Erro ao carregar usuário:",
                error
            )

            authStore.logout()

        }

    }

}


initializeAuth().finally(() => {

    app.mount('#app')

})