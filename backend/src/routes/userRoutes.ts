import express from 'express';
import { updateProfile, getAllUsers, updateUserRole, deleteUser, createUser } from '../controllers/userController.js';
import { protect, restrictTo } from '../middlewares/authMiddleware.js';

const router = express.Router();

router.use(protect);

router.put('/profile', updateProfile);

// SUPER_ADMIN Routes only
router.use(restrictTo('SUPER_ADMIN'));

router.post('/', createUser);
router.get('/', getAllUsers);
router.route('/:id')
    .delete(deleteUser);

router.put('/:id/role', updateUserRole);

export default router;
