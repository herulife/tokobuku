import { Request, Response, NextFunction } from 'express';
import { PrismaClient } from '@prisma/client';
import { asyncHandler } from '../middlewares/asyncHandler';
import { AppError } from '../utils/AppError';

const prisma = new PrismaClient();

export const getSettings = asyncHandler(async (req: Request, res: Response, next: NextFunction) => {
    const settings = await prisma.setting.findMany();
    // Convert array to object key-value
    const settingsObj: any = {};
    settings.forEach(s => {
        settingsObj[s.key] = s.value;
    });

    res.status(200).json({
        status: 'success',
        data: { settings: settingsObj }
    });
});

export const updateSettings = asyncHandler(async (req: Request, res: Response, next: NextFunction) => {
    const { settings } = req.body; // Expects object { key: value, key2: value2 }

    if (!settings || typeof settings !== 'object') {
        return next(new AppError('Invalid settings data', 400));
    }

    const updates = Object.keys(settings).map(key => {
        return prisma.setting.upsert({
            where: { key },
            update: { value: String(settings[key]) },
            create: { key, value: String(settings[key]) }
        });
    });

    await Promise.all(updates);

    res.status(200).json({
        status: 'success',
        message: 'Settings updated successfully'
    });
});
