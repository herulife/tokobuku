"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
var express_1 = require("express");
var userController_js_1 = require("../controllers/userController.js");
var authMiddleware_js_1 = require("../middlewares/authMiddleware.js");
var router = express_1.default.Router();
router.use(authMiddleware_js_1.protect);
router.put('/profile', userController_js_1.updateProfile);
// SUPER_ADMIN Routes only
router.use((0, authMiddleware_js_1.restrictTo)('SUPER_ADMIN'));
router.post('/', userController_js_1.createUser);
router.get('/', userController_js_1.getAllUsers);
router.route('/:id')
    .delete(userController_js_1.deleteUser);
router.put('/:id/role', userController_js_1.updateUserRole);
exports.default = router;
