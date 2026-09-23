```vue
<template>
  <div class="notifications-page">
    <div v-if="notificationsLoading" class="notification-empty">Carregando...</div>

    <div v-else-if="notifications.length === 0" class="notification-empty">
      <Bell :size="28" />

      <span>Nenhuma notificação.</span>
    </div>

    <div v-else class="notification-list">
      <div
        v-for="notification in notifications"
        :key="notification.id"
        class="notification-item"
        :class="{ unread: !notification.read }"
      >
        <!-- AMIZADE -->

        <template v-if="notification.type === 'friend_request'">
          <div class="notification-icon">
            <UserPlus :size="18" />
          </div>

          <div class="notification-content">
            <strong>Nova solicitação de amizade</strong>

            <p>
              {{ notification.sender_username }}
              quer adicionar você como amigo.
            </p>

            <div
              v-if="!notification.read && !notification.accepted"
              class="notification-actions"
            >
              <button
                class="accept-button"
                :disabled="processingNotification === notification.id"
                @click="acceptFriend(notification)"
              >
                Aceitar
              </button>

              <button
                class="reject-button"
                :disabled="processingNotification === notification.id"
                @click="rejectFriend(notification)"
              >
                Recusar
              </button>
            </div>
          </div>
        </template>

        <!-- PROJETO -->

        <template v-else-if="notification.type === 'project_invite'">
          <div class="notification-icon">
            <Folder :size="18" />
          </div>

          <div class="notification-content">
            <strong>Convite para projeto</strong>

            <p>
              {{ notification.sender_username }}
              convidou você para
              <strong class="project-name">
                {{ notification.project_name }} </strong
              >.
            </p>

            <p v-if="notification.role" class="project-role">
              Função:
              {{ notification.role === "admin" ? "Administrador" : "Visualizador" }}
            </p>

            <div
              v-if="!notification.read && !notification.accepted"
              class="notification-actions"
            >
              <button
                class="accept-button"
                :disabled="processingNotification === notification.id"
                @click="acceptProjectInvite(notification)"
              >
                Aceitar
              </button>

              <button
                class="reject-button"
                :disabled="processingNotification === notification.id"
                @click="rejectProjectInvite(notification)"
              >
                Recusar
              </button>
            </div>
          </div>
        </template>

        <!-- OUTRA NOTIFICAÇÃO -->

        <template v-else>
          <div class="notification-icon">
            <Bell :size="18" />
          </div>

          <div class="notification-content">
            <strong>Notificação</strong>
          </div>
        </template>
      </div>
    </div>
  </div>
</template> 

<script setup>
import { ref, onMounted } from "vue";

import { Bell, UserPlus, Folder } from "lucide-vue-next";

import FriendService from "../services/friendService";
import NotificationService from "../services/NotificationService";

// ========================================================
// ESTADO
// ========================================================

const notifications = ref([]);

const notificationsLoading = ref(false);

const processingNotification = ref(null);

// ========================================================
// CARREGAR NOTIFICAÇÕES
// ========================================================

const loadNotifications = async () => {
  try {
    notificationsLoading.value = true;

    notifications.value = await NotificationService.getNotifications();
  } catch (error) {
    console.error("Erro ao carregar notificações:", error);
  } finally {
    notificationsLoading.value = false;
  }
};

// ========================================================
// ACEITAR AMIZADE
// ========================================================

const acceptFriend = async (notification) => {
  if (!notification.friendship_id) {
    alert("Não foi possível identificar a solicitação.");

    return;
  }

  try {
    processingNotification.value = notification.id;

    await FriendService.acceptFriendRequest(notification.friendship_id);

    notification.read = true;
    notification.accepted = true;

    alert(`Agora você e ${notification.sender_username} são amigos.`);
  } catch (error) {
    console.error("Erro ao aceitar solicitação:", error);

    alert(error.response?.data?.detail || "Não foi possível aceitar a solicitação.");
  } finally {
    processingNotification.value = null;
  }
};

// ========================================================
// RECUSAR AMIZADE
// ========================================================

const rejectFriend = async (notification) => {
  if (!notification.friendship_id) {
    alert("Não foi possível identificar a solicitação.");

    return;
  }

  try {
    processingNotification.value = notification.id;

    await FriendService.rejectFriendRequest(notification.friendship_id);

    notification.read = true;

    alert("Solicitação recusada.");
  } catch (error) {
    console.error("Erro ao recusar solicitação:", error);

    alert(error.response?.data?.detail || "Não foi possível recusar a solicitação.");
  } finally {
    processingNotification.value = null;
  }
};

// ========================================================
// ACEITAR CONVITE DE PROJETO
// ========================================================

const acceptProjectInvite = async (notification) => {
  try {
    processingNotification.value = notification.id;

    await NotificationService.respondToProjectInvite(notification.id, "accept");

    notification.read = true;
    notification.accepted = true;

    alert(`Você entrou no projeto ${notification.project_name}.`);
  } catch (error) {
    console.error("Erro ao aceitar convite:", error);

    alert(error.response?.data?.detail || "Não foi possível aceitar o convite.");
  } finally {
    processingNotification.value = null;
  }
};

// ========================================================
// RECUSAR CONVITE DE PROJETO
// ========================================================

const rejectProjectInvite = async (notification) => {
  try {
    processingNotification.value = notification.id;

    await NotificationService.respondToProjectInvite(notification.id, "reject");

    notification.read = true;
    notification.accepted = false;

    alert("Convite recusado.");
  } catch (error) {
    console.error("Erro ao recusar convite:", error);

    alert(error.response?.data?.detail || "Não foi possível recusar o convite.");
  } finally {
    processingNotification.value = null;
  }
};

// ========================================================
// INICIALIZAÇÃO
// ========================================================

onMounted(() => {
  loadNotifications();
});
</script>

<style scoped>
.notifications-page {
  width: 100%;

  max-width: 900px;

  margin: 0 auto;
}

/* ========================================================
   LISTA
======================================================== */

.notification-list {
  display: flex;

  flex-direction: column;

  gap: 10px;
}

.notification-item {
  display: flex;

  gap: 14px;

  padding: 16px;

  border: 1px solid #e5e5e5;

  border-radius: 10px;

  background: white;

  transition: 0.2s ease;
}

.notification-item:hover {
  border-color: #000;
}

.notification-item.unread {
  background: #fafafa;
}

/* ========================================================
   ÍCONE
======================================================== */

.notification-icon {
  width: 38px;

  height: 38px;

  flex-shrink: 0;

  display: flex;

  align-items: center;

  justify-content: center;

  border-radius: 9px;

  background: #f0f0f0;

  color: #333;
}

/* ========================================================
   CONTEÚDO
======================================================== */

.notification-content {
  flex: 1;

  min-width: 0;
}

.notification-content strong {
  display: block;

  margin-bottom: 5px;

  color: #222;

  font-size: 14px;

  font-weight: 600;
}

.notification-content p {
  margin: 0;

  color: #777;

  font-size: 13px;

  line-height: 1.5;
}

.notification-content .project-name {
  display: inline;

  margin: 0;

  color: #333;

  font-size: inherit;

  font-weight: 600;
}

.project-role {
  margin-top: 5px !important;

  font-size: 12px !important;

  color: #999 !important;
}

/* ========================================================
   AÇÕES
======================================================== */

.notification-actions {
  display: flex;

  gap: 8px;

  margin-top: 12px;
}

.accept-button,
.reject-button {
  height: 32px;

  padding: 0 13px;

  border-radius: 7px;

  font-size: 12px;

  cursor: pointer;

  transition: 0.2s ease;
}

.accept-button {
  border: 1px solid #111;

  background: #111;

  color: white;
}

.accept-button:hover {
  background: #333;
}

.reject-button {
  border: 1px solid #ddd;

  background: white;

  color: #444;
}

.reject-button:hover {
  background: #f3f3f3;
}

.accept-button:disabled,
.reject-button:disabled {
  opacity: 0.5;

  cursor: not-allowed;
}

/* ========================================================
   ESTADO VAZIO
======================================================== */

.notification-empty {
  min-height: 240px;

  display: flex;

  flex-direction: column;

  align-items: center;

  justify-content: center;

  gap: 10px;

  border: 1px solid #e5e5e5;

  border-radius: 10px;

  color: #999;

  font-size: 13px;
}
</style>
```
