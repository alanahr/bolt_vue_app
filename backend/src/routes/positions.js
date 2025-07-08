import express from 'express';
import { body, param, validationResult } from 'express-validator';
import { asyncHandler } from '../middleware/errorMiddleware.js';
import * as positionsController from '../controllers/positionsController.js';

const router = express.Router();

// Validation middleware
const validatePosition = [
  body('name').notEmpty().withMessage('Name is required'),
  body('start_year').isInt({ min: 1900, max: 2100 }).withMessage('Valid start year is required'),
  body('start_month').isInt({ min: 1, max: 12 }).withMessage('Valid start month is required'),
  body('start_day').isInt({ min: 1, max: 31 }).withMessage('Valid start day is required'),
  body('salary').optional().isNumeric().withMessage('Salary must be a number'),
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
router.get('/', asyncHandler(positionsController.getAllPositions));
router.get('/:id', validateId, handleValidationErrors, asyncHandler(positionsController.getPositionById));
router.post('/', validatePosition, handleValidationErrors, asyncHandler(positionsController.createPosition));
router.put('/:id', validateId, validatePosition, handleValidationErrors, asyncHandler(positionsController.updatePosition));
router.delete('/:id', validateId, handleValidationErrors, asyncHandler(positionsController.deletePosition));

export default router;