import express from 'express';
import {
    getAllBooks,
    getBook,
    getBookBySlug,
    createBook,
    updateBook,
    deleteBook,
    deleteBulkBooks,
} from '../controllers/bookController';
import { protect, restrictTo } from '../middlewares/authMiddleware';

const router = express.Router();

router.get('/', getAllBooks);
router.get('/slug/:slug', getBookBySlug);
router.get('/:id', getBook);

// Nested routes
import reviewRouter from './reviewRoutes';
router.use('/:bookId/reviews', reviewRouter);

// Admin only routes
import { upload, resizeImage } from '../middlewares/uploadMiddleware';

router.post('/bulk-delete', protect, restrictTo('ADMIN', 'SUPER_ADMIN'), deleteBulkBooks);

router.post('/', protect, restrictTo('ADMIN', 'SUPER_ADMIN'), upload.single('coverImage'), resizeImage, createBook);
router.route('/:id')
    .put(protect, restrictTo('ADMIN', 'SUPER_ADMIN'), upload.single('coverImage'), resizeImage, updateBook)
    .delete(protect, restrictTo('ADMIN', 'SUPER_ADMIN'), deleteBook);

export default router;
