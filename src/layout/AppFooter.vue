<template>
  <footer class="footer mt-auto py-3 bg-light">
    <div class="container-fluid text-center">
      <span class="text-muted">Employment History Tracker &copy; {{ currentYear }}</span>
    </div>
  </footer>
</template>

<script setup lang="ts">
import { computed } from 'vue'

const currentYear = computed(() => new Date().getFullYear())
</script>

<style scoped>
.footer {
  border-top: 1px solid #dee2e6;
}
</style>