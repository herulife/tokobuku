import express from 'express';
import {
    createReview,
    getBookReviews,
    deleteReview,
} from '../controllers/reviewController';
import { protect, restrictTo } from '../middlewares/authMiddleware';

const router = express.Router({ mergeParams: true });

// Routes starting with /api/v1/books/:bookId/reviews
// OR /api/v1/reviews (for delete)

router
    .route('/')
    .get(getBookReviews)
    .post(protect, createReview);

router
    .route('/:id')
    .delete(protect, deleteReview);

export default router;
