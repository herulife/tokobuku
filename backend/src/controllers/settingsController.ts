import { Request, Response } from 'express';
import prisma from '../lib/prisma';

class SettingsController {
    // Get all settings
    async getAllSettings(req: Request, res: Response) {
        try {
            const settings = await prisma.setting.findMany();

            // Convert to key-value object
            const settingsObj: Record<string, string> = {};
            settings.forEach(setting => {
                settingsObj[setting.key] = setting.value;
            });

            res.json({
                success: true,
                data: settingsObj
            });
        } catch (error: any) {
            res.status(500).json({
                success: false,
                message: error.message
            });
        }
    }

    // Get public settings (no auth required)
    async getPublicSettings(req: Request, res: Response) {
        try {
            const publicKeys = ['bank_name', 'account_number', 'account_holder', 'whatsapp_number'];
            const settings = await prisma.setting.findMany({
                where: {
                    key: { in: publicKeys }
                }
            });

            const settingsObj: Record<string, string> = {};
            settings.forEach(setting => {
                settingsObj[setting.key] = setting.value;
            });

            res.json({
                success: true,
                data: settingsObj
            });
        } catch (error: any) {
            res.status(500).json({
                success: false,
                message: error.message
            });
        }
    }

    // Get specific setting
    async getSetting(req: Request, res: Response) {
        try {
            const { key } = req.params;

            if (typeof key !== 'string') {
                return res.status(400).json({
                    success: false,
                    message: 'Invalid key parameter'
                });
            }

            const setting = await prisma.setting.findUnique({
                where: { key }
            });

            if (!setting) {
                return res.status(404).json({
                    success: false,
                    message: 'Setting not found'
                });
            }

            res.json({
                success: true,
                data: {
                    key: setting.key,
                    value: setting.value
                }
            });
        } catch (error: any) {
            res.status(500).json({
                success: false,
                message: error.message
            });
        }
    }

    // Update settings (batch)
    async updateSettings(req: Request, res: Response) {
        try {
            const settings = req.body; // { key1: value1, key2: value2, ... }

            const updates = [];
            for (const [key, value] of Object.entries(settings)) {
                updates.push(
                    prisma.setting.upsert({
                        where: { key },
                        update: { value: String(value) },
                        create: { key, value: String(value) }
                    })
                );
            }

            await Promise.all(updates);

            res.json({
                success: true,
                message: 'Settings updated successfully'
            });
        } catch (error: any) {
            res.status(500).json({
                success: false,
                message: error.message
            });
        }
    }

    // Update single setting
    async updateSetting(req: Request, res: Response) {
        try {
            const { key } = req.params;
            const { value } = req.body;

            if (typeof key !== 'string') {
                return res.status(400).json({
                    success: false,
                    message: 'Invalid key parameter'
                });
            }

            const setting = await prisma.setting.upsert({
                where: { key },
                update: { value: String(value) },
                create: { key, value: String(value) }
            });

            res.json({
                success: true,
                data: setting
            });
        } catch (error: any) {
            res.status(500).json({
                success: false,
                message: error.message
            });
        }
    }

    // Delete setting
    async deleteSetting(req: Request, res: Response) {
        try {
            const { key } = req.params;

            if (typeof key !== 'string') {
                return res.status(400).json({
                    success: false,
                    message: 'Invalid key parameter'
                });
            }

            await prisma.setting.delete({
                where: { key }
            });

            res.json({
                success: true,
                message: 'Setting deleted successfully'
            });
        } catch (error: any) {
            res.status(500).json({
                success: false,
                message: error.message
            });
        }
    }
}

export default new SettingsController();
