import axios from 'axios'
import { useAlertsStore } from '../stores/alertStore'

const baseUrl = import.meta.env.VITE_BACKEND_URI
const apiPort = import.meta.env.VITE_BACKEND_PORT
const apiUrl = `http://${baseUrl}:${apiPort}/api`
const useToken = false

const alertStore = useAlertsStore()

const api = axios.create({
  baseURL: apiUrl,
  timeout: 30000,
  headers: {
    'Content-type': 'application/json',
  }
})

// Request interceptor
api.interceptors.request.use(
  config => {
    if (useToken){
      const token = localStorage.getItem('token');
      if (token) {
        config.headers.Authorization = `Bearer ${token}`;
      }
    }
    return config;
  },
  error => {
    alertStore.addAlert(error)
    return Promise.reject(error);
  }
)

// Response interceptor
api.interceptors.response.use((response) => {
  return response
}, (error) => {
  alertStore.addAlert(error)
  console.error(error)
  return Promise.reject(error)
})