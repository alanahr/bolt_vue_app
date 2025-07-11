import database from '../config/database.js';

const COLLECTION_NAME = 'positions';

// Get next available ID
const getNextId = async () => {
  const db = database.getDb();
  const lastPosition = await db.collection(COLLECTION_NAME)
    .findOne({}, { sort: { id: -1 } });
  return lastPosition ? lastPosition.id + 1 : 1;
};

export const findAll = async () => {
  try {
    const db = database.getDb();
    const positions = await db.collection(COLLECTION_NAME)
      .find({})
      .sort({ id: 1 })
      .toArray();
    
    // Remove MongoDB _id field from results
    return positions.map(({ _id, ...position }) => position);
  } catch (error) {
    console.error('Error finding all positions:', error);
    throw error;
  }
};

export const findById = async (id) => {
  try {
    const db = database.getDb();
    const position = await db.collection(COLLECTION_NAME)
      .findOne({ id: parseInt(id) });
    
    if (!position) return null;
    
    // Remove MongoDB _id field
    const { _id, ...positionData } = position;
    return positionData;
  } catch (error) {
    console.error('Error finding position by ID:', error);
    throw error;
  }
};

export const create = async (positionData) => {
  try {
    const db = database.getDb();
    const id = await getNextId();
    
    const newPosition = {
      id,
      ...positionData,
      details: positionData.details || [],
      created_at: new Date(),
      updated_at: new Date(),
    };
    
    const result = await db.collection(COLLECTION_NAME)
      .insertOne(newPosition);
    
    if (!result.insertedId) {
      throw new Error('Failed to create position');
    }
    
    // Remove MongoDB _id field
    const { _id, ...createdPosition } = newPosition;
    return createdPosition;
  } catch (error) {
    console.error('Error creating position:', error);
    throw error;
  }
};

export const update = async (id, positionData) => {
  try {
    const db = database.getDb();
    const parsedId = parseInt(id);
    
    const updateData = {
      ...positionData,
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
    const { _id, ...updatedPosition } = result.value;
    return updatedPosition;
  } catch (error) {
    console.error('Error updating position:', error);
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
    console.error('Error removing position:', error);
    throw error;
  }
};