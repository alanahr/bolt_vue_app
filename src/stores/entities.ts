import { defineStore } from 'pinia';
import { ref } from 'vue';
import type { Entity } from '../types';



export const useEntityStore = defineStore('entities', () => {
  const entities = ref<Entity[]>([]);
  
let nextTagId = 1;

const tagData = [
  {id: nextTagId++, name:"agile", entity_type:"skill", color:"", icon:"", entity_parent: null },
  {id: nextTagId++, name:"QA", entity_type:"skill" },
                                {id:nextTagId++, name:"SDET", entity_type:"skill" },
                                {id:nextTagId++, name:"TestRail", entity_type:"tool" },
  {id:nextTagId++, name:"ArcGIS", entity_type:"tool" },
                                {id:nextTagId++, "name":"GIS", entity_type:"skill" }
]
  entities.value = tagData;
  let nextId = 1;

  function addEntity(entity: Omit<Entity, 'id'>) {
    const newEntity = { ...entity, id: nextId++ };
    entities.value.push(newEntity);
    return newEntity;
  }

  function updateEntity(id: number, entity: Partial<Entity>) {
    const index = entities.value.findIndex(e => e.id === id);
    if (index !== -1) {
      entities.value[index] = { ...entities.value[index], ...entity };
      return entities.value[index];
    }
    return null;
  }

  function deleteEntity(id: number) {
    const index = entities.value.findIndex(e => e.id === id);
    if (index !== -1) {
      entities.value.splice(index, 1);
      return true;
    }
    return false;
  }

  function getEntity(id: number) {
    return entities.value.find(e => e.id === id);
  }

  function getEntities() {
    return entities.value;
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