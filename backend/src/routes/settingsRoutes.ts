import express from 'express';
import settingsController from '../controllers/settingsController.js';
import { protect, restrictTo } from '../middlewares/authMiddleware.js';

const router = express.Router();

// Public route
router.get('/public', settingsController.getPublicSettings);

// All other settings routes require admin authentication
router.use(protect, restrictTo('ADMIN'));

router.get('/', settingsController.getAllSettings);
router.get('/:key', settingsController.getSetting);
router.put('/', settingsController.updateSettings);
router.put('/:key', settingsController.updateSetting);
router.delete('/:key', settingsController.deleteSetting);

export default router;
