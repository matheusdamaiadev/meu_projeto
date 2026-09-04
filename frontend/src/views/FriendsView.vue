```vue
<template>
  <div class="friends-page">
    <!-- ========================================================
         AÇÕES
    ======================================================== -->

    <div class="friends-actions">
      <button class="add-button" @click="showAddFriend = !showAddFriend">
        <UserPlus :size="18" />

        Adicionar amigo
      </button>
    </div>

    <!-- ========================================================
         ADICIONAR AMIGO
    ======================================================== -->

    <section v-if="showAddFriend" class="add-friend-section">
      <div class="add-friend-box">
        <div class="add-friend-header">
          <div>
            <h2>Adicionar amigo</h2>

            <p>Pesquise pelo nome de usuário da pessoa.</p>
          </div>

          <button class="close-button" title="Fechar" @click="showAddFriend = false">
            <X :size="18" />
          </button>
        </div>

        <!-- PESQUISA DE NOVOS USUÁRIOS -->

        <div class="search-input-wrapper">
          <Search :size="17" />

          <input
            v-model="searchUsername"
            type="text"
            placeholder="Digite o nome de usuário..."
            @input="searchUsers"
          />
        </div>

        <!-- RESULTADOS -->

        <div v-if="searchUsername && searchResults.length > 0" class="search-results">
          <div v-for="user in searchResults" :key="user.id" class="search-result">
            <div class="user-avatar">
              {{ user.username.charAt(0).toUpperCase() }}
            </div>

            <div class="user-info">
              <strong>
                {{ user.username }}
              </strong>

              <span> Usuário do Momentum </span>
            </div>

            <!-- PENDENTE -->

            <button
              v-if="isRequestPending(user.username)"
              class="request-button pending"
              disabled
            >
              <Clock :size="16" />

              Pendente
            </button>

            <!-- AMIGO -->

            <button
              v-else-if="isFriend(user.username)"
              class="request-button pending"
              disabled
            >
              <Check :size="16" />

              Amigo
            </button>

            <!-- ADICIONAR -->

            <button
              v-else
              class="request-button"
              :disabled="sendingRequest"
              @click="sendRequest(user.username)"
            >
              <UserPlus :size="16" />

              Adicionar
            </button>
          </div>
        </div>

        <!-- NENHUM RESULTADO -->

        <div v-else-if="searchUsername && !searching" class="no-results">
          Nenhum usuário encontrado.
        </div>
      </div>
    </section>

    <!-- ========================================================
         CONVITES ENVIADOS
    ======================================================== -->

    <section
      v-if="pendingRequests.some((request) => request.status === 'pending')"
      class="requests-section"
    >
      <div class="section-header">
        <div>
          <h2>Convites enviados</h2>

          <p>Solicitações de amizade que ainda estão pendentes.</p>
        </div>

        <span class="section-count">
          {{ pendingRequests.filter((request) => request.status === "pending").length }}

          {{
            pendingRequests.filter((request) => request.status === "pending").length === 1
              ? "convite"
              : "convites"
          }}
        </span>
      </div>

      <div class="requests-list">
        <div
          v-for="request in pendingRequests.filter(
            (request) => request.status === 'pending'
          )"
          :key="request.id"
          class="request-card"
        >
          <div class="user-avatar">
            {{ request.username.charAt(0).toUpperCase() }}
          </div>

          <div class="user-info">
            <strong>
              {{ request.username }}
            </strong>

            <span> Solicitação enviada </span>
          </div>

          <div class="request-status">
            <Clock :size="15" />

            Pendente
          </div>
        </div>
      </div>
    </section>

    <!-- ========================================================
         AMIGOS
    ======================================================== -->

    <section class="friends-section">
      <div class="section-header">
        <div>
          <h2>Seus amigos</h2>

          <p>Pessoas que você adicionou ao Momentum.</p>
        </div>

        <span class="section-count">
          {{ friends.length }}

          {{ friends.length === 1 ? "amigo" : "amigos" }}
        </span>
      </div>

      <!-- CARREGANDO -->

      <div v-if="loading" class="empty-state loading-state">
        <div class="empty-icon">
          <Users :size="28" />
        </div>

        <h3>Carregando amigos...</h3>
      </div>

      <!-- LISTA DE AMIGOS -->

      <div v-else-if="filteredFriends.length > 0" class="friends-list">
        <FriendItem
          v-for="friend in filteredFriends"
          :key="friend.id"
          :friend="friend"
          :deleting="deletingFriend"
          @open-profile="openProfile"
          @delete="deleteFriend"
        />
      </div>

      <!-- NENHUM AMIGO ENCONTRADO PELA BUSCA -->

      <div
        v-else-if="friendStore.search.trim() && friends.length > 0"
        class="empty-state"
      >
        <div class="empty-icon">
          <Search :size="28" />
        </div>

        <h3>Nenhum amigo encontrado</h3>

        <p>Não encontramos nenhum amigo com o nome "{{ friendStore.search }}".</p>
      </div>

      <!-- ESTADO VAZIO -->

      <div v-else class="empty-state">
        <div class="empty-icon">
          <Users :size="28" />
        </div>

        <h3>Você ainda não tem amigos</h3>

        <p>Adicione amigos para poder convidá-los diretamente para seus projetos.</p>

        <button class="empty-button" @click="showAddFriend = true">
          <UserPlus :size="17" />

          Adicionar amigo
        </button>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import { useRouter } from "vue-router";

import { Users, UserPlus, Search, X, Clock, Check } from "lucide-vue-next";

import FriendService from "../services/FriendService";
import FriendItem from "../components/friends/FriendItem.vue";
import { useFriendStore } from "../stores/friend";

// ========================================================
// ROUTER
// ========================================================

const router = useRouter();

const friendStore = useFriendStore();

// ========================================================
// ESTADO
// ========================================================

const friends = ref([]);

const pendingRequests = ref([]);

const loading = ref(true);

const showAddFriend = ref(false);

// ========================================================
// BUSCA DE ADICIONAR AMIGO
// ========================================================
// Esta busca é independente da busca do Header.

const searchUsername = ref("");

const searchResults = ref([]);

const searching = ref(false);

const sendingRequest = ref(false);

const deletingFriend = ref(false);

// ========================================================
// FILTRAR AMIGOS
// ========================================================
// Esta é a busca usada pelo Header.
// Ela SOMENTE filtra os amigos que já existem.

const filteredFriends = computed(() => {
  const query = friendStore.search.trim().toLowerCase();

  if (!query) {
    return friends.value;
  }

  return friends.value.filter((friend) => friend.username.toLowerCase().includes(query));
});

// ========================================================
// CARREGAR AMIGOS
// ========================================================

const loadFriends = async () => {
  try {
    loading.value = true;

    friends.value = await FriendService.getFriends();
  } catch (error) {
    console.error("Erro ao carregar amigos:", error);
  } finally {
    loading.value = false;
  }
};

// ========================================================
// CARREGAR CONVITES ENVIADOS
// ========================================================

const loadPendingRequests = async () => {
  try {
    pendingRequests.value = await FriendService.getPendingRequests();
  } catch (error) {
    console.error("Erro ao carregar convites:", error);
  }
};

// ========================================================
// VERIFICAR SE JÁ É AMIGO
// ========================================================

const isFriend = (username) => {
  return friends.value.some((friend) => friend.username === username);
};

// ========================================================
// VERIFICAR SOLICITAÇÃO PENDENTE
// ========================================================

const isRequestPending = (username) => {
  return pendingRequests.value.some(
    (request) => request.username === username && request.status === "pending"
  );
};

// ========================================================
// PESQUISAR USUÁRIOS PARA ADICIONAR
// ========================================================

let searchTimeout = null;

const searchUsers = () => {
  clearTimeout(searchTimeout);

  searchResults.value = [];

  if (!searchUsername.value.trim()) {
    searching.value = false;

    return;
  }

  searchTimeout = setTimeout(async () => {
    try {
      searching.value = true;

      searchResults.value = await FriendService.searchFriends(
        searchUsername.value.trim()
      );
    } catch (error) {
      console.error("Erro ao pesquisar usuários:", error);

      searchResults.value = [];
    } finally {
      searching.value = false;
    }
  }, 300);
};

// ========================================================
// ENVIAR SOLICITAÇÃO
// ========================================================

const sendRequest = async (username) => {
  try {
    sendingRequest.value = true;

    const request = await FriendService.sendFriendRequest(username);

    pendingRequests.value.unshift(request);

    searchResults.value = searchResults.value.filter(
      (user) => user.username !== username
    );

    alert(`Solicitação enviada para ${username}.`);
  } catch (error) {
    console.error("Erro ao enviar solicitação:", error);

    const message =
      error.response?.data?.detail || "Não foi possível enviar a solicitação.";

    alert(message);
  } finally {
    sendingRequest.value = false;
  }
};

// ========================================================
// ABRIR PERFIL
// ========================================================

const openProfile = (friend) => {
  router.push({
    name: "profile",

    params: {
      username: friend.username,
    },
  });
};

// ========================================================
// EXCLUIR AMIZADE
// ========================================================

const deleteFriend = async (friend) => {
  const confirmed = confirm(
    `Tem certeza que deseja excluir ${friend.username} dos seus amigos?`
  );

  if (!confirmed) {
    return;
  }

  try {
    deletingFriend.value = true;

    await FriendService.deleteFriend(friend.id);

    friends.value = friends.value.filter((item) => item.id !== friend.id);

    searchResults.value = searchResults.value.filter(
      (user) => user.username !== friend.username
    );
  } catch (error) {
    console.error("Erro ao excluir amizade:", error);

    const message = error.response?.data?.detail || "Não foi possível excluir a amizade.";

    alert(message);
  } finally {
    deletingFriend.value = false;
  }
};

// ========================================================
// INICIALIZAÇÃO
// ========================================================

onMounted(async () => {
  await Promise.all([loadFriends(), loadPendingRequests()]);
});
</script>

<style scoped>
/* ========================================================
   PÁGINA
======================================================== */

.friends-page {
  width: 100%;

  max-width: 1100px;

  margin: 0 auto;

  padding: 40px;

  box-sizing: border-box;
}

/* ========================================================
   AÇÕES
======================================================== */

.friends-actions {
  display: flex;

  align-items: center;

  margin-bottom: 24px;
}

.add-button {
  display: flex;

  align-items: center;

  justify-content: center;

  gap: 9px;

  height: 40px;

  padding: 0 16px;

  border: 1px solid #111;

  border-radius: 9px;

  background: #111;

  color: white;

  font-size: 13px;

  font-weight: 500;

  cursor: pointer;

  transition: 0.2s;
}

.add-button:hover {
  background: #292929;

  border-color: #292929;
}

/* ========================================================
   ADICIONAR AMIGO
======================================================== */

.add-friend-section {
  width: 100%;

  margin-bottom: 32px;
}

.add-friend-box {
  width: 100%;

  padding: 22px;

  box-sizing: border-box;

  border: 1px solid #e5e5e5;

  border-radius: 14px;

  background: white;
}

.add-friend-header {
  display: flex;

  align-items: flex-start;

  justify-content: space-between;

  margin-bottom: 18px;
}

.add-friend-header h2 {
  margin: 0 0 5px 0;

  font-size: 16px;

  font-weight: 600;

  color: #111;
}

.add-friend-header p {
  margin: 0;

  color: #888;

  font-size: 13px;
}

.close-button {
  width: 32px;

  height: 32px;

  border: 0;

  border-radius: 8px;

  background: transparent;

  color: #777;

  display: flex;

  align-items: center;

  justify-content: center;

  cursor: pointer;

  transition: 0.2s;
}

.close-button:hover {
  background: #f3f3f3;

  color: #111;
}

/* ========================================================
   PESQUISA
======================================================== */

.search-input-wrapper {
  height: 42px;

  display: flex;

  align-items: center;

  gap: 10px;

  padding: 0 13px;

  box-sizing: border-box;

  border: 1px solid #ddd;

  border-radius: 9px;

  color: #888;

  transition: 0.2s;
}

.search-input-wrapper:focus-within {
  border-color: #aaa;
}

.search-input-wrapper input {
  width: 100%;

  border: 0;

  outline: none;

  background: transparent;

  color: #222;

  font-size: 13px;
}

/* ========================================================
   RESULTADOS
======================================================== */

.search-results {
  margin-top: 12px;

  border: 1px solid #e5e5e5;

  border-radius: 10px;

  overflow: hidden;
}

.search-result {
  display: flex;

  align-items: center;

  gap: 12px;

  padding: 12px 14px;

  border-bottom: 1px solid #eee;
}

.search-result:last-child {
  border-bottom: 0;
}

/* ========================================================
   AVATAR
======================================================== */

.user-avatar {
  width: 38px;

  height: 38px;

  flex-shrink: 0;

  border-radius: 50%;

  background: #f0f0f0;

  color: #333;

  display: flex;

  align-items: center;

  justify-content: center;

  font-size: 14px;

  font-weight: 600;

  text-transform: uppercase;
}

/* ========================================================
   INFORMAÇÕES
======================================================== */

.user-info {
  flex: 1;

  min-width: 0;

  display: flex;

  flex-direction: column;

  gap: 3px;
}

.user-info strong {
  overflow: hidden;

  white-space: nowrap;

  text-overflow: ellipsis;

  color: #222;

  font-size: 13px;

  font-weight: 600;
}

.user-info span {
  color: #999;

  font-size: 11px;
}

/* ========================================================
   BOTÃO DE SOLICITAÇÃO
======================================================== */

.request-button {
  display: flex;

  align-items: center;

  gap: 7px;

  height: 34px;

  padding: 0 12px;

  border: 1px solid #ddd;

  border-radius: 8px;

  background: white;

  color: #222;

  font-size: 12px;

  cursor: pointer;

  transition: 0.2s;
}

.request-button:hover {
  background: #f5f5f5;

  border-color: #ccc;
}

.request-button:disabled {
  opacity: 0.6;

  cursor: not-allowed;
}

.request-button.pending {
  background: #f5f5f5;

  color: #777;

  border-color: #e0e0e0;
}

/* ========================================================
   SEM RESULTADOS
======================================================== */

.no-results {
  padding: 18px;

  text-align: center;

  color: #999;

  font-size: 13px;
}

/* ========================================================
   SEÇÕES
======================================================== */

.requests-section,
.friends-section {
  width: 100%;

  margin-bottom: 36px;
}

.section-header {
  display: flex;

  align-items: center;

  justify-content: space-between;

  gap: 16px;

  margin-bottom: 16px;
}

.section-header h2 {
  margin: 0 0 4px 0;

  color: #111;

  font-size: 17px;

  font-weight: 600;
}

.section-header p {
  margin: 0;

  color: #999;

  font-size: 12px;
}

.section-count {
  flex-shrink: 0;

  color: #999;

  font-size: 12px;
}

/* ========================================================
   CONVITES
======================================================== */

.requests-list {
  display: flex;

  flex-direction: column;

  gap: 10px;
}

.request-card {
  display: flex;

  align-items: center;

  gap: 12px;

  padding: 14px 16px;

  border: 1px solid #e5e5e5;

  border-radius: 12px;

  background: white;
}

.request-status {
  display: flex;

  align-items: center;

  gap: 6px;

  padding: 6px 9px;

  border-radius: 7px;

  background: #f3f3f3;

  color: #666;

  font-size: 11px;

  font-weight: 500;
}

/* ========================================================
   LISTA DE AMIGOS
======================================================== */

.friends-list {
  display: grid;

  grid-template-columns: repeat(2, minmax(0, 1fr));

  gap: 12px;
}

/* ========================================================
   ESTADO VAZIO
======================================================== */

.empty-state {
  min-height: 360px;

  border: 1px solid #e5e5e5;

  border-radius: 14px;

  display: flex;

  flex-direction: column;

  align-items: center;

  justify-content: center;

  text-align: center;

  padding: 40px;

  box-sizing: border-box;
}

.loading-state {
  min-height: 260px;
}

.empty-icon {
  width: 58px;

  height: 58px;

  border-radius: 14px;

  background: #f3f3f3;

  color: #555;

  display: flex;

  align-items: center;

  justify-content: center;

  margin-bottom: 18px;
}

.empty-state h3 {
  margin: 0 0 8px 0;

  font-size: 16px;

  font-weight: 600;

  color: #222;
}

.empty-state p {
  max-width: 420px;

  margin: 0 0 22px 0;

  color: #888;

  font-size: 13px;

  line-height: 1.6;
}

.empty-button {
  display: flex;

  align-items: center;

  gap: 8px;

  height: 38px;

  padding: 0 15px;

  border: 1px solid #ddd;

  border-radius: 9px;

  background: white;

  color: #222;

  font-size: 13px;

  cursor: pointer;

  transition: 0.2s;
}

.empty-button:hover {
  background: #f5f5f5;

  border-color: #ccc;
}

/* ========================================================
   RESPONSIVO
======================================================== */

@media (max-width: 700px) {
  .friends-page {
    padding: 24px;
  }

  .friends-list {
    grid-template-columns: 1fr;
  }

  .search-result {
    align-items: flex-start;

    flex-wrap: wrap;
  }

  .request-button {
    margin-left: 50px;
  }

  .request-card {
    align-items: flex-start;

    flex-wrap: wrap;
  }

  .request-status {
    margin-left: 50px;
  }

  .section-header {
    align-items: flex-start;
  }
}

@media (max-width: 450px) {
  .friends-page {
    padding: 18px;
  }

  .add-button {
    width: 100%;
  }
}
</style>
