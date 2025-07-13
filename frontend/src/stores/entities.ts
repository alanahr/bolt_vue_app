import { defineStore } from 'pinia';
import { ref } from 'vue';
import type { Entity } from '../types';
import axios from 'axios';

const baseUrl = import.meta.env.VITE_BACKEND_URI;
const apiPort = import.meta.env.VITE_BACKEND_PORT;
const apiUrl = `http://${baseUrl}:${apiPort}/api`;

const api = axios.create({
  baseURL: apiUrl,
  timeout: 30000,
  headers: {
    'Content-type': 'application/json',
  }
});

export const useEntityStore = defineStore('entities', () => {
  const entities = ref<Entity[]>([]);

  async function addEntity(entity: Omit<Entity, 'id'>) {
    try {
      const response = await api.post('/entities', entity);
      const newEntity = response.data.data;
      entities.value.push(newEntity);
      return newEntity;
    } catch (error) {
      console.error('Error creating entity:', error);
      throw error;
    }
  }

  async function updateEntity(id: number, entity: Partial<Entity>) {
    try {
      const response = await api.put(`/entities/${id}`, entity);
      const updatedEntity = response.data.data;
      const index = entities.value.findIndex(e => e.id === id);
      if (index !== -1) {
        entities.value[index] = updatedEntity;
      }
      return updatedEntity;
    } catch (error) {
      console.error('Error updating entity:', error);
      throw error;
    }
  }

  async function deleteEntity(id: number) {
    try {
      await api.delete(`/entities/${id}`);
      const index = entities.value.findIndex(e => e.id === id);
      if (index !== -1) {
        entities.value.splice(index, 1);
      }
      return true;
    } catch (error) {
      console.error('Error deleting entity:', error);
      throw error;
    }
  }

  async function getEntity(id: number) {
    try {
      const response = await api.get(`/entities/${id}`);
      return response.data.data;
    } catch (error) {
      console.error('Error fetching entity:', error);
      throw error;
    }
  }

  async function getEntities() {
    try {
      const response = await api.get('/entities');
      entities.value = response.data.data;
      return entities.value;
    } catch (error) {
      console.error('Error fetching entities:', error);
      throw error;
    }
  }

  return {
    entities,
    addEntity,
    updateEntity,
    deleteEntity,
    getEntity,
    getEntities
  };
});