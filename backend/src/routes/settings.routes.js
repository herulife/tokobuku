const express = require('express');
const router = express.Router();
const settingsController = require('../controllers/settings.controller');
const { authenticate, authorize } = require('../middlewares/auth.middleware');

// All settings routes require admin authentication
router.use(authenticate, authorize('ADMIN'));

router.get('/', settingsController.getAllSettings);
router.get('/:key', settingsController.getSetting);
router.put('/', settingsController.updateSettings);
router.put('/:key', settingsController.updateSetting);
router.delete('/:key', settingsController.deleteSetting);

module.exports = router;
