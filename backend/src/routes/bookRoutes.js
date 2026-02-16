"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
var express_1 = require("express");
var bookController_js_1 = require("../controllers/bookController.js");
var authMiddleware_js_1 = require("../middlewares/authMiddleware.js");
var router = express_1.default.Router();
router.get('/', bookController_js_1.getAllBooks);
router.get('/slug/:slug', bookController_js_1.getBookBySlug);
router.get('/:id', bookController_js_1.getBook);
// Nested routes
var reviewRoutes_js_1 = require("./reviewRoutes.js");
router.use('/:bookId/reviews', reviewRoutes_js_1.default);
// Admin only routes
var uploadMiddleware_js_1 = require("../middlewares/uploadMiddleware.js");
router.post('/bulk-delete', authMiddleware_js_1.protect, (0, authMiddleware_js_1.restrictTo)('ADMIN', 'SUPER_ADMIN'), bookController_js_1.deleteBulkBooks);
router.post('/', authMiddleware_js_1.protect, (0, authMiddleware_js_1.restrictTo)('ADMIN', 'SUPER_ADMIN'), uploadMiddleware_js_1.upload.single('coverImage'), uploadMiddleware_js_1.resizeImage, bookController_js_1.createBook);
router.route('/:id')
    .put(authMiddleware_js_1.protect, (0, authMiddleware_js_1.restrictTo)('ADMIN', 'SUPER_ADMIN'), uploadMiddleware_js_1.upload.single('coverImage'), uploadMiddleware_js_1.resizeImage, bookController_js_1.updateBook)
    .delete(authMiddleware_js_1.protect, (0, authMiddleware_js_1.restrictTo)('ADMIN', 'SUPER_ADMIN'), bookController_js_1.deleteBook);
exports.default = router;
