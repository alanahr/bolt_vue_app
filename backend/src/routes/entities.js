import express from 'express';
import { body, param, validationResult } from 'express-validator';
import { asyncHandler } from '../middleware/errorMiddleware.js';
import * as entitiesController from '../controllers/entitiesController.js';

const router = express.Router();

// Validation middleware
const validateEntity = [
  body('name').notEmpty().withMessage('Name is required'),
  body('entity_type').isIn([
    'company', 'person', 'skill', 'location', 'room', 'container',
    'equipment', 'muscles', 'meta', 'exercise_type', 'object', 'tool', 'other'
  ]).withMessage('Valid entity type is required'),
];

const validateId = [
  param('id').isInt({ min: 1 }).withMessage('Valid ID is required'),
];

const handleValidationErrors = (req, res, next) => {
  const errors = validationResult(req);
  if (!errors.isEmpty()) {
    return res.status(400).json({
      message: 'Validation failed',
      errors: errors.array(),
    });
  }
  next();
};

// Routes
router.get('/', asyncHandler(entitiesController.getAllEntities));
router.get('/:id', validateId, handleValidationErrors, asyncHandler(entitiesController.getEntityById));
router.post('/', validateEntity, handleValidationErrors, asyncHandler(entitiesController.createEntity));
router.put('/:id', validateId, validateEntity, handleValidationErrors, asyncHandler(entitiesController.updateEntity));
router.delete('/:id', validateId, handleValidationErrors, asyncHandler(entitiesController.deleteEntity));

export default router;