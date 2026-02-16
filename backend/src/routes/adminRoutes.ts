import express from 'express';
import { getDashboardStats } from '../controllers/adminController.js';
import { protect, restrictTo } from '../middlewares/authMiddleware.js';

const router = express.Router();

router.use(protect);
router.use(restrictTo('ADMIN', 'SUPER_ADMIN'));

router.get('/stats', getDashboardStats);

export default router;
