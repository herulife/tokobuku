"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
var express_1 = require("express");
var shippingController_js_1 = require("../controllers/shippingController.js");
var router = (0, express_1.Router)();
// New Komerce Routes
router.get('/search', shippingController_js_1.default.searchDestination);
router.post('/cost', shippingController_js_1.default.calculateCost);
router.get('/check-connection', shippingController_js_1.default.checkConnection);
// Legacy routes (kept for safety but return empty)
router.get('/provinces', shippingController_js_1.default.getProvinces);
router.get('/cities', shippingController_js_1.default.getCities);
exports.default = router;
