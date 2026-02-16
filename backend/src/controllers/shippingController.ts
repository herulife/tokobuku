import { Request, Response } from 'express';
import binderByteService from '../services/binderbyte.service';
import prisma from '../lib/prisma';

class ShippingController {
    // Replaced getProvinces with searchDestination
    async searchDestination(req: Request, res: Response) {
        try {
            const { keyword } = req.query;
            if (!keyword || typeof keyword !== 'string' || keyword.length < 3) {
                return res.json({ success: true, data: [] });
            }

            const data = await binderByteService.searchDestination(keyword);
            res.json({
                success: true,
                data: data
            });
        } catch (error: any) {
            console.error('Error in searchDestination:', error.message);
            const status = error.response?.status || 500;
            const message = error.response?.data?.meta?.message || error.message || 'Internal Server Error';

            res.status(status).json({
                success: false,
                message: message
            });
        }
    }

    // Keep getCities for backward compatibility but it handles nothing or search? 
    // We will direct route /provinces and /cities to fail or strict usage.
    async getProvinces(req: Request, res: Response) {
        res.json({ success: true, data: [] });
    }

    async getCities(req: Request, res: Response) {
        res.json({ success: true, data: [] });
    }

    async calculateCost(req: Request, res: Response) {
        try {
            let { origin, destination, weight, courier } = req.body;

            // Hardcoded origin: Jakarta Timur (since we use custom shipping calculation)
            if (!origin) {
                origin = '3172'; // Jakarta Timur city ID
            }

            // Validation
            if (!destination || !weight || !courier) {
                return res.status(400).json({
                    success: false,
                    message: `Missing required fields: destination, weight, courier`
                });
            }

            const result = await binderByteService.calculateCost(
                origin,
                destination,
                Number(weight),
                courier
            );

            res.json({
                success: true,
                data: result
            });
        } catch (error: any) {
            console.error('Error in calculateCost:', error);
            res.status(500).json({
                success: false,
                message: error.message || 'Failed to calculate shipping cost'
            });
        }
    }
    async checkConnection(req: Request, res: Response) {
        try {
            // Test connection by attempting a simple search
            const testResult = await binderByteService.searchDestination('Jakarta');
            if (testResult && testResult.length >= 0) {
                return res.json({ success: true, message: 'Connection successful' });
            } else {
                return res.status(400).json({ success: false, message: 'Connection failed' });
            }
        } catch (error: any) {
            return res.status(500).json({ success: false, message: error.message });
        }
    }
}

export default new ShippingController();
