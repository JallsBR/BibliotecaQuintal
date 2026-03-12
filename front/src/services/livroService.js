import api from '@/services/APIService'

const BASE = '/livros'

const livroService = {
  // =========================
  // --- CATEGORIAS ---
  // =========================
  categorias: {
    getAll: async (params = {}) => {
      const response = await api.get(`${BASE}/categorias/`, { params })
      return response.data
    },
    getById: async (id) => {
      const response = await api.get(`${BASE}/categorias/${id}/`)
      return response.data
    },
    create: async (data) => {
      const response = await api.post(`${BASE}/categorias/`, data)
      return response.data
    },
    update: async (id, data) => {
      const response = await api.put(`${BASE}/categorias/${id}/`, data)
      return response.data
    },
    delete: async (id) => {
      await api.delete(`${BASE}/categorias/${id}/`)
    }
  },

  // =========================
  // --- AUTORES ---
  // =========================
  autores: {
    getAll: async (params = {}) => {
      const response = await api.get(`${BASE}/autores/`, { params })
      return response.data
    },
    getById: async (id) => {
      const response = await api.get(`${BASE}/autores/${id}/`)
      return response.data
    },
    create: async (data) => {
      const response = await api.post(`${BASE}/autores/`, data)
      return response.data
    },
    update: async (id, data) => {
      const response = await api.put(`${BASE}/autores/${id}/`, data)
      return response.data
    },
    delete: async (id) => {
      await api.delete(`${BASE}/autores/${id}/`)
    }
  },

  // =========================
  // --- EDITORAS ---
  // =========================
  editoras: {
    getAll: async (params = {}) => {
      const response = await api.get(`${BASE}/editoras/`, { params })
      return response.data
    },
    getById: async (id) => {
      const response = await api.get(`${BASE}/editoras/${id}/`)
      return response.data
    },
    create: async (data) => {
      const response = await api.post(`${BASE}/editoras/`, data)
      return response.data
    },
    update: async (id, data) => {
      const response = await api.put(`${BASE}/editoras/${id}/`, data)
      return response.data
    },
    delete: async (id) => {
      await api.delete(`${BASE}/editoras/${id}/`)
    }
  },

  // =========================
  // --- LIVROS ---
  // =========================
  livros: {
    getAll: async (params = {}) => {
      const response = await api.get(`${BASE}/livros/`, { params })
      return response.data
    },
    getById: async (id) => {
      const response = await api.get(`${BASE}/livros/${id}/`)
      return response.data
    },
    create: async (data) => {
      const response = await api.post(`${BASE}/livros/`, data)
      return response.data
    },
    /** Cria livro enviando imagem via FormData (multipart/form-data). */
    createWithFile: async (payload) => {
      const formData = new FormData()
      const file = payload.imagemFile
      if (file) {
        formData.append('imagem', file)
        delete payload.imagemFile
      }
      Object.entries(payload).forEach(([key, value]) => {
        if (value !== null && value !== undefined && value !== '') {
          formData.append(key, value === true || value === false ? value : value)
        }
      })
      const response = await api.post(`${BASE}/livros/`, formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      })
      return response.data
    },
    update: async (id, data) => {
      const response = await api.put(`${BASE}/livros/${id}/`, data)
      return response.data
    },
    delete: async (id) => {
      await api.delete(`${BASE}/livros/${id}/`)
    }
  }
}

export default livroService
