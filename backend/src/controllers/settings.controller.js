const prisma = require('../config/database');

class SettingsController {
    // Get all settings
    async getAllSettings(req, res) {
        try {
            const settings = await prisma.setting.findMany();

            // Convert to key-value object
            const settingsObj = {};
            settings.forEach(setting => {
                settingsObj[setting.key] = setting.value;
            });

            res.json({
                success: true,
                data: settingsObj
            });
        } catch (error) {
            res.status(500).json({
                success: false,
                message: error.message
            });
        }
    }

    // Get specific setting
    async getSetting(req, res) {
        try {
            const { key } = req.params;
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
        } catch (error) {
            res.status(500).json({
                success: false,
                message: error.message
            });
        }
    }

    // Update settings (batch)
    async updateSettings(req, res) {
        try {
            const settings = req.body; // { key1: value1, key2: value2, ... }

            const updates = [];
            for (const [key, value] of Object.entries(settings)) {
                updates.push(
                    prisma.setting.upsert({
                        where: { key },
                        update: { value: value.toString() },
                        create: { key, value: value.toString() }
                    })
                );
            }

            await Promise.all(updates);

            res.json({
                success: true,
                message: 'Settings updated successfully'
            });
        } catch (error) {
            res.status(500).json({
                success: false,
                message: error.message
            });
        }
    }

    // Update single setting
    async updateSetting(req, res) {
        try {
            const { key } = req.params;
            const { value } = req.body;

            const setting = await prisma.setting.upsert({
                where: { key },
                update: { value: value.toString() },
                create: { key, value: value.toString() }
            });

            res.json({
                success: true,
                data: setting
            });
        } catch (error) {
            res.status(500).json({
                success: false,
                message: error.message
            });
        }
    }

    // Delete setting
    async deleteSetting(req, res) {
        try {
            const { key } = req.params;

            await prisma.setting.delete({
                where: { key }
            });

            res.json({
                success: true,
                message: 'Setting deleted successfully'
            });
        } catch (error) {
            res.status(500).json({
                success: false,
                message: error.message
            });
        }
    }
}

module.exports = new SettingsController();
