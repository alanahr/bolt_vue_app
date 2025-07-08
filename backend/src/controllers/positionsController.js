import * as positionsModel from '../models/positionsModel.js';

export const getAllPositions = async (req, res) => {
  const positions = await positionsModel.findAll();
  res.json({
    success: true,
    data: positions,
    count: positions.length,
  });
};

export const getPositionById = async (req, res) => {
  const { id } = req.params;
  const position = await positionsModel.findById(parseInt(id));
  
  if (!position) {
    return res.status(404).json({
      success: false,
      message: 'Position not found',
    });
  }
  
  res.json({
    success: true,
    data: position,
  });
};

export const createPosition = async (req, res) => {
  const position = await positionsModel.create(req.body);
  
  res.status(201).json({
    success: true,
    data: position,
    message: 'Position created successfully',
  });
};

export const updatePosition = async (req, res) => {
  const { id } = req.params;
  const position = await positionsModel.update(parseInt(id), req.body);
  
  if (!position) {
    return res.status(404).json({
      success: false,
      message: 'Position not found',
    });
  }
  
  res.json({
    success: true,
    data: position,
    message: 'Position updated successfully',
  });
};

export const deletePosition = async (req, res) => {
  const { id } = req.params;
  const deleted = await positionsModel.remove(parseInt(id));
  
  if (!deleted) {
    return res.status(404).json({
      success: false,
      message: 'Position not found',
    });
  }
  
  res.json({
    success: true,
    message: 'Position deleted successfully',
  });
};