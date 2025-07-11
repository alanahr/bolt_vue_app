import database from '../config/database.js';

const COLLECTION_NAME = 'entities';

// Get next available ID
const getNextId = async () => {
  const db = database.getDb();
  const lastEntity = await db.collection(COLLECTION_NAME)
    .findOne({}, { sort: { id: -1 } });
  return lastEntity ? lastEntity.id + 1 : 1;
};

export const findAll = async () => {
  try {
    const db = database.getDb();
    const entities = await db.collection(COLLECTION_NAME)
      .find({})
      .sort({ id: 1 })
      .toArray();
    
    // Remove MongoDB _id field from results
    return entities.map(({ _id, ...entity }) => entity);
  } catch (error) {
    console.error('Error finding all entities:', error);
    throw error;
  }
};

export const findById = async (id) => {
  try {
    const db = database.getDb();
    const entity = await db.collection(COLLECTION_NAME)
      .findOne({ id: parseInt(id) });
    
    if (!entity) return null;
    
    // Remove MongoDB _id field
    const { _id, ...entityData } = entity;
    return entityData;
  } catch (error) {
    console.error('Error finding entity by ID:', error);
    throw error;
  }
};

export const create = async (entityData) => {
  try {
    const db = database.getDb();
    const id = await getNextId();
    
    const newEntity = {
      id,
      ...entityData,
      created_at: new Date(),
      updated_at: new Date(),
    };
    
    const result = await db.collection(COLLECTION_NAME)
      .insertOne(newEntity);
    
    if (!result.insertedId) {
      throw new Error('Failed to create entity');
    }
    
    // Remove MongoDB _id field
    const { _id, ...createdEntity } = newEntity;
    return createdEntity;
  } catch (error) {
    console.error('Error creating entity:', error);
    throw error;
  }
};

export const update = async (id, entityData) => {
  try {
    const db = database.getDb();
    const parsedId = parseInt(id);
    
    const updateData = {
      ...entityData,
      id: parsedId, // Ensure ID doesn't change
      updated_at: new Date(),
    };
    
    const result = await db.collection(COLLECTION_NAME)
      .findOneAndUpdate(
        { id: parsedId },
        { $set: updateData },
        { returnDocument: 'after' }
      );
    
    if (!result.value) return null;
    
    // Remove MongoDB _id field
    const { _id, ...updatedEntity } = result.value;
    return updatedEntity;
  } catch (error) {
    console.error('Error updating entity:', error);
    throw error;
  }
};

export const remove = async (id) => {
  try {
    const db = database.getDb();
    const result = await db.collection(COLLECTION_NAME)
      .deleteOne({ id: parseInt(id) });
    
    return result.deletedCount > 0;
  } catch (error) {
    console.error('Error removing entity:', error);
    throw error;
  }
};