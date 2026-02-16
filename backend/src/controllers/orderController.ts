import { Request, Response, NextFunction } from 'express';
import { PrismaClient } from '@prisma/client';
import { asyncHandler } from '../middlewares/asyncHandler.js';
import { AppError } from '../utils/AppError.js';

const prisma = new PrismaClient();

// Generate Invoice Number: INV/20231027/CUID-SUFFIX
const generateInvoiceNumber = () => {
    const date = new Date().toISOString().slice(0, 10).replace(/-/g, '');
    const random = Math.floor(Math.random() * 10000).toString().padStart(4, '0');
    return `INV/${date}/${random}`;
};

export const createOrder = asyncHandler(async (req: Request, res: Response, next: NextFunction) => {
    const userId = (req as any).user.id;
    const { shippingAddress, paymentMethod, courier } = req.body;

    if (!shippingAddress || !paymentMethod) {
        return next(new AppError('Shipping address and payment method are required', 400));
    }

    // 1. Get User's Cart
    const cart = await prisma.cart.findUnique({
        where: { userId },
        include: {
            items: {
                include: { book: true }
            }
        }
    });

    if (!cart || cart.items.length === 0) {
        return next(new AppError('Cart is empty', 400));
    }

    // 2. Validate Stock & Calculate Total
    let total = 0;
    const orderItemsData: { bookId: string; quantity: number; price: number }[] = [];

    for (const item of cart.items) {
        if (item.book.stock < item.quantity) {
            return next(new AppError(`Book '${item.book.title}' is out of stock or insufficient quantity`, 400));
        }

        const price = item.book.discountPrice || item.book.price;
        total += price * item.quantity;

        orderItemsData.push({
            bookId: item.bookId,
            quantity: item.quantity,
            price: price
        });
    }

    // 3. Create Order Transaction
    const order = await prisma.$transaction(async (tx) => {
        // Create Order
        const newOrder = await tx.order.create({
            data: {
                userId,
                invoiceNumber: generateInvoiceNumber(),
                total,
                status: 'PENDING',
                paymentMethod,
                shippingAddress,
                courier,
                items: {
                    create: orderItemsData
                }
            },
            include: {
                items: {
                    include: { book: true }
                }
            }
        });

        // Reduce Stock
        for (const item of cart.items) {
            await tx.book.update({
                where: { id: item.bookId },
                data: { stock: { decrement: item.quantity } }
            });
        }

        // Clear Cart
        await tx.cartItem.deleteMany({
            where: { cartId: cart.id }
        });

        return newOrder;
    });

    res.status(201).json({
        status: 'success',
        data: { order }
    });
});

export const getMyOrders = asyncHandler(async (req: Request, res: Response, next: NextFunction) => {
    const userId = (req as any).user.id;

    const orders = await prisma.order.findMany({
        where: { userId },
        orderBy: { createdAt: 'desc' },
        include: {
            items: {
                include: { book: true }
            }
        }
    });

    res.status(200).json({
        status: 'success',
        data: { orders }
    });
});

export const getOrderById = asyncHandler(async (req: Request, res: Response, next: NextFunction) => {
    const { id } = req.params as { id: string };
    const userId = (req as any).user.id;
    const userRole = (req as any).user.role;

    const order = await prisma.order.findUnique({
        where: { id },
        include: {
            user: {
                select: { name: true, email: true }
            },
            items: {
                include: { book: true }
            }
        }
    });

    if (!order) {
        return next(new AppError('Order not found', 404));
    }

    // Check ownership or admin role
    if (order.userId !== userId && userRole !== 'admin' && userRole !== 'ADMIN') {
        return next(new AppError('You do not have permission to view this order', 403));
    }

    res.status(200).json({
        status: 'success',
        data: { order }
    });
});

export const cancelOrder = asyncHandler(async (req: Request, res: Response, next: NextFunction) => {
    const { id } = req.params as { id: string };
    const userId = (req as any).user.id;

    const order = await prisma.order.findUnique({
        where: { id }
    });

    if (!order) {
        return next(new AppError('Order not found', 404));
    }

    if (order.userId !== userId) {
        return next(new AppError('You do not have permission to cancel this order', 403));
    }

    if (order.status !== 'PENDING') {
        return next(new AppError('Cannot cancel order that is not pending', 400));
    }

    // Restore stock and update status
    await prisma.$transaction(async (tx) => {
        // Get order items to restore stock
        const orderItems = await tx.orderItem.findMany({
            where: { orderId: id }
        });

        for (const item of orderItems) {
            await tx.book.update({
                where: { id: item.bookId },
                data: { stock: { increment: item.quantity } }
            });
        }

        await tx.order.update({
            where: { id },
            data: { status: 'CANCELLED' }
        });
    });

    res.status(200).json({
        status: 'success',
        message: 'Order cancelled successfully'
    });
});

// Admin Controllers
export const getAllOrders = asyncHandler(async (req: Request, res: Response, next: NextFunction) => {
    const orders = await prisma.order.findMany({
        orderBy: { createdAt: 'desc' },
        include: {
            user: {
                select: { name: true, email: true }
            },
            items: {
                include: { book: true } // Don't include book details to keep response light if many orders? Maybe ok for now.
            }
        }
    });

    res.status(200).json({
        status: 'success',
        data: { orders }
    });
});

export const updateOrderStatus = asyncHandler(async (req: Request, res: Response, next: NextFunction) => {
    const { id } = req.params as { id: string };
    const { status, resi } = req.body;

    // Allowed status transitions could be validated here

    const order = await prisma.order.update({
        where: { id },
        data: {
            status,
            resi: resi || undefined,
            ...(status === 'SHIPPED' ? { shippedAt: new Date() } : {}),
            ...(status === 'DELIVERED' ? { deliveredAt: new Date() } : {}),
            ...(status === 'PAID' ? { paidAt: new Date() } : {}),
        }
    });

    res.status(200).json({
        status: 'success',
        data: { order }
    });
});



export const uploadPaymentProof = asyncHandler(async (req: Request, res: Response, next: NextFunction) => {
    const { id } = req.params as { id: string };
    const userId = (req as any).user.id;
    const paymentProof = req.body.paymentProof; // Set by middleware

    // Validate if file was uploaded
    if (!paymentProof) {
        return next(new AppError('No image uploaded', 400));
    }

    const order = await prisma.order.findUnique({
        where: { id }
    });

    if (!order) {
        return next(new AppError('Order not found', 404));
    }

    // Ensure user owns the order
    if (order.userId !== userId) {
        return next(new AppError('You do not have permission to upload proof for this order', 403));
    }

    // Update order with proof path
    const updatedOrder = await prisma.order.update({
        where: { id },
        data: { paymentProof }
    });

    res.status(200).json({
        status: 'success',
        data: { order: updatedOrder }
    });
});

export const deleteOrder = asyncHandler(async (req: Request, res: Response, next: NextFunction) => {
    const { id } = req.params as { id: string };

    // Transaction to delete order items first (if cascade is not set, but Prisma usually handles it if relation is configured)
    // However, we should be careful. If we delete order, items are deleted?
    // Let's check schema/relation behavior. Usually onDelete: Cascade.
    // Assuming Cascade or manual deletion.

    // Also consider stock restoration? 
    // "Bersihkan" might mean just delete the junk data. 
    // If order was PENDING/CANCELLED, stock might be held or not. 
    // If PENDING, stock was decremented. We should RESTORE it before deleting?
    // If PAID/SHIPPED/DELIVERED, stock is gone.
    // Let's restore stock if status is PENDING or PROCESSING? 
    // Or just simple delete? 
    // User said "hapus aja dan bersihkan", imply cleaning test data.
    // I will restore stock if PENDING/PROCESSING/PAID.

    const order = await prisma.order.findUnique({
        where: { id },
        include: { items: true }
    });

    if (!order) {
        return next(new AppError('Order not found', 404));
    }

    await prisma.$transaction(async (tx) => {
        // Restore stock for all items if order was not cancelled (since cancelled already restored)
        if (order.status !== 'CANCELLED') {
            for (const item of order.items) {
                await tx.book.update({
                    where: { id: item.bookId },
                    data: { stock: { increment: item.quantity } }
                });
            }
        }

        // Delete order (Cascade deletion of OrderItems should happen if schema is configured, otherwise delete items first)
        // Let's delete items explicitly to be safe
        await tx.orderItem.deleteMany({
            where: { orderId: id }
        });

        await tx.order.delete({
            where: { id }
        });
    });

    res.status(204).json({
        status: 'success',
        data: null
    });
});
