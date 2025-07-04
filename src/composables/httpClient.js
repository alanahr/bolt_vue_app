import axios from 'axios'
import { useAlertsStore } from '../stores/alertStore'
// import { useLoadingWidgetStore } from '../stores/loadingWidgetStore'

const baseUrl = import.meta.env.VITE_BACKEND_URI
const apiPort = import.meta.env.VITE_BACKEND_PORT
const apiUrl = `http://${baseUrl}:${apiPort}`
const useToken = false

const alertStore = useAlertsStore()
//const isLoadingStore = useLoadingWidgetStore()

const api = axios.create({
  baseURL: apiUrl,
  //30 seconds
  timeout: 30000,
  headers: {
    'Content-type': 'application/json',
  }
})

// axios.defaults.headers.common = {
//   ...axios.defaults.headers.common,
//   Accept: '*/*',
//   'Content-Type': 'application/json',
//   'X-Content-Type-Options': 'nosniff',
//   'X-Frame-Options': 'sameorigin',
//   'Cache-Control': 'no-cache'
// }

//request
api.interceptors.request.use(
  config => {
    if (useToken){
      // Modify the request config (e.g., add headers)
      const token = localStorage.getItem('token');
      if (token) {
        config.headers.Authorization = `Bearer ${token}`;
      }
    }
    return config;
  },
  error => {
    // Handle request errors
    alertStore.addAlert(error)
    return Promise.reject(error);
  }
);

// Response interceptor
api.interceptors.response.use((response) => {
  // Handle the response here
  return response
}, (error) => {
  // Handle errors here
  alertStore.addAlert(error)
  console.error(error)
  return Promise.reject(error)
})

export default api
