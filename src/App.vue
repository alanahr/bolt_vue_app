<template>
  <AppNavar />

  <div class="container">
    <router-view></router-view>
  </div>
</template>

<script setup lang="ts">
import AppNavbar from './components/layout/AppNavbar.vue'
import AppFooter from './components/layout/AppFooter.vue'
import AlertBar from './components/layout/AlertBar.vue';
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