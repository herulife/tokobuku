import { Request, Response, NextFunction } from 'express';
import { PrismaClient, Prisma } from '@prisma/client';
import { AppError } from '../utils/AppError';
import { asyncHandler } from '../middlewares/asyncHandler';
import slugify from 'slugify';

const prisma = new PrismaClient();

export const getAllBooks = asyncHandler(async (req: Request, res: Response, next: NextFunction) => {
    const {
        page = 1,
        limit = 10,
        sort,
        search,
        category,
        minPrice,
        maxPrice,
        inStock,
    } = req.query;

    const pageNum = Number(page);
    const limitNum = Number(limit);
    const skip = (pageNum - 1) * limitNum;

    const where: Prisma.BookWhereInput = {};

    if (search) {
        where.OR = [
            { title: { contains: String(search) } },
            { author: { contains: String(search) } },
        ];
    }

    if (category) {
        where.category = {
            slug: String(category),
        };
    }

    if (minPrice || maxPrice) {
        where.price = {};
        if (minPrice) where.price.gte = Number(minPrice);
        if (maxPrice) where.price.lte = Number(maxPrice);
    }

    if (inStock === 'true') {
        where.stock = { gt: 0 };
    }

    const orderBy: Prisma.BookOrderByWithRelationInput = {};
    if (sort) {
        const [field, direction] = String(sort).split(':');
        if (field === 'price') orderBy.price = direction === 'desc' ? 'desc' : 'asc';
        if (field === 'rating') orderBy.rating = direction === 'desc' ? 'desc' : 'asc';
        if (field === 'newest') orderBy.createdAt = 'desc';
    } else {
        orderBy.createdAt = 'desc';
    }

    const [books, total] = await Promise.all([
        prisma.book.findMany({
            where,
            skip,
            take: limitNum,
            orderBy,
            include: { category: true },
        }),
        prisma.book.count({ where }),
    ]);

    res.status(200).json({
        status: 'success',
        results: books.length,
        total,
        totalPages: Math.ceil(total / limitNum),
        currentPage: pageNum,
        data: { books },
    });
});

export const getBook = asyncHandler(async (req: Request, res: Response, next: NextFunction) => {
    const { id } = req.params;
    const bookId = String(id); // Convert to string for Prisma

    // Check if it's a slug (looks like slug-string) or CUID/UUID
    // For simplicity, we can try both or assume slug if not CUID-like
    // But explicit route separation is better. Here we assume ID first, then try slug if logic allows, 
    // but better to have separate endpoint for slug. 
    // The prompt asked for /books/:id and /books/slug/:slug separately.

    const book = await prisma.book.findUnique({
        where: { id: bookId },
        include: { category: true },
    });

    if (!book) {
        return next(new AppError('No book found with that ID', 404));
    }

    res.status(200).json({
        status: 'success',
        data: { book },
    });
});

export const getBookBySlug = asyncHandler(async (req: Request, res: Response, next: NextFunction) => {
    const { slug: paramSlug } = req.params;
    const slug = String(paramSlug); // Convert to string for Prisma

    const book = await prisma.book.findUnique({
        where: { slug },
        include: { category: true },
    });

    if (!book) {
        return next(new AppError('No book found with that slug', 404));
    }

    res.status(200).json({
        status: 'success',
        data: { book },
    });
});

export const createBook = asyncHandler(async (req: Request, res: Response, next: NextFunction) => {
    const {
        title,
        author,
        publisher,
        isbn,
        description,
        price,
        stock,
        weight,
        coverImage,
        categoryId,
        pages,
        language
    } = req.body;

    const bookData: any = {
        title,
        author,
        publisher,
        isbn,
        description,
        price: Number(price),
        stock: Number(stock),
        weight: weight ? Number(weight) : 300,
        coverImage,
        pages: pages ? Number(pages) : undefined,
        language,
        categoryId: categoryId && typeof categoryId === 'string' ? categoryId : undefined
    };

    // Auto generate slug if not provided
    if (!req.body.slug && title) {
        bookData.slug = slugify(title, { lower: true, strict: true });
    }

    const newBook = await prisma.book.create({
        data: bookData,
    });

    res.status(201).json({
        status: 'success',
        data: { book: newBook },
    });
});

export const updateBook = asyncHandler(async (req: Request, res: Response, next: NextFunction) => {
    const { id } = req.params;
    const bookId = String(id); // Convert to string for Prisma
    const {
        title,
        author,
        publisher,
        isbn,
        description,
        price,
        discountPrice,
        stock,
        coverImage,
        samplePdf,
        categoryId,
        isPreorder,
        preorderDate,
        pages,
        language,
        weight
    } = req.body;

    const data: any = {
        title,
        author,
        publisher,
        isbn,
        description,
        price: price ? Number(price) : undefined,
        discountPrice: discountPrice ? Number(discountPrice) : undefined,
        stock: stock ? Number(stock) : undefined,
        coverImage,
        samplePdf,
        isPreorder: isPreorder !== undefined ? Boolean(isPreorder) : undefined,
        preorderDate: preorderDate ? new Date(preorderDate) : undefined,
        rating: req.body.rating ? Number(req.body.rating) : undefined,
        totalRating: req.body.totalRating ? Number(req.body.totalRating) : undefined,
        pages: pages ? Number(pages) : undefined,
        language,
        weight: weight ? Number(weight) : undefined
    };

    // Only add categoryId if it's provided and not null/undefined/object
    if (categoryId && typeof categoryId === 'string') {
        data.categoryId = categoryId;
    }

    if (data.title && !req.body.slug) {
        data.slug = slugify(data.title, { lower: true, strict: true });
    }

    // Remove undefined keys
    Object.keys(data).forEach(key => data[key] === undefined && delete data[key]);

    const updatedBook = await prisma.book.update({
        where: { id: bookId },
        data,
    });

    if (!updatedBook) {
        return next(new AppError('No book found with that ID', 404));
    }

    res.status(200).json({
        status: 'success',
        data: { book: updatedBook },
    });
});

export const deleteBook = asyncHandler(async (req: Request, res: Response, next: NextFunction) => {
    const { id } = req.params;
    const bookId = String(id); // Convert to string for Prisma

    // Check if book has orders
    const inOrder = await prisma.orderItem.findFirst({
        where: { bookId }
    });

    if (inOrder) {
        return next(new AppError('Buku tidak dapat dihapus karena memiliki riwayat pesanan. Non-aktifkan stok saja.', 400));
    }

    await prisma.book.delete({
        where: { id: bookId },
    });

    res.status(204).json({
        status: 'success',
        data: null,
    });
});

export const deleteBulkBooks = asyncHandler(async (req: Request, res: Response, next: NextFunction) => {
    const { ids } = req.body;

    if (!ids || !Array.isArray(ids) || ids.length === 0) {
        return next(new AppError('Please provide an array of IDs to delete', 400));
    }

    // Check for books in orders
    const booksInOrders = await prisma.orderItem.findMany({
        where: {
            bookId: { in: ids }
        },
        select: { bookId: true },
        distinct: ['bookId']
    });

    const nonDeletableIds = booksInOrders.map(b => b.bookId);
    const deletableIds = ids.filter((id: string) => !nonDeletableIds.includes(id));

    let deletedCount = 0;
    if (deletableIds.length > 0) {
        const result = await prisma.book.deleteMany({
            where: {
                id: { in: deletableIds }
            }
        });
        deletedCount = result.count;
    }

    if (nonDeletableIds.length > 0) {
        return res.status(200).json({
            status: 'success',
            message: `${deletedCount} buku dihapus. ${nonDeletableIds.length} buku tidak bisa dihapus karena ada di pesanan.`,
            data: {
                deleted: deletableIds,
                failed: nonDeletableIds
            }
        });
    }

    res.status(200).json({
        status: 'success',
        message: `${deletedCount} buku berhasil dihapus`
    });
});
