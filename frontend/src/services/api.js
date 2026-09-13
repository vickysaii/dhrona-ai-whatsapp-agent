import axios from 'axios'

let rawBase = (import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1').trim()

// Strip any trailing slashes
rawBase = rawBase.replace(/\/+$/, '')

// Automatically append /api/v1 if omitted in Vercel/hosting env
if (!rawBase.endsWith('/api/v1')) {
  rawBase = `${rawBase}/api/v1`
}

const api = axios.create({
  baseURL: rawBase,
  headers: { 'Content-Type': 'application/json' }
})

// Attach token to every request
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token')
  if (token) config.headers.Authorization = `Bearer ${token}`
  return config
})

// Handle 401 globally
api.interceptors.response.use(
  (res) => res,
  (err) => {
    if (err.response?.status === 401) {
      localStorage.removeItem('access_token')
      window.location.href = '/login'
    }
    return Promise.reject(err)
  }
)

export default api
