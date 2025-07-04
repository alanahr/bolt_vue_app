<template>
  <div class="app-container">
    <AppNavbar />
    
  <div class="container">
    <router-view></router-view>
  </div>
</template>

<script setup lang="ts">
import AppNavbar from './layout/AppNavbar.vue'
import AppFooter from './layout/AppFooter.vue'
import AlertBar from './layout/AlertBar.vue';
</script>

<style>
#app {
  width: 100%;
  max-width: none;
  margin: 0;
  padding: 0;
  text-align: left;
}
</style>