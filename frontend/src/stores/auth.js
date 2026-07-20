import { defineStore } from "pinia";

import {
    login as loginService,
    register as registerService
} from "@/services/authService";


export const useAuthStore = defineStore(
    "auth",
    {

        state: () => ({
            access: localStorage.getItem("access"),
            refresh: localStorage.getItem("refresh"),
        }),


        getters: {

            isAuthenticated: (state) => {
                return !!state.access;
            }

        },


        actions: {


            async login(credentials) {

                const data = await loginService(credentials);


                this.access = data.access;
                this.refresh = data.refresh;


                localStorage.setItem(
                    "access",
                    data.access
                );


                localStorage.setItem(
                    "refresh",
                    data.refresh
                );

            },


            async register(userData) {

                return await registerService(userData);

            },


            logout() {

                this.access = null;
                this.refresh = null;


                localStorage.removeItem("access");
                localStorage.removeItem("refresh");

            }

        }

    }
);