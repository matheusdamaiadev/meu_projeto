import api from "./api";


export async function register(userData) {

    const response = await api.post(
        "/register/",
        userData
    );

    return response.data;

}



export async function login(credentials) {

    const response = await api.post(
        "/token/",
        credentials
    );

    return response.data;

}



export async function refreshToken(refresh) {

    const response = await api.post(
        "/token/refresh/",
        {
            refresh
        }
    );

    return response.data;

}



export async function getMe() {

    const response = await api.get(
        "/me/"
    );

    return response.data;

}