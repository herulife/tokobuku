import express from 'express';
import {
    getAllCategories,
    createCategory,
    updateCategory,
    deleteCategory,
} from '../controllers/categoryController.js';
import { protect, restrictTo } from '../middlewares/authMiddleware.js';

const router = express.Router();

router.get('/', getAllCategories);

// Admin only routes
router.use(protect, restrictTo('ADMIN', 'SUPER_ADMIN'));

router.post('/', createCategory);
router.route('/:id')
    .put(updateCategory)
    .delete(deleteCategory);

export default router;
