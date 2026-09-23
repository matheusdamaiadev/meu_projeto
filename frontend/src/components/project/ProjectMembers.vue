```vue
<template>
  <section class="members-section">
    <div class="section-header">
      <div>
        <h2>Membros</h2>
        <p>Gerencie quem participa deste projeto.</p>
      </div>

      <button v-if="canManage" class="add-button" @click="openAddModal">
        + Adicionar membro
      </button>
    </div>

    <div v-if="loading" class="state">Carregando membros...</div>

    <div v-else-if="error" class="state error">
      {{ error }}
    </div>

    <div v-else-if="members.length === 0" class="empty">
      <p>Nenhum membro neste projeto.</p>

      <button v-if="canManage" class="empty-button" @click="openAddModal">
        Adicionar primeiro membro
      </button>
    </div>

    <div v-else class="members-list">
      <div v-for="member in members" :key="member.id" class="member-card">
        <div class="member-avatar">
          {{ member.username?.charAt(0).toUpperCase() }}
        </div>

        <div class="member-info">
          <strong>{{ member.username }}</strong>

          <span class="role">
            {{ getRoleLabel(member.role) }}
          </span>
        </div>

        <div v-if="canManage" class="member-actions">
          <select
            :value="member.role"
            :disabled="processingMember === member.id"
            @change="changeRole(member, $event.target.value)"
          >
            <option value="viewer">Visualizador</option>
            <option value="admin">Administrador</option>
          </select>

          <button
            class="remove-button"
            :disabled="processingMember === member.id"
            @click="removeMember(member)"
          >
            Remover
          </button>
        </div>
      </div>
    </div>

    <!-- Modal adicionar membro -->
    <div v-if="showAddModal" class="modal-overlay" @click.self="closeAddModal">
      <div class="modal">
        <div class="modal-header">
          <div>
            <h3>Adicionar membro</h3>
            <p>Convide um dos seus amigos para o projeto.</p>
          </div>

          <button class="close-button" @click="closeAddModal">×</button>
        </div>

        <div v-if="friendsLoading" class="modal-state">Carregando amigos...</div>

        <div v-else-if="availableFriends.length === 0" class="modal-state">
          <p>Você não possui amigos disponíveis para adicionar.</p>
        </div>

        <div v-else>
          <div class="friends-list">
            <button
              v-for="friend in availableFriends"
              :key="friend.id"
              class="friend-option"
              :class="{ selected: selectedFriend?.id === friend.id }"
              @click="selectedFriend = friend"
            >
              <div class="friend-avatar">
                {{ friend.username?.charAt(0).toUpperCase() }}
              </div>

              <span>{{ friend.username }}</span>

              <span v-if="selectedFriend?.id === friend.id" class="check"> ✓ </span>
            </button>
          </div>

          <div class="role-field">
            <label>Função</label>

            <select v-model="selectedRole">
              <option value="viewer">Visualizador</option>
              <option value="admin">Administrador</option>
            </select>
          </div>

          <div v-if="modalError" class="modal-error">
            {{ modalError }}
          </div>

          <div v-if="modalSuccess" class="modal-success">
            {{ modalSuccess }}
          </div>

          <button
            class="invite-button"
            :disabled="!selectedFriend || inviting"
            @click="inviteMember"
          >
            {{ inviting ? "Enviando..." : "Enviar convite" }}
          </button>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { computed, ref, watch } from "vue";
import { useAuthStore } from "../../stores/auth";
import friendService from "../../services/friendService";
import {
  getProjectMembers,
  inviteProjectMember,
  updateProjectMember,
  removeProjectMember,
} from "../../services/projectService";

const props = defineProps({
  project: {
    type: Object,
    required: true,
  },
});

const authStore = useAuthStore();

const members = ref([]);
const loading = ref(false);
const error = ref("");

const showAddModal = ref(false);
const friends = ref([]);
const friendsLoading = ref(false);

const selectedFriend = ref(null);
const selectedRole = ref("viewer");

const inviting = ref(false);
const processingMember = ref(null);

const modalError = ref("");
const modalSuccess = ref("");

const currentUsername = computed(() => {
  return (
    authStore.user?.username ||
    authStore.user?.name ||
    localStorage.getItem("username") ||
    ""
  );
});

const isOwner = computed(() => {
  return props.project?.user === authStore.user?.id;
});

const canManage = computed(() => {
  if (isOwner.value) {
    return true;
  }

  return members.value.some(
    (member) => member.username === currentUsername.value && member.role === "admin"
  );
});

const availableFriends = computed(() => {
  const memberIds = new Set(members.value.map((member) => member.user));

  return friends.value.filter(
    (friend) => !memberIds.has(friend.friend) && friend.username !== currentUsername.value
  );
});

async function loadMembers() {
  if (!props.project?.id) return;

  loading.value = true;
  error.value = "";

  try {
    const response = await getProjectMembers(props.project.id);
    members.value = response.data;
  } catch (err) {
    console.error("Erro ao carregar membros:", err);

    error.value = err.response?.data?.detail || "Não foi possível carregar os membros.";
  } finally {
    loading.value = false;
  }
}

async function loadFriends() {
  friendsLoading.value = true;
  modalError.value = "";

  try {
    const response = await friendService.getFriends();
    friends.value = response;
  } catch (err) {
    console.error("Erro ao carregar amigos:", err);

    modalError.value =
      err.response?.data?.detail || "Não foi possível carregar seus amigos.";
  } finally {
    friendsLoading.value = false;
  }
}

async function openAddModal() {
  showAddModal.value = true;
  selectedFriend.value = null;
  selectedRole.value = "viewer";
  modalError.value = "";
  modalSuccess.value = "";

  await loadFriends();
}

function closeAddModal() {
  if (inviting.value) return;

  showAddModal.value = false;
  selectedFriend.value = null;
  modalError.value = "";
  modalSuccess.value = "";
}

async function inviteMember() {
  if (!selectedFriend.value || inviting.value) return;

  inviting.value = true;
  modalError.value = "";
  modalSuccess.value = "";

  try {
    await inviteProjectMember(
      props.project.id,
      selectedFriend.value.username,
      selectedRole.value
    );

    modalSuccess.value = "Convite enviado com sucesso.";

    selectedFriend.value = null;

    setTimeout(() => {
      if (showAddModal.value) {
        closeAddModal();
      }
    }, 800);
  } catch (err) {
    console.error("Erro ao enviar convite:", err);

    modalError.value = err.response?.data?.detail || "Não foi possível enviar o convite.";
  } finally {
    inviting.value = false;
  }
}

async function changeRole(member, role) {
  if (member.role === role) return;

  processingMember.value = member.id;

  try {
    const response = await updateProjectMember(props.project.id, member.id, role);

    const index = members.value.findIndex((item) => item.id === member.id);

    if (index !== -1) {
      members.value[index] = response.data;
    }
  } catch (err) {
    console.error("Erro ao alterar função:", err);

    alert(err.response?.data?.detail || "Não foi possível alterar a função.");
  } finally {
    processingMember.value = null;
  }
}

async function removeMember(member) {
  const confirmed = window.confirm(
    `Tem certeza que deseja remover ${member.username} do projeto?`
  );

  if (!confirmed) return;

  processingMember.value = member.id;

  try {
    await removeProjectMember(props.project.id, member.id);

    members.value = members.value.filter((item) => item.id !== member.id);
  } catch (err) {
    console.error("Erro ao remover membro:", err);

    alert(err.response?.data?.detail || "Não foi possível remover o membro.");
  } finally {
    processingMember.value = null;
  }
}

function getRoleLabel(role) {
  if (role === "admin") {
    return "Administrador";
  }

  return "Visualizador";
}

watch(
  () => props.project?.id,
  async (id) => {
    if (id) {
      await loadMembers();
    }
  },
  { immediate: true }
);
</script>

<style scoped>
.members-section {
  margin-top: 32px;
  padding: 24px;
  background: #fff;
  border: 1px solid #e5e5e5;
  border-radius: 12px;
}

.section-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 20px;
  margin-bottom: 22px;
}

.section-header h2 {
  margin: 0;
  font-size: 20px;
  font-weight: 600;
  color: #111;
}

.section-header p {
  margin: 5px 0 0;
  font-size: 14px;
  color: #777;
}

.add-button,
.empty-button,
.invite-button {
  border: none;
  background: #111;
  color: #fff;
  cursor: pointer;
  border-radius: 8px;
  padding: 10px 14px;
  font-size: 14px;
  transition: opacity 0.2s;
}

.add-button:hover,
.empty-button:hover,
.invite-button:hover {
  opacity: 0.85;
}

.add-button:disabled,
.invite-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.members-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.member-card {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 13px;
  border: 1px solid #ededed;
  border-radius: 9px;
}

.member-avatar,
.friend-avatar {
  width: 38px;
  height: 38px;
  min-width: 38px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  background: #111;
  color: #fff;
  font-size: 14px;
  font-weight: 600;
}

.member-info {
  display: flex;
  flex-direction: column;
  gap: 3px;
  flex: 1;
  min-width: 0;
}

.member-info strong {
  font-size: 14px;
  color: #111;
}

.role {
  font-size: 12px;
  color: #888;
}

.member-actions {
  display: flex;
  align-items: center;
  gap: 8px;
}

.member-actions select,
.role-field select {
  border: 1px solid #ddd;
  border-radius: 7px;
  padding: 8px 10px;
  background: #fff;
  color: #222;
  font-size: 13px;
  outline: none;
}

.remove-button {
  border: 1px solid #ddd;
  background: #fff;
  color: #555;
  border-radius: 7px;
  padding: 8px 10px;
  font-size: 13px;
  cursor: pointer;
}

.remove-button:hover {
  border-color: #bbb;
  color: #111;
}

.remove-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.state,
.empty {
  padding: 30px 10px;
  text-align: center;
  color: #777;
  font-size: 14px;
}

.error,
.modal-error {
  color: #c62828;
}

.empty p {
  margin: 0 0 14px;
}

.empty-button {
  font-size: 13px;
}

.modal-overlay {
  position: fixed;
  inset: 0;
  z-index: 1000;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
  background: rgba(0, 0, 0, 0.45);
}

.modal {
  width: 100%;
  max-width: 480px;
  max-height: 85vh;
  overflow-y: auto;
  background: #fff;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 20px 50px rgba(0, 0, 0, 0.15);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  gap: 20px;
  margin-bottom: 20px;
}

.modal-header h3 {
  margin: 0;
  font-size: 18px;
  color: #111;
}

.modal-header p {
  margin: 5px 0 0;
  color: #777;
  font-size: 13px;
}

.close-button {
  width: 30px;
  height: 30px;
  border: none;
  background: transparent;
  color: #777;
  font-size: 25px;
  cursor: pointer;
}

.modal-state {
  padding: 25px 0;
  text-align: center;
  color: #777;
  font-size: 14px;
}

.friends-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-bottom: 20px;
}

.friend-option {
  width: 100%;
  display: flex;
  align-items: center;
  gap: 10px;
  border: 1px solid #e5e5e5;
  background: #fff;
  border-radius: 8px;
  padding: 10px;
  cursor: pointer;
  text-align: left;
}

.friend-option:hover {
  background: #fafafa;
}

.friend-option.selected {
  border-color: #111;
}

.friend-option span:nth-child(2) {
  flex: 1;
  font-size: 14px;
  color: #222;
}

.friend-avatar {
  width: 34px;
  height: 34px;
  min-width: 34px;
  font-size: 13px;
}

.check {
  font-size: 16px;
  color: #111;
}

.role-field {
  display: flex;
  flex-direction: column;
  gap: 7px;
  margin-bottom: 16px;
}

.role-field label {
  font-size: 13px;
  font-weight: 500;
  color: #333;
}

.role-field select {
  width: 100%;
}

.modal-error,
.modal-success {
  margin-bottom: 14px;
  padding: 10px;
  border-radius: 7px;
  font-size: 13px;
}

.modal-error {
  background: #fff4f4;
}

.modal-success {
  background: #f2faf4;
  color: #26733d;
}

.invite-button {
  width: 100%;
}

@media (max-width: 700px) {
  .members-section {
    padding: 18px;
  }

  .section-header {
    align-items: flex-start;
    flex-direction: column;
  }

  .add-button {
    width: 100%;
  }

  .member-card {
    align-items: flex-start;
    flex-wrap: wrap;
  }

  .member-actions {
    width: 100%;
    margin-left: 50px;
  }

  .member-actions select {
    flex: 1;
  }
}
</style>
