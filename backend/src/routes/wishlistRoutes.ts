import express from 'express';
import {
    getWishlist,
    addToWishlist,
    removeFromWishlist,
} from '../controllers/wishlistController.js';
import { protect } from '../middlewares/authMiddleware.js';

const router = express.Router();

router.use(protect);

router.get('/', getWishlist);
router.post('/', addToWishlist);
router.delete('/:bookId', removeFromWishlist);

export default router;
