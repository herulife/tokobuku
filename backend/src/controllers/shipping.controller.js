const rajaOngkirService = require('../services/rajaongkir.service');

class ShippingController {
    // Get all provinces
    async getProvinces(req, res) {
        try {
            const result = await rajaOngkirService.getProvinces();

            res.json({
                success: true,
                data: result.rajaongkir.results
            });
        } catch (error) {
            res.status(500).json({
                success: false,
                message: error.message
            });
        }
    }

    // Get cities (optionally filtered by province)
    async getCities(req, res) {
        try {
            const { province_id } = req.query;
            const result = await rajaOngkirService.getCities(province_id);

            res.json({
                success: true,
                data: result.rajaongkir.results
            });
        } catch (error) {
            res.status(500).json({
                success: false,
                message: error.message
            });
        }
    }

    // Calculate shipping cost
    async calculateCost(req, res) {
        try {
            const { destination, weight, courier } = req.body;

            if (!destination || !weight || !courier) {
                return res.status(400).json({
                    success: false,
                    message: 'Destination, weight, and courier are required'
                });
            }

            const result = await rajaOngkirService.calculateCost(
                destination,
                weight,
                courier
            );

            res.json({
                success: true,
                data: result.rajaongkir.results
            });
        } catch (error) {
            res.status(500).json({
                success: false,
                message: error.message
            });
        }
    }
}

module.exports = new ShippingController();
