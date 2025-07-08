import * as entitiesModel from '../models/entitiesModel.js';

export const getAllEntities = async (req, res) => {
  const entities = await entitiesModel.findAll();
  res.json({
    success: true,
    data: entities,
    count: entities.length,
  });
};

export const getEntityById = async (req, res) => {
  const { id } = req.params;
  const entity = await entitiesModel.findById(parseInt(id));
  
  if (!entity) {
    return res.status(404).json({
      success: false,
      message: 'Entity not found',
    });
  }
  
  res.json({
    success: true,
    data: entity,
  });
};

export const createEntity = async (req, res) => {
  const entity = await entitiesModel.create(req.body);
  
  res.status(201).json({
    success: true,
    data: entity,
    message: 'Entity created successfully',
  });
};

export const updateEntity = async (req, res) => {
  const { id } = req.params;
  const entity = await entitiesModel.update(parseInt(id), req.body);
  
  if (!entity) {
    return res.status(404).json({
      success: false,
      message: 'Entity not found',
    });
  }
  
  res.json({
    success: true,
    data: entity,
    message: 'Entity updated successfully',
  });
};

export const deleteEntity = async (req, res) => {
  const { id } = req.params;
  const deleted = await entitiesModel.remove(parseInt(id));
  
  if (!deleted) {
    return res.status(404).json({
      success: false,
      message: 'Entity not found',
    });
  }
  
  res.json({
    success: true,
    message: 'Entity deleted successfully',
  });
};