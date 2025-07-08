<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { usePositionStore } from '../../stores/positions';
import type { Position } from '../../types/position';
import DetailEditor from '../../components/DetailEditor.vue';
import { VueDraggableNext } from 'vue-draggable-next';

const route = useRoute();
const router = useRouter();
const positionStore = usePositionStore();
const position = ref<Position>();

onMounted(async () => {
  if (route.params.id) {
    const id = parseInt(route.params.id as string);
    const loadedPosition = positionStore.getPosition(id);
    if (loadedPosition) {
      position.value = loadedPosition;
    }
  }
});

const handleDelete = async () => {
  if (position.value && confirm('Are you sure you want to delete this position?')) {
    await positionStore.deletePosition(position.value.id);
    router.push('/positions');
  }
};

  
const updatePosition = async () => {
  if (position.value) {
    const updatedPosition = await positionStore.updatePosition(position.value.id, position.value);
    if (updatedPosition){
      position.value = updatedPosition
    } else {
      const loadedPosition = await positionStore.getPosition(position.value.id);
      if (loadedPosition) {
        position.value = loadedPosition;
      }
    }
  }
};

const addDetail = () => {
  if (position.value) {
    const newDetail = {
      id: Date.now(),
      name: '',
      description: {},
      tags: [],
      details: []
    };
    position.value.details.push(newDetail);
    updatePosition();
  }
};
</script>

<template>
  <div class="container mt-4" v-if="position">
    <h1>{{ position.name }}</h1>
    <div class="card mb-4">
      <div class="card-body">
        <h5 class="card-title">Position Details</h5>
        <p class="card-text">
          <strong>Start Date:</strong> {{ `${position.start_year}-${position.start_month}-${position.start_day}` }}
        </p>
        <p class="card-text">
          <strong>End Date:</strong> 
          {{ position.end_year ? `${position.end_year}-${position.end_month}-${position.end_day}` : 'Present' }}
        </p>
        <p class="card-text" v-if="position.salary">
          <strong>Salary:</strong> ${{ position.salary.toLocaleString() }}
        </p>
      </div>
    </div>

    <div class="card mb-4">
      <div class="card-body">
        <h5 class="card-title mb-4">Experience Details</h5>
        <VueDraggableNext
          v-model="position.details"
          group="details"
          @change="updatePosition"
        >
          <div v-if="typeof position !== 'undefined'">
            <div v-for="(detail, index) in position.details" :key="detail.id">
              <DetailEditor
                :detail="detail"
                @update:detail="(updatedDetail) => { if (position)
                  position.details[index] = updatedDetail; 
                  updatePosition()
                    ;}"
              />
            </div>
          </div>
        </VueDraggableNext>
        <button class="btn btn-success mt-3" @click="addDetail">
          Add Detail
        </button>
      </div>
    </div>

    <div class="mt-3">
      <router-link :to="`/positions/${position.id}/edit`" class="btn btn-primary me-2">Edit</router-link>
      <button @click="handleDelete" class="btn btn-danger me-2">Delete</button>
      <router-link to="/positions" class="btn btn-secondary">Back to List</router-link>
    </div>
  </div>
</template>