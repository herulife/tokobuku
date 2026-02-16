"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
var express_1 = require("express");
var orderController_js_1 = require("../controllers/orderController.js");
var uploadMiddleware_js_1 = require("../middlewares/uploadMiddleware.js");
var authMiddleware_js_1 = require("../middlewares/authMiddleware.js");
var router = express_1.default.Router();
router.use(authMiddleware_js_1.protect);
// User routes
router.post('/', orderController_js_1.createOrder);
router.post('/:id/proof', uploadMiddleware_js_1.upload.single('paymentProof'), uploadMiddleware_js_1.processPaymentProof, orderController_js_1.uploadPaymentProof); // New route
router.get('/', orderController_js_1.getMyOrders);
router.get('/:id', orderController_js_1.getOrderById);
router.put('/:id/cancel', orderController_js_1.cancelOrder);
// Admin routes
router.get('/admin/all', (0, authMiddleware_js_1.restrictTo)('ADMIN', 'SUPER_ADMIN'), orderController_js_1.getAllOrders);
router.put('/admin/:id/status', (0, authMiddleware_js_1.restrictTo)('ADMIN', 'SUPER_ADMIN'), orderController_js_1.updateOrderStatus);
router.delete('/admin/:id', (0, authMiddleware_js_1.restrictTo)('SUPER_ADMIN'), orderController_js_1.deleteOrder);
exports.default = router;
