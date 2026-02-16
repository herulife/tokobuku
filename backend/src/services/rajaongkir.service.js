const axios = require('axios');
const prisma = require('../config/database');

class RajaOngkirService {
    constructor() {
        this.baseURL = 'https://api.rajaongkir.com/starter';
        this.apiKey = null;
    }

    async loadSettings() {
        try {
            const apiKeySetting = await prisma.setting.findUnique({
                where: { key: 'rajaongkir_api_key' }
            });
            this.apiKey = apiKeySetting?.value || null;
        } catch (error) {
            console.error('Failed to load RajaOngkir settings:', error);
        }
    }

    async getHeaders() {
        if (!this.apiKey) {
            await this.loadSettings();
        }
        if (!this.apiKey) {
            throw new Error('RajaOngkir API key not configured');
        }
        return {
            'key': this.apiKey,
            'content-type': 'application/x-www-form-urlencoded'
        };
    }

    async getProvinces() {
        try {
            const headers = await this.getHeaders();
            const response = await axios.get(`${this.baseURL}/province`, { headers });
            return response.data;
        } catch (error) {
            throw new Error(`Failed to fetch provinces: ${error.message}`);
        }
    }

    async getCities(provinceId = null) {
        try {
            const headers = await this.getHeaders();
            const url = provinceId
                ? `${this.baseURL}/city?province=${provinceId}`
                : `${this.baseURL}/city`;
            const response = await axios.get(url, { headers });
            return response.data;
        } catch (error) {
            throw new Error(`Failed to fetch cities: ${error.message}`);
        }
    }

    async calculateCost(destination, weight, courier) {
        try {
            const headers = await this.getHeaders();

            // Get origin city from settings
            const originSetting = await prisma.setting.findUnique({
                where: { key: 'rajaongkir_origin_city_id' }
            });

            if (!originSetting) {
                throw new Error('Origin city not configured');
            }

            const origin = originSetting.value;

            const data = new URLSearchParams({
                origin: origin,
                destination: destination,
                weight: weight.toString(),
                courier: courier.toLowerCase()
            });

            const response = await axios.post(
                `${this.baseURL}/cost`,
                data,
                { headers }
            );

            return response.data;
        } catch (error) {
            throw new Error(`Failed to calculate shipping cost: ${error.message}`);
        }
    }

    async getSettings() {
        try {
            const settings = await prisma.setting.findMany({
                where: {
                    key: {
                        in: ['rajaongkir_api_key', 'rajaongkir_origin_city_id', 'default_book_weight']
                    }
                }
            });

            const settingsMap = {};
            settings.forEach(setting => {
                settingsMap[setting.key] = setting.value;
            });

            return settingsMap;
        } catch (error) {
            throw new Error(`Failed to fetch settings: ${error.message}`);
        }
    }
}

module.exports = new RajaOngkirService();
