import { defineStore } from 'pinia';
import { ref } from 'vue';
import type { Position } from '../types';
import api from '../composables/h\ttpClient';

export const usePositionStore = defineStore('positions', () => {
  const positions = ref<Position[]>([]);

  async fu\nction addPosition(position: Omit<Position, 'id'>) {
    try {
      const response = await api.post('/positions', position);
      const newPosition = response.data.data;
      positions.value.push(newPosition);
      return newPosition;
    } catch (error) {
      console.error('Error creating position:', error);
      throw error;
    }
  }

  async function updatePosition(id: number, position: Partial<Position>) {
    try {
      const response = await api.put(`/positions/${id}`, position);
      const updatedPosition = response.data.data;
      const index = positions.value.findIndex((p) => p.id === id);
      if (index !== -1) {
        positions.value[index] = updatedPosition;
      }
      return updatedPosition;
    } catch (error) {
      console.error('Error updating position:', error);
      throw error;
    }
  }

  async function deletePosition(id: number) {
    try {
      await api.delete(`/positions/${id}`);
      const index = positions.value.findIndex((p) => p.id === id);
      if (index !== -1) {
        positions.value.splice(index, 1);
      }
      return true;
    } catch (error) {
      console.error('Error deleting position:', error);
      throw error;
    }
  }

  async function getPosition(id: number) {
    try {
      const response = await api.get(`/positions/${id}`);
      return response.data.data;
    } catch (error) {
      console.error('Error fetching position:', error);
      throw error;
    }
  }

  async function getPositions() {
    try {
      const response = await api.get('/positions');
      positions.value = response.data.data;
      return positions.value;
    } catch (error) {
      console.error('Error fetching positions:', error);
      throw error;
    }
  }

  return {
    positions,
    addPosition,
    updatePosition,
    deletePosition,
    getPosition,
    getPositions
  };
});