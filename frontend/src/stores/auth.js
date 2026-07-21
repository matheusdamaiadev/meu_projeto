import { defineStore } from "pinia";

import {
    login as loginService,
    register as registerService,
    getMe as getMeService
} from "../services/authService";


export const useAuthStore = defineStore(
    "auth",
    {

        state: () => ({
            access: localStorage.getItem("access"),
            refresh: localStorage.getItem("refresh"),
            user: null,
        }),


        getters: {

            isAuthenticated: (state) => {
                return !!state.access;
            },


            username: (state) => {
                return state.user?.username || "";
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


                await this.getMe();

            },



            async register(userData) {

                return await registerService(userData);

            },



            async getMe() {

                const data = await getMeService();

                this.user = data;

            },



            logout() {

                this.access = null;

                this.refresh = null;

                this.user = null;


                localStorage.removeItem("access");

                localStorage.removeItem("refresh");

            }

        }

    }
);