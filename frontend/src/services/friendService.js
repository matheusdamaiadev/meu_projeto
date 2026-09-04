import api from './api';

const FriendService = {
  async getFriends() {
    const response = await api.get('/friends/');
    return response.data;
  },

  async searchFriends(username) {
    const response = await api.get('/friends/search/', {
      params: { username }
    });
    return response.data;
  },

  async sendFriendRequest(username) {
    const response = await api.post('/friends/request/', { username });
    return response.data;
  },

  async getPendingRequests() {
    const response = await api.get('/friends/pending/');
    return response.data;
  },

  async acceptFriendRequest(friendshipId) {
    const response = await api.post(`/friends/${friendshipId}/accept/`);
    return response.data;
  },

  async rejectFriendRequest(friendshipId) {
    const response = await api.post(`/friends/${friendshipId}/reject/`);
    return response.data;
  },

  async deleteFriend(friendshipId) {
    const response = await api.delete(`/friends/${friendshipId}/`);
    return response.data;
  }
};

export default FriendService;
