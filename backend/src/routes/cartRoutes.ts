import express from 'express';
import {
    getCart,
    addToCart,
    updateCartItem,
    removeCartItem,
    clearCart
} from '../controllers/cartController.js';
import { protect } from '../middlewares/authMiddleware.js';

const router = express.Router();

router.use(protect);

router.get('/', getCart);
router.post('/items', addToCart);
router.put('/items/:bookId', updateCartItem);
router.delete('/items/:bookId', removeCartItem);
router.delete('/', clearCart);

export default router;
