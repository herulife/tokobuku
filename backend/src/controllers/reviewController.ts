import { Request, Response, NextFunction } from 'express';
import { PrismaClient } from '@prisma/client';
import { asyncHandler } from '../middlewares/asyncHandler.js';
import { AppError } from '../utils/AppError.js';

const prisma = new PrismaClient();

export const createReview = asyncHandler(async (req: Request, res: Response, next: NextFunction) => {
    const userId = (req as any).user.id;
    const { bookId: paramBookId } = req.params;
    const bookId = String(paramBookId); // Convert to string for Prisma
    const { rating, comment } = req.body;

    if (!rating || rating < 1 || rating > 5) {
        return next(new AppError('Rating must be between 1 and 5', 400));
    }

    // Check if book exists
    const book = await prisma.book.findUnique({ where: { id: bookId } });
    if (!book) {
        return next(new AppError('Book not found', 404));
    }

    // Check if user already reviewed this book
    const existingReview = await prisma.review.findUnique({
        where: {
            userId_bookId: {
                userId,
                bookId,
            },
        },
    });

    if (existingReview) {
        return next(new AppError('You have already reviewed this book', 400));
    }

    // Create review
    const review = await prisma.review.create({
        data: {
            userId,
            bookId,
            rating: Number(rating),
            comment,
        },
        include: {
            user: {
                select: {
                    id: true,
                    name: true,
                    avatar: true,
                },
            },
        },
    });

    // Update book average rating and total rating
    const aggregations = await prisma.review.aggregate({
        where: { bookId },
        _avg: { rating: true },
        _count: { rating: true },
    });

    await prisma.book.update({
        where: { id: bookId },
        data: {
            rating: aggregations._avg.rating || 0,
            totalRating: aggregations._count.rating || 0,
        },
    });

    res.status(201).json({
        status: 'success',
        data: { review },
    });
});

export const getBookReviews = asyncHandler(async (req: Request, res: Response, next: NextFunction) => {
    const { bookId: paramBookId } = req.params;
    const bookId = String(paramBookId); // Convert to string for Prisma

    const reviews = await prisma.review.findMany({
        where: { bookId },
        include: {
            user: {
                select: {
                    id: true,
                    name: true,
                    avatar: true,
                },
            },
        },
        orderBy: { createdAt: 'desc' },
    });

    res.status(200).json({
        status: 'success',
        results: reviews.length,
        data: { reviews },
    });
});

export const deleteReview = asyncHandler(async (req: Request, res: Response, next: NextFunction) => {
    const userId = (req as any).user.id;
    const userRole = (req as any).user.role;
    const { id } = req.params;
    const reviewId = String(id); // Convert to string for Prisma

    const review = await prisma.review.findUnique({ where: { id: reviewId } });

    if (!review) {
        return next(new AppError('Review not found', 404));
    }

    // Only allow deletion if user is owner or admin
    if (review.userId !== userId && userRole !== 'ADMIN') {
        return next(new AppError('You update not authorized to delete this review', 403));
    }

    await prisma.review.delete({ where: { id: reviewId } });

    // Recalculate book rating
    const bookId = review.bookId;
    const aggregations = await prisma.review.aggregate({
        where: { bookId },
        _avg: { rating: true },
        _count: { rating: true },
    });

    await prisma.book.update({
        where: { id: bookId },
        data: {
            rating: aggregations._avg.rating || 0,
            totalRating: aggregations._count.rating || 0,
        },
    });

    res.status(204).json({
        status: 'success',
        data: null,
    });
});
