<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { usePositionStore } from '../../stores/positions';
import type { Position } from '../../types/position';

const route = useRoute();
const router = useRouter();
const positionStore = usePositionStore();

const position = ref<Partial<Position>>({
  name: '',
  start_year: new Date().getFullYear(),
  start_month: new Date().getMonth() + 1,
  start_day: new Date().getDate(),
  salary: 0,
  details: []
});

const isEdit = route.params.id !== undefined;

onMounted(async () => {
  if (isEdit && route.params.id) {
    const loadedPosition = positionStore.getPosition(parseInt(route.params.id as string));
    if (loadedPosition) {
      position.value = { ...loadedPosition };
    }
  }
});

const handleSubmit = async () => {
  if (isEdit && route.params.id) {
    await positionStore.updatePosition(parseInt(route.params.id as string), position.value);
  } else {
    await positionStore.addPosition(position.value as Omit<Position, 'id'>);
  }
  router.push('/positions');
};
</script>

<template>
  <div class="container mt-4">
    <h1>{{ isEdit ? 'Edit Position' : 'New Position' }}</h1>
    <form @submit.prevent="handleSubmit">
      <div class="mb-3">
        <label for="name" class="form-label">Position Title</label>
        <input
          type="text"
          class="form-control"
          id="name"
          v-model="position.name"
          required
        >
      </div>
      
      <div class="row">
        <div class="col-md-4 mb-3">
          <label for="start_year" class="form-label">Start Year</label>
          <input
            type="number"
            class="form-control"
            id="start_year"
            v-model="position.start_year"
            required
          >
        </div>
        <div class="col-md-4 mb-3">
          <label for="start_month" class="form-label">Start Month</label>
          <input
            type="number"
            class="form-control"
            id="start_month"
            v-model="position.start_month"
            min="1"
            max="12"
            required
          >
        </div>
        <div class="col-md-4 mb-3">
          <label for="start_day" class="form-label">Start Day</label>
          <input
            type="number"
            class="form-control"
            id="start_day"
            v-model="position.start_day"
            min="1"
            max="31"
            required
          >
        </div>
      </div>

      <div class="row">
        <div class="col-md-4 mb-3">
          <label for="end_year" class="form-label">End Year</label>
          <input
            type="number"
            class="form-control"
            id="end_year"
            v-model="position.end_year"
          >
        </div>
        <div class="col-md-4 mb-3">
          <label for="end_month" class="form-label">End Month</label>
          <input
            type="number"
            class="form-control"
            id="end_month"
            v-model="position.end_month"
            min="1"
            max="12"
          >
        </div>
        <div class="col-md-4 mb-3">
          <label for="end_day" class="form-label">End Day</label>
          <input
            type="number"
            class="form-control"
            id="end_day"
            v-model="position.end_day"
            min="1"
            max="31"
          >
        </div>
      </div>

      <div class="mb-3">
        <label for="salary" class="form-label">Salary</label>
        <input
          type="number"
          class="form-control"
          id="salary"
          v-model="position.salary"
        >
      </div>

      <div class="mb-3">
        <button type="submit" class="btn btn-primary me-2">Save</button>
        <router-link to="/positions" class="btn btn-secondary">Cancel</router-link>
      </div>
    </form>
  </div>
</template>