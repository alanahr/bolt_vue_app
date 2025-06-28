<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useEntityStore } from '../../stores/entities'
import type { Entity } from '../../types/entity'

const entitiesStore = useEntityStore()
const entities = ref<Entity[]>([]);

onMounted(async () => {
  entities.value = await entitiesStore.getEntities()
})
</script>

<template>
  <div class="container">
    <h2>Entities</h2>
    <div class="table-responsive">
      <table class="table">
        <thead>
          <tr>
            <th>ID</th>
            <th>Name</th>
            <th>Type</th>
            <th>Parent</th>
            <th>Color</th>
            <th>Icon</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="entity in entities" :key="entity.id">
            <td>{{ entity.id }}</td>
            <td>{{ entity.name }}</td>
            <td>{{ entity.entity_type }}</td>
            <td>{{ entity.entity_parent }}</td>
            <td>
              <span v-if="entity.color && !entity.icon">
                <div :style="`color:${entity.color};`">{{ entity.color }}</div>
              </span> 
            </td>
            <td>
              <span v-if="entity.icon && !entity.color">
                <i :title="`${entity.icon}`" :class="`${entity.icon}`"></i>
              </span> 
              <span v-if="entity.icon && entity.color">
                <i :style="`color:${entity.color};`" :title="`${entity.color} ${entity.icon}`" :class="`${entity.icon}`"></i>
              </span> 
            </td>
            <td>
              <router-link :to="`/entities/${entity.id}`" class="btn btn-sm btn-info me-2">View</router-link>
              <router-link :to="`/entities/${entity.id}/edit`" class="btn btn-sm btn-primary">Edit</router-link>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    <router-link to="/entities/new" class="btn btn-success">Create New Entity</router-link>
  </div>
</template>