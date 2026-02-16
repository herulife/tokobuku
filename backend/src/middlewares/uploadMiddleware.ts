
import multer from 'multer';
import sharp from 'sharp';
import fs from 'fs';
import path from 'path';
import { Request, Response, NextFunction } from 'express';
import { AppError } from '../utils/AppError';

// Ensure upload directory exists
const uploadDir = 'public/uploads';
if (!fs.existsSync(uploadDir)) {
    fs.mkdirSync(uploadDir, { recursive: true });
}

// Multer Storage (Memory for processing)
const storage = multer.memoryStorage();

// Multer Filter
const multerFilter = (req: Request, file: Express.Multer.File, cb: multer.FileFilterCallback) => {
    if (file.mimetype.startsWith('image')) {
        cb(null, true);
    } else {
        cb(new AppError('Not an image! Please upload only images.', 400) as any, false);
    }
};

export const upload = multer({
    storage: storage,
    fileFilter: multerFilter
});

export const resizeImage = async (req: Request, res: Response, next: NextFunction) => {
    if (!req.file) return next();

    // Filename: book-{timestamp}-{random}.webp
    const filename = `book-${Date.now()}-${Math.round(Math.random() * 1E9)}.webp`;
    const filepath = path.join(uploadDir, filename);

    try {
        await sharp(req.file.buffer)
            .resize(800, 1200, { // Standard book cover ratio 2:3, somewhat high res
                fit: 'cover',
                withoutEnlargement: true
            })
            .toFormat('webp')
            .webp({ quality: 80 })
            .toFile(filepath);

        req.body.coverImage = `/uploads/${filename}`;
        next();
    } catch (error) {
        next(new AppError('Error processing image', 500));
    }
};

export const processPaymentProof = async (req: Request, res: Response, next: NextFunction) => {
    if (!req.file) return next();

    const filename = `proof-${Date.now()}-${Math.round(Math.random() * 1E9)}.webp`;
    const filepath = path.join(uploadDir, filename);

    try {
        await sharp(req.file.buffer)
            .resize(1000, 1000, {
                fit: 'inside',
                withoutEnlargement: true
            })
            .toFormat('webp')
            .webp({ quality: 80 })
            .toFile(filepath);

        req.body.paymentProof = `/uploads/${filename}`;
        next();
    } catch (error) {
        next(new AppError('Error processing image', 500));
    }
};
