"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
var express_1 = require("express");
var categoryController_js_1 = require("../controllers/categoryController.js");
var authMiddleware_js_1 = require("../middlewares/authMiddleware.js");
var router = express_1.default.Router();
router.get('/', categoryController_js_1.getAllCategories);
// Admin only routes
router.use(authMiddleware_js_1.protect, (0, authMiddleware_js_1.restrictTo)('ADMIN', 'SUPER_ADMIN'));
router.post('/', categoryController_js_1.createCategory);
router.route('/:id')
    .put(categoryController_js_1.updateCategory)
    .delete(categoryController_js_1.deleteCategory);
exports.default = router;
