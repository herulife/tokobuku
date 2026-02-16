import { Router } from 'express';
import shippingController from '../controllers/shippingController';

const router = Router();

// New Komerce Routes
router.get('/search', shippingController.searchDestination);
router.post('/cost', shippingController.calculateCost);
router.get('/check-connection', shippingController.checkConnection);

// Legacy routes (kept for safety but return empty)
router.get('/provinces', shippingController.getProvinces);
router.get('/cities', shippingController.getCities);

export default router;
