<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useEntityStore } from '../../stores/entities'
import type { Entity } from '../../types/entity'

const route = useRoute()
const router = useRouter()
const entitiesStore = useEntityStore()
const entity = ref<Entity>();



  
onMounted(async () => {
  if (route.params.id) {
    const id = parseInt(route.params.id as string)
    const loadedEntity = await entitiesStore.getEntity(id)
    if (loadedEntity) {
      entity.value = loadedEntity
    }
  }
 
})

const handleDelete = async () => {
  if (entity.value && confirm('Are you sure you want to delete this entity?')) {
    await entitiesStore.deleteEntity(entity.value.id)
    router.push('/entities')
  }
}
</script>

<template>
  <div class="container" v-if="entity">
    <h2>View Entity</h2>
    <div class="card">
      <div class="card-body">
        <h3>{{ entity.id }}: {{ entity.name }}</h3>
        <p><strong>Type:</strong> {{ entity.entity_type }}</p>
        <p><strong>Parent:</strong> {{ entity.entity_parent }}</p>
        <p><strong>Color:</strong> {{ entity.color }}</p>
        <p><strong>Icon:</strong> {{ entity.icon }}</p>
        
        <div class="mt-3">
          <router-link :to="`/entities/${entity.id}/edit`" class="btn btn-primary me-2">Edit</router-link>
          <button @click="handleDelete" class="btn btn-danger">Delete</button>
        </div>
      </div>
    </div>
  </div>
</template>