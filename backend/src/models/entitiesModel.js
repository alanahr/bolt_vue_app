import { v4 as uuidv4 } from 'uuid';

// In-memory storage (replace with database in production)
let entities = [
  { id: 1, name: "agile", entity_type: "skill", color: "#40dae2", icon: "bi bi-backpack", entity_parent: null },
  { id: 2, name: "QA", entity_type: "skill", color: "", icon: "", entity_parent: null },
  { id: 3, name: "SDET", entity_type: "skill", color: "", icon: "", entity_parent: null },
  { id: 4, name: "TestRail", entity_type: "tool", color: "", icon: "", entity_parent: null },
  { id: 5, name: "ArcGIS", entity_type: "tool", color: "", icon: "", entity_parent: null },
  { id: 6, name: "GIS", entity_type: "skill", color: "", icon: "", entity_parent: null },
];

let nextId = 7;

export const findAll = async () => {
  return entities;
};

export const findById = async (id) => {
  return entities.find(e => e.id === id);
};

export const create = async (entityData) => {
  const newEntity = {
    id: nextId++,
    ...entityData,
    created_at: new Date().toISOString(),
    updated_at: new Date().toISOString(),
  };
  
  entities.push(newEntity);
  return newEntity;
};

export const update = async (id, entityData) => {
  const index = entities.findIndex(e => e.id === id);
  if (index === -1) return null;
  
  entities[index] = {
    ...entities[index],
    ...entityData,
    id, // Ensure ID doesn't change
    updated_at: new Date().toISOString(),
  };
  
  return entities[index];
};

export const remove = async (id) => {
  const index = entities.findIndex(e => e.id === id);
  if (index === -1) return false;
  
  entities.splice(index, 1);
  return true;
};