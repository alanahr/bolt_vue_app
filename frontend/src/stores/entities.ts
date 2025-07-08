@@ .. @@
 import { defineStore } from 'pinia';
 import { ref } from 'vue';
 import type { Entity } from '../types';
-
-
+import api from '../composables/httpClient';
 
 export const useEntityStore = defineStore('entities', () => {
   const entities = ref<Entity[]>([]);
-  
-let nextTagId = 1;
-
-  //#todo figure out if using objectid or number (new ObjectId())
-const tagData = [
-  {id: nextTagId++, name:"agile", entity_type:"skill", color:"#40dae2", icon:"bi bi-backpack", entity_parent: null },
-  {id: nextTagId++, name:"QA", entity_type:"skill", color:"", icon:"", entity_parent: null  },
-                                {id:nextTagId++, name:"SDET", entity_type:"skill", color:"", icon:"", entity_parent: null  },
-                                {id:nextTagId++, name:"TestRail", entity_type:"tool", color:"", icon:"", entity_parent: null  },
-  {id:nextTagId++, name:"ArcGIS", entity_type:"tool" },
-                                {id:nextTagId++, "name":"GIS", entity_type:"skill", color:"", icon:"", entity_parent: null  }
-]
-  entities.value = tagData;
-  let nextId = 1;
 
-  function addEntity(entity: Omit<Entity, 'id'>) {
-    const newEntity = { ...entity, id: nextId++ };
-    entities.value.push(newEntity);
-    return newEntity;
+  async function addEntity(entity: Omit<Entity, 'id'>) {
+    try {
+      const response = await api.post('/entities', entity);
+      const newEntity = response.data.data;
+      entities.value.push(newEntity);
+      return newEntity;
+    } catch (error) {
+      console.error('Error creating entity:', error);
+      throw error;
+    }
   }
 
-  function updateEntity(id: number, entity: Partial<Entity>) {
-    const index = entities.value.findIndex(e => e.id === id);
-    if (index !== -1) {
-      entities.value[index] = { ...entities.value[index], ...entity };
-      return entities.value[index];
+  async function updateEntity(id: number, entity: Partial<Entity>) {
+    try {
+      const response = await api.put(`/entities/${id}`, entity);
+      const updatedEntity = response.data.data;
+      const index = entities.value.findIndex(e => e.id === id);
+      if (index !== -1) {
+        entities.value[index] = updatedEntity;
+      }
+      return updatedEntity;
+    } catch (error) {
+      console.error('Error updating entity:', error);
+      throw error;
     }
-    return null;
   }
 
-  function deleteEntity(id: number) {
-    const index = entities.value.findIndex(e => e.id === id);
-    if (index !== -1) {
-      entities.value.splice(index, 1);
-      return true;
+  async function deleteEntity(id: number) {
+    try {
+      await api.delete(`/entities/${id}`);
+      const index = entities.value.findIndex(e => e.id === id);
+      if (index !== -1) {
+        entities.value.splice(index, 1);
+      }
+      return true;
+    } catch (error) {
+      console.error('Error deleting entity:', error);
+      throw error;
     }
-    return false;
   }
 
-  function getEntity(id: number) {
-    return entities.value.find(e => e.id === id);
+  async function getEntity(id: number) {
+    try {
+      const response = await api.get(`/entities/${id}`);
+      return response.data.data;
+    } catch (error) {
+      console.error('Error fetching entity:', error);
+      throw error;
+    }
   }
 
-  function getEntities() {
-    return entities.value;
+  async function getEntities() {
+    try {
+      const response = await api.get('/entities');
+      entities.value = response.data.data;
+      return entities.value;
+    } catch (error) {
+      console.error('Error fetching entities:', error);
+      throw error;
+    }
   }
 
   return {
@@ .. @@
   };
 });