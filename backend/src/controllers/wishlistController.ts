import { Request, Response, NextFunction } from 'express';
import { PrismaClient } from '@prisma/client';
import { asyncHandler } from '../middlewares/asyncHandler.js';
import { AppError } from '../utils/AppError.js';

const prisma = new PrismaClient();

export const getWishlist = asyncHandler(async (req: Request, res: Response, next: NextFunction) => {
    const userId = (req as any).user.id;

    const wishlist = await prisma.wishlist.findMany({
        where: { userId },
        include: {
            book: true,
        },
    });

    res.status(200).json({
        status: 'success',
        data: { wishlist },
    });
});

export const addToWishlist = asyncHandler(async (req: Request, res: Response, next: NextFunction) => {
    const userId = (req as any).user.id;
    const { bookId } = req.body;

    if (!bookId) {
        return next(new AppError('Book ID is required', 400));
    }

    // Check if book exists
    const book = await prisma.book.findUnique({ where: { id: bookId } });
    if (!book) {
        return next(new AppError('Book not found', 404));
    }

    // Check if already in wishlist
    const existingItem = await prisma.wishlist.findUnique({
        where: {
            userId_bookId: {
                userId,
                bookId,
            },
        },
    });

    if (existingItem) {
        return next(new AppError('Book already in wishlist', 400));
    }

    const newItem = await prisma.wishlist.create({
        data: {
            userId,
            bookId,
        },
        include: {
            book: true
        }
    });

    res.status(201).json({
        status: 'success',
        data: { item: newItem },
    });
});

export const removeFromWishlist = asyncHandler(async (req: Request, res: Response, next: NextFunction) => {
    const userId = (req as any).user.id;
    const { bookId } = req.params as { bookId: string };

    try {
        await prisma.wishlist.delete({
            where: {
                userId_bookId: {
                    userId,
                    bookId,
                },
            },
        });
    } catch (e) {
        return next(new AppError('Item not found in wishlist', 404));
    }

    res.status(204).json({
        status: 'success',
        data: null,
    });
});
