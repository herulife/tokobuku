import { Request, Response, NextFunction } from 'express';
import { PrismaClient } from '@prisma/client';
import { asyncHandler } from '../middlewares/asyncHandler.js';
import { AppError } from '../utils/AppError.js';

const prisma = new PrismaClient();

// Helper to get or create cart for user
const getOrCreateCart = async (userId: string) => {
    let cart = await prisma.cart.findUnique({
        where: { userId },
        include: {
            items: {
                include: {
                    book: true,
                },
                orderBy: {
                    createdAt: 'asc'
                }
            },
        },
    });

    if (!cart) {
        cart = await prisma.cart.create({
            data: { userId },
            include: {
                items: {
                    include: {
                        book: true,
                    },
                },
            },
        });
    }

    return cart;
};

export const getCart = asyncHandler(async (req: Request, res: Response, next: NextFunction) => {
    const userId = (req as any).user.id;
    const cart = await getOrCreateCart(userId);

    res.status(200).json({
        status: 'success',
        data: { cart },
    });
});

export const addToCart = asyncHandler(async (req: Request, res: Response, next: NextFunction) => {
    const userId = (req as any).user.id;
    const { bookId, quantity = 1 } = req.body;

    if (!bookId) {
        return next(new AppError('Book ID is required', 400));
    }

    // Ensure book exists and has stock
    const book = await prisma.book.findUnique({ where: { id: bookId } });
    if (!book) {
        return next(new AppError('Book not found', 404));
    }

    if (book.stock < quantity) {
        return next(new AppError('Not enough stock', 400));
    }

    let cart = await getOrCreateCart(userId);

    // Check if item exists in cart
    const existingItem = await prisma.cartItem.findUnique({
        where: {
            cartId_bookId: {
                cartId: cart.id,
                bookId,
            },
        },
    });

    if (existingItem) {
        // Update quantity
        await prisma.cartItem.update({
            where: { id: existingItem.id },
            data: { quantity: existingItem.quantity + Number(quantity) },
        });
    } else {
        // Add new item
        await prisma.cartItem.create({
            data: {
                cartId: cart.id,
                bookId,
                quantity: Number(quantity),
            },
        });
    }

    // Refetch cart with updated items
    const updatedCart = await getOrCreateCart(userId);

    res.status(200).json({
        status: 'success',
        data: { cart: updatedCart },
    });
});

export const updateCartItem = asyncHandler(async (req: Request, res: Response, next: NextFunction) => {
    const userId = (req as any).user.id;
    const { bookId } = req.params;
    const { quantity } = req.body;

    if (quantity < 1) {
        return next(new AppError('Quantity must be at least 1', 400));
    }

    const cart = await prisma.cart.findUnique({ where: { userId } });
    if (!cart) return next(new AppError('Cart not found', 404));

    const item = await prisma.cartItem.findUnique({
        where: {
            cartId_bookId: {
                cartId: cart.id,
                bookId: bookId
            }
        }
    });

    if (!item) return next(new AppError('Item not found in cart', 404));

    // Check stock again
    const book = await prisma.book.findUnique({ where: { id: bookId } });
    if (book && book.stock < quantity) {
        return next(new AppError('Not enough stock', 400));
    }

    await prisma.cartItem.update({
        where: { id: item.id },
        data: { quantity: Number(quantity) },
    });

    const updatedCart = await getOrCreateCart(userId);

    res.status(200).json({
        status: 'success',
        data: { cart: updatedCart },
    });
});

export const removeCartItem = asyncHandler(async (req: Request, res: Response, next: NextFunction) => {
    const userId = (req as any).user.id;
    const { bookId } = req.params;

    const cart = await prisma.cart.findUnique({ where: { userId } });
    if (!cart) return next(new AppError('Cart not found', 404));

    try {
        await prisma.cartItem.delete({
            where: {
                cartId_bookId: {
                    cartId: cart.id,
                    bookId: bookId
                }
            }
        });
    } catch (e) {
        return next(new AppError('Item not found in cart', 404));
    }

    const updatedCart = await getOrCreateCart(userId);

    res.status(200).json({
        status: 'success',
        data: { cart: updatedCart },
    });
});

export const clearCart = asyncHandler(async (req: Request, res: Response, next: NextFunction) => {
    const userId = (req as any).user.id;

    const cart = await prisma.cart.findUnique({ where: { userId } });
    if (!cart) return next(new AppError('Cart not found', 404));

    await prisma.cartItem.deleteMany({
        where: { cartId: cart.id }
    });

    res.status(204).json({
        status: 'success',
        data: null
    });
});
