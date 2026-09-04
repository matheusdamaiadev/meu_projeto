```vue
<template>
  <div class="friend-item">
    <!-- PERFIL -->

    <button class="friend-content" @click="openProfile">
      <div class="user-avatar">
        {{ avatarLetter }}
      </div>

      <div class="friend-info">
        <span class="friend-username">
          {{ friend.username }}
        </span>

        <span class="friend-status"> Amigo </span>
      </div>
    </button>

    <!-- EXCLUIR -->

    <button class="delete-button" :disabled="deleting" @click.stop="handleDelete">
      <Trash2 :size="16" />
    </button>
  </div>
</template>

<script setup>
import { computed } from "vue";

import { Trash2 } from "lucide-vue-next";

const props = defineProps({
  friend: {
    type: Object,
    required: true,
  },

  deleting: {
    type: Boolean,
    default: false,
  },
});

const emit = defineEmits(["open-profile", "delete"]);

const avatarLetter = computed(() => {
  return props.friend.username?.charAt(0).toUpperCase() || "?";
});

function openProfile() {
  emit("open-profile", props.friend);
}

function handleDelete() {
  if (props.deleting) {
    return;
  }

  emit("delete", props.friend);
}
</script>

<style scoped>
/* =========================
   FRIEND ITEM
========================= */

.friend-item {
  display: flex;

  align-items: center;

  gap: 12px;

  width: 100%;

  max-width: 100%;

  box-sizing: border-box;

  padding: 12px 14px;

  border: 1px solid #e5e5e5;

  border-radius: 10px;

  background: #fff;

  overflow: hidden;

  transition: 0.2s ease;
}

.friend-item:hover {
  border-color: #000000;
}

/* =========================
   CONTEÚDO
========================= */

.friend-content {
  flex: 1;

  min-width: 0;

  width: 0;

  display: flex;

  align-items: center;

  gap: 12px;

  padding: 0;

  border: 0;

  background: transparent;

  color: inherit;

  text-align: left;

  cursor: pointer;

  overflow: hidden;
}

.friend-content:hover {
  background: transparent;
}

/* =========================
   AVATAR
========================= */

.user-avatar {
  width: 36px;

  height: 36px;

  flex-shrink: 0;

  display: flex;

  align-items: center;

  justify-content: center;

  border-radius: 50%;

  background: #111;

  color: #fff;

  font-size: 13px;

  font-weight: 600;

  text-transform: uppercase;
}

/* =========================
   INFORMAÇÕES
========================= */

.friend-info {
  flex: 1;

  min-width: 0;

  display: flex;

  flex-direction: column;

  align-items: flex-start;

  gap: 3px;

  overflow: hidden;
}

.friend-username {
  display: block;

  width: 100%;

  min-width: 0;

  overflow: hidden;

  white-space: nowrap;

  text-overflow: ellipsis;

  color: #222;

  font-size: 14px;

  font-weight: 500;
}

.friend-status {
  display: block;

  width: 100%;

  overflow: hidden;

  white-space: nowrap;

  text-overflow: ellipsis;

  color: #888;

  font-size: 12px;
}

/* =========================
   EXCLUIR
========================= */

.delete-button {
  min-width: 32px;

  height: 32px;

  flex-shrink: 0;

  display: flex;

  align-items: center;

  justify-content: center;

  padding: 0 8px;

  border: 1px solid transparent;

  border-radius: 8px;

  background: transparent;

  color: #dc2626;

  cursor: pointer;

  opacity: 0;

  transition: 0.2s ease;
}

.friend-item:hover .delete-button {
  opacity: 1;
}

.delete-button:hover {
  background: #fef2f2;

  border-color: #fecaca;
}

.delete-button:disabled {
  cursor: wait;

  opacity: 0.7;
}

/* =========================
   MOBILE
========================= */

@media (max-width: 600px) {
  .delete-button {
    opacity: 1;
  }
}
</style>
```
