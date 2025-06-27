<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { usePositionStore } from '../../stores/positions';
import type { Position } from '../../types/position';

const positionStore = usePositionStore();
const positions = ref<Position[]>([]);

onMounted(async () => {
  positions.value = positionStore.getPositions();
});
</script>

<template>
  <div class="container mt-4">
    <h1>Positions</h1>
    <div class="table-responsive">
      <table class="table">
        <thead>
          <tr>
            <th>ID</th>
            <th>Name</th>
            <th>Start Date</th>
            <th>End Date</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="position in positions" :key="position.id">
            <td>{{ position.id }}</td>
            <td>{{ position.name }}</td>
            <td>{{ `${position.start_year}-${position.start_month}-${position.start_day}` }}</td>
            <td>{{ position.end_year ? `${position.end_year}-${position.end_month}-${position.end_day}` : 'Present' }}</td>
            <td>
              <router-link :to="`/positions/${position.id}`" class="btn btn-sm btn-info me-2">View</router-link>
              <router-link :to="`/positions/${position.id}/edit`" class="btn btn-sm btn-primary">Edit</router-link>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    <router-link to="/positions/new" class="btn btn-success">Add New Position</router-link>
  </div>
</template>