"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
var express_1 = require("express");
var settingController_1 = require("../controllers/settingController");
var authMiddleware_1 = require("../middlewares/authMiddleware");
var router = express_1.default.Router();
router.get('/', settingController_1.getSettings); // Public access to read settings (Bank info etc)
router.put('/', authMiddleware_1.protect, (0, authMiddleware_1.restrictTo)('SUPER_ADMIN'), settingController_1.updateSettings);
exports.default = router;
