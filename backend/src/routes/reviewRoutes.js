"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
var express_1 = require("express");
var reviewController_js_1 = require("../controllers/reviewController.js");
var authMiddleware_js_1 = require("../middlewares/authMiddleware.js");
var router = express_1.default.Router({ mergeParams: true });
// Routes starting with /api/v1/books/:bookId/reviews
// OR /api/v1/reviews (for delete)
router
    .route('/')
    .get(reviewController_js_1.getBookReviews)
    .post(authMiddleware_js_1.protect, reviewController_js_1.createReview);
router
    .route('/:id')
    .delete(authMiddleware_js_1.protect, reviewController_js_1.deleteReview);
exports.default = router;
