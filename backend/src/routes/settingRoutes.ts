import express from 'express';
import { getSettings, updateSettings } from '../controllers/settingController';
import { protect, restrictTo } from '../middlewares/authMiddleware';

const router = express.Router();

router.get('/', getSettings); // Public access to read settings (Bank info etc)
router.put('/', protect, restrictTo('SUPER_ADMIN'), updateSettings);

export default router;
