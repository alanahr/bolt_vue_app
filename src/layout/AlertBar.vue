<template>
  <span 
    v-for="(alert, index) in alerts" 
    :key="index"
  >
  <div>
    <div class="alert" :class="alert.status" role="alert">
        <button class="ml-2" @click.prevent="removeAlert(index)">X</button> {{ alert.message }} 
    </div>
  </div>
</span>
</template>

<script setup lang="ts">

import { computed } from 'vue'
import { useAlertsStore } from '../../stores/alertStore'

const alertStore = useAlertsStore()

const alerts = computed(() => {
  return alertStore.alerts
})

const removeAlert = (index: number) => {
  alertStore.removeAlert(index)
}

</script>