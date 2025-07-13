import { defineStore } from 'pinia'
import { ref } from 'vue'

export interface AlertObject {
  status?: string | null
  message: string | null
}

export const useAlertsStore = defineStore('alerts', () => {
    const alerts = ref<AlertObject[]>([])
    
    function clearAlerts() {
        alerts.value = []
    }
    function addAlert(data: AlertObject){
        alerts.value.push(data)
    }
    function removeAlert(idx: number){
        alerts.value.splice(idx, 1);
    }
  return {
    alerts,
    clearAlerts,
    addAlert,
    removeAlert
  }
})