
import api from "./api";

const NotificationService = {
    async getNotifications() {
        const response = await api.get("/notifications/");
        return response.data;
    },

    async markAsRead(notificationId) {
        const response = await api.post(
            `/notifications/${notificationId}/read/`
        );

        return response.data;
    },

    async respondToProjectInvite(notificationId, action) {
        const response = await api.post(
            `/notifications/${notificationId}/project-invite/`,
            {
                action,
            }
        );

        return response.data;
    },
};

export default NotificationService;