const express = require('express');
const router = express.Router();
const shippingController = require('../controllers/shipping.controller');

// Public routes - no authentication required
router.get('/provinces', shippingController.getProvinces);
router.get('/cities', shippingController.getCities);
router.post('/cost', shippingController.calculateCost);

module.exports = router;
