import { Request, Response, NextFunction } from 'express';
import { PrismaClient } from '@prisma/client';
import { asyncHandler } from '../middlewares/asyncHandler.js';
import { AppError } from '../utils/AppError.js';
const prisma = new PrismaClient();

const slugify = (text: string) => {
    return text.toString().toLowerCase()
        .replace(/\s+/g, '-')           // Replace spaces with -
        .replace(/[^\w\-]+/g, '')       // Remove all non-word chars
        .replace(/\-\-+/g, '-')         // Replace multiple - with single -
        .replace(/^-+/, '')             // Trim - from start of text
        .replace(/-+$/, '');            // Trim - from end of text
};

export const getAllCategories = asyncHandler(async (req: Request, res: Response, next: NextFunction) => {
    const categories = await prisma.category.findMany({
        orderBy: { name: 'asc' },
        include: {
            _count: {
                select: { books: true }
            }
        }
    });

    res.status(200).json({
        status: 'success',
        results: categories.length,
        data: { categories },
    });
});

export const createCategory = asyncHandler(async (req: Request, res: Response, next: NextFunction) => {
    const { name } = req.body;

    if (!name) {
        return next(new AppError('Category name is required', 400));
    }

    const slug = slugify(name);

    const existingCategory = await prisma.category.findUnique({
        where: { slug }
    });

    if (existingCategory) {
        return next(new AppError('Category already exists', 400));
    }

    const category = await prisma.category.create({
        data: { name, slug }
    });

    res.status(201).json({
        status: 'success',
        data: { category },
    });
});

export const updateCategory = asyncHandler(async (req: Request, res: Response, next: NextFunction) => {
    const { id } = req.params as { id: string };
    const { name } = req.body as { name: string };

    if (!name) {
        return next(new AppError('Category name is required', 400));
    }

    const slug = slugify(name);

    // Check if another category has this slug
    const existingCategory = await prisma.category.findUnique({
        where: { slug }
    });

    if (existingCategory && existingCategory.id !== id) {
        return next(new AppError('Category name already exists', 400));
    }

    const category = await prisma.category.update({
        where: { id },
        data: { name, slug }
    });

    res.status(200).json({
        status: 'success',
        data: { category },
    });
});

export const deleteCategory = asyncHandler(async (req: Request, res: Response, next: NextFunction) => {
    const { id } = req.params as { id: string };

    // Check if category exists
    const category: any = await prisma.category.findUnique({
        where: { id },
        include: {
            _count: {
                select: { books: true }
            }
        }
    });

    if (!category) {
        return next(new AppError('Category not found', 404));
    }

    if (category._count.books > 0) {
        return next(new AppError('Cannot delete category with associated books', 400));
    }

    await prisma.category.delete({
        where: { id }
    });

    res.status(204).json({
        status: 'success',
        data: null,
    });
});
