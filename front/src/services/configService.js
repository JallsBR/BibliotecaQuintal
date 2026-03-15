import api from '@/services/APIService'

const BASE = '/auth'

const configService = {
  groups: {
    getAll: async (params = {}) => {
      const response = await api.get(`${BASE}/groups/`, { params })
      return response.data
    },
    getById: async (id) => {
      const response = await api.get(`${BASE}/groups/${id}/`)
      return response.data
    },
    create: async (data) => {
      const response = await api.post(`${BASE}/groups/`, data)
      return response.data
    },
    update: async (id, data) => {
      const response = await api.put(`${BASE}/groups/${id}/`, data)
      return response.data
    },
    delete: async (id) => {
      await api.delete(`${BASE}/groups/${id}/`)
    },
    getUsers: async (groupId) => {
      const response = await api.get(`${BASE}/groups/${groupId}/users/`)
      return response.data
    },
    setUsers: async (groupId, userIds) => {
      const response = await api.put(`${BASE}/groups/${groupId}/users/`, { user_ids: userIds })
      return response.data
    }
  },
  permissions: {
    getAll: async () => {
      const response = await api.get(`${BASE}/permissions/`)
      return response.data
    }
  },
  users: {
    getAll: async (params = {}) => {
      const response = await api.get(`${BASE}/users/`, { params })
      return response.data
    },
    getById: async (id) => {
      const response = await api.get(`${BASE}/users/${id}/`)
      return response.data
    },
    update: async (id, data) => {
      const response = await api.patch(`${BASE}/users/${id}/`, data)
      return response.data
    }
  }
}

export default configService
