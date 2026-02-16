import { Request, Response, NextFunction } from 'express';
import { PrismaClient, Prisma } from '@prisma/client';
import bcrypt from 'bcrypt';
import { asyncHandler } from '../middlewares/asyncHandler';
import { AppError } from '../utils/AppError';

const prisma = new PrismaClient();

export const updateProfile = asyncHandler(async (req: Request, res: Response, next: NextFunction) => {
    const userId = (req as any).user.id;
    const { name, password, confirmPassword } = req.body;

    const dataToUpdate: any = { name };

    if (password) {
        if (password !== confirmPassword) {
            return next(new AppError('Konfirmasi password tidak cocok', 400));
        }
        dataToUpdate.password = await bcrypt.hash(password, 12);
    }

    const updatedUser = await prisma.user.update({
        where: { id: userId },
        data: dataToUpdate,
        select: {
            id: true,
            name: true,
            email: true,
            role: true,
            avatar: true,
        },
    });

    res.status(200).json({
        status: 'success',
        data: {
            user: updatedUser,
        },
    });
});

// Admin Controllers
export const getAllUsers = asyncHandler(async (req: Request, res: Response, next: NextFunction) => {
    const { page = 1, limit = 10, search } = req.query;
    const pageNum = Number(page);
    const limitNum = Number(limit);
    const skip = (pageNum - 1) * limitNum;

    const where: Prisma.UserWhereInput = {};

    if (search) {
        where.OR = [
            { name: { contains: String(search) } }, // Remove mode: insensitive for SQLite if needed, but Prisma usually handles it. Wait, SQLite does NOT support mode insensitive in older versions, but Prisma client polyfills it? No.
            // For SQLite, contains is case insensitive by default for ASCII but not unicode?
            // Let's stick to standard contains for now. If issues arise, we valid.
            { email: { contains: String(search) } },
        ];
    }

    const [users, total] = await Promise.all([
        prisma.user.findMany({
            where,
            skip,
            take: limitNum,
            orderBy: { createdAt: 'desc' },
            select: {
                id: true,
                name: true,
                email: true,
                role: true,
                createdAt: true,
                _count: {
                    select: { orders: true }
                }
            }
        }),
        prisma.user.count({ where })
    ]);

    res.status(200).json({
        status: 'success',
        results: users.length,
        total,
        totalPages: Math.ceil(total / limitNum),
        currentPage: pageNum,
        data: { users }
    });
});

export const updateUserRole = asyncHandler(async (req: Request, res: Response, next: NextFunction) => {
    const { id } = req.params;
    const userId = String(id); // Convert to string for Prisma
    const { role } = req.body;

    if (!['USER', 'ADMIN', 'SUPER_ADMIN'].includes(role)) {
        return next(new AppError('Role invalid', 400));
    }

    const user = await prisma.user.update({
        where: { id: userId },
        data: { role },
        select: { id: true, name: true, email: true, role: true }
    });

    res.status(200).json({
        status: 'success',
        data: { user }
    });
});

export const createUser = asyncHandler(async (req: Request, res: Response, next: NextFunction) => {
    const { name, email, password, role } = req.body;

    const existingUser = await prisma.user.findUnique({ where: { email: String(email) } });
    if (existingUser) {
        return next(new AppError('Email already registered', 400));
    }

    const hashedPassword = await bcrypt.hash(String(password), 12);

    const newUser = await prisma.user.create({
        data: {
            name: String(name),
            email: String(email),
            password: hashedPassword,
            role: String(role || 'USER')
        },
        select: {
            id: true,
            name: true,
            email: true,
            role: true,
            createdAt: true
        }
    });

    res.status(201).json({
        status: 'success',
        data: { user: newUser }
    });
});


export const deleteUser = asyncHandler(async (req: Request, res: Response, next: NextFunction) => {
    const { id } = req.params;
    const userId = String(id); // Convert to string for Prisma

    // Prevent deleting self? Maybe.
    const currentUserId = (req as any).user.id;
    if (userId === currentUserId) {
        return next(new AppError('Cannot delete yourself', 400));
    }

    await prisma.user.delete({
        where: { id: userId }
    });

    res.status(204).json({
        status: 'success',
        data: null
    });
});
