import api from '@/services/APIService'

const BASE = '/leitor'

const leitorService = {
  // =========================
  // --- CEP (ViaCEP) ---
  // =========================
  cep: {
    consultar: async (cep) => {
      const response = await api.get(`${BASE}/cep/`, { params: { cep } })
      return response.data
    }
  },

  // =========================
  // --- RECOMPENSAS ---
  // =========================
  recompensas: {
    getAll: async (params = {}) => {
      const response = await api.get(`${BASE}/recompensas/`, { params })
      return response.data
    },
    getById: async (id) => {
      const response = await api.get(`${BASE}/recompensas/${id}/`)
      return response.data
    },
    create: async (data) => {
      const response = await api.post(`${BASE}/recompensas/`, data)
      return response.data
    },
    update: async (id, data) => {
      const response = await api.put(`${BASE}/recompensas/${id}/`, data)
      return response.data
    },
    delete: async (id) => {
      await api.delete(`${BASE}/recompensas/${id}/`)
    }
  },

  // =========================
  // --- LEITORES ---
  // =========================
  leitores: {
    getAll: async (params = {}) => {
      const response = await api.get(`${BASE}/leitores/`, { params })
      return response.data
    },
    getById: async (id) => {
      const response = await api.get(`${BASE}/leitores/${id}/`)
      return response.data
    },
    create: async (data) => {
      const response = await api.post(`${BASE}/leitores/`, data)
      return response.data
    },
    update: async (id, data) => {
      const response = await api.put(`${BASE}/leitores/${id}/`, data)
      return response.data
    },
    delete: async (id) => {
      await api.delete(`${BASE}/leitores/${id}/`)
    }
  },

  // =========================
  // --- EMPRÉSTIMOS ---
  // =========================
  emprestimos: {
    getAll: async (params = {}) => {
      const response = await api.get(`${BASE}/emprestimos/`, { params })
      return response.data
    },
    getById: async (id) => {
      const response = await api.get(`${BASE}/emprestimos/${id}/`)
      return response.data
    },
    create: async (data) => {
      const response = await api.post(`${BASE}/emprestimos/`, data)
      return response.data
    },
    update: async (id, data) => {
      const response = await api.put(`${BASE}/emprestimos/${id}/`, data)
      return response.data
    },
    delete: async (id) => {
      await api.delete(`${BASE}/emprestimos/${id}/`)
    }
  },

  // =========================
  // --- RESERVAS ---
  // =========================
  reservas: {
    getAll: async (params = {}) => {
      const response = await api.get(`${BASE}/reservas/`, { params })
      return response.data
    },
    getById: async (id) => {
      const response = await api.get(`${BASE}/reservas/${id}/`)
      return response.data
    },
    create: async (data) => {
      const response = await api.post(`${BASE}/reservas/`, data)
      return response.data
    },
    update: async (id, data) => {
      const response = await api.put(`${BASE}/reservas/${id}/`, data)
      return response.data
    },
    delete: async (id) => {
      await api.delete(`${BASE}/reservas/${id}/`)
    }
  }
}

export default leitorService
