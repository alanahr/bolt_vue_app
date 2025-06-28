<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useEntityStore } from '../../stores/entities'
import type { Entity } from '../../types/entity';


const route = useRoute()
const router = useRouter()
const entitiesStore = useEntityStore()

const entity = ref<Entity>({
  id: 0,
  name: '',
  entity_type: 'tool',
  entity_parent: ''
});
  //ref<Comment[]>([])

onMounted(async () => {
  if (route.params.id) {
    const id = parseInt(route.params.id as string)
    const loadedEntity = await entitiesStore.getEntity(id)
    if (loadedEntity) {
      entity.value = loadedEntity
    }
  }
})

const handleSubmit = async () => {
  if (route.params.id) {
    await entitiesStore.updateEntity(parseInt(route.params.id as string), entity.value)
  } else {
    await entitiesStore.addEntity(entity.value)
  }
  router.push('/entities')
}
</script>

<template>
  <div class="container">
    <h2>{{ route.params.id ? 'Edit' : 'Create' }} Entity</h2>
    <form @submit.prevent="handleSubmit">
      <div class="mb-3">
        <label for="name" class="form-label">Name</label>
        <input type="text" class="form-control" id="name" v-model="entity.name" required>
      </div>
      <div class="mb-3">
        <label for="type" class="form-label">Type</label>
        <select class="form-select" id="type" v-model="entity.entity_type">
          <option value="company">Company</option>
          <option value="person">Person</option>
          <option value="skill">Skill</option>
          <option value="tool">Tool</option>
          <option value="other">Other</option>
        </select>
      </div>
      <button type="submit" class="btn btn-primary">Save</button>
      <router-link to="/entities" class="btn btn-secondary ms-2">Cancel</router-link>
    </form>
  </div>
</template>