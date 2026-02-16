import express from 'express';
import {
    createOrder,
    getMyOrders,
    getOrderById,
    cancelOrder,
    getAllOrders,

    updateOrderStatus,
    deleteOrder,
    uploadPaymentProof
} from '../controllers/orderController';
import { upload, processPaymentProof } from '../middlewares/uploadMiddleware';
import { protect, restrictTo } from '../middlewares/authMiddleware';

const router = express.Router();

router.use(protect);

// User routes
router.post('/', createOrder);
router.post('/:id/proof', upload.single('paymentProof'), processPaymentProof, uploadPaymentProof); // New route
router.get('/', getMyOrders);
router.get('/:id', getOrderById);
router.put('/:id/cancel', cancelOrder);

// Admin routes
router.get('/admin/all', restrictTo('ADMIN', 'SUPER_ADMIN'), getAllOrders);
router.put('/admin/:id/status', restrictTo('ADMIN', 'SUPER_ADMIN'), updateOrderStatus);
router.delete('/admin/:id', restrictTo('SUPER_ADMIN'), deleteOrder);

export default router;
