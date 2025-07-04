<template>
    <AppNavbar />
    
  <div class="container">
    <main class="container-fluid py-4">
      <div class="row">
            <AlertBar />
          </div>
        <router-view></router-view>

    </main>
     <AppFooter />
   
    
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