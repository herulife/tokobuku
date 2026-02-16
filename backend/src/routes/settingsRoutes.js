"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
var express_1 = require("express");
var settingsController_js_1 = require("../controllers/settingsController.js");
var authMiddleware_js_1 = require("../middlewares/authMiddleware.js");
var router = express_1.default.Router();
// Public route
router.get('/public', settingsController_js_1.default.getPublicSettings);
// All other settings routes require admin authentication
router.use(authMiddleware_js_1.protect, (0, authMiddleware_js_1.restrictTo)('ADMIN'));
router.get('/', settingsController_js_1.default.getAllSettings);
router.get('/:key', settingsController_js_1.default.getSetting);
router.put('/', settingsController_js_1.default.updateSettings);
router.put('/:key', settingsController_js_1.default.updateSetting);
router.delete('/:key', settingsController_js_1.default.deleteSetting);
exports.default = router;
