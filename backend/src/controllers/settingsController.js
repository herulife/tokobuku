"use strict";
var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
var __generator = (this && this.__generator) || function (thisArg, body) {
    var _ = { label: 0, sent: function() { if (t[0] & 1) throw t[1]; return t[1]; }, trys: [], ops: [] }, f, y, t, g = Object.create((typeof Iterator === "function" ? Iterator : Object).prototype);
    return g.next = verb(0), g["throw"] = verb(1), g["return"] = verb(2), typeof Symbol === "function" && (g[Symbol.iterator] = function() { return this; }), g;
    function verb(n) { return function (v) { return step([n, v]); }; }
    function step(op) {
        if (f) throw new TypeError("Generator is already executing.");
        while (g && (g = 0, op[0] && (_ = 0)), _) try {
            if (f = 1, y && (t = op[0] & 2 ? y["return"] : op[0] ? y["throw"] || ((t = y["return"]) && t.call(y), 0) : y.next) && !(t = t.call(y, op[1])).done) return t;
            if (y = 0, t) op = [op[0] & 2, t.value];
            switch (op[0]) {
                case 0: case 1: t = op; break;
                case 4: _.label++; return { value: op[1], done: false };
                case 5: _.label++; y = op[1]; op = [0]; continue;
                case 7: op = _.ops.pop(); _.trys.pop(); continue;
                default:
                    if (!(t = _.trys, t = t.length > 0 && t[t.length - 1]) && (op[0] === 6 || op[0] === 2)) { _ = 0; continue; }
                    if (op[0] === 3 && (!t || (op[1] > t[0] && op[1] < t[3]))) { _.label = op[1]; break; }
                    if (op[0] === 6 && _.label < t[1]) { _.label = t[1]; t = op; break; }
                    if (t && _.label < t[2]) { _.label = t[2]; _.ops.push(op); break; }
                    if (t[2]) _.ops.pop();
                    _.trys.pop(); continue;
            }
            op = body.call(thisArg, _);
        } catch (e) { op = [6, e]; y = 0; } finally { f = t = 0; }
        if (op[0] & 5) throw op[1]; return { value: op[0] ? op[1] : void 0, done: true };
    }
};
Object.defineProperty(exports, "__esModule", { value: true });
var prisma_js_1 = require("../lib/prisma.js");
var SettingsController = /** @class */ (function () {
    function SettingsController() {
    }
    // Get all settings
    SettingsController.prototype.getAllSettings = function (req, res) {
        return __awaiter(this, void 0, void 0, function () {
            var settings, settingsObj_1, error_1;
            return __generator(this, function (_a) {
                switch (_a.label) {
                    case 0:
                        _a.trys.push([0, 2, , 3]);
                        return [4 /*yield*/, prisma_js_1.default.setting.findMany()];
                    case 1:
                        settings = _a.sent();
                        settingsObj_1 = {};
                        settings.forEach(function (setting) {
                            settingsObj_1[setting.key] = setting.value;
                        });
                        res.json({
                            success: true,
                            data: settingsObj_1
                        });
                        return [3 /*break*/, 3];
                    case 2:
                        error_1 = _a.sent();
                        res.status(500).json({
                            success: false,
                            message: error_1.message
                        });
                        return [3 /*break*/, 3];
                    case 3: return [2 /*return*/];
                }
            });
        });
    };
    // Get public settings (no auth required)
    SettingsController.prototype.getPublicSettings = function (req, res) {
        return __awaiter(this, void 0, void 0, function () {
            var publicKeys, settings, settingsObj_2, error_2;
            return __generator(this, function (_a) {
                switch (_a.label) {
                    case 0:
                        _a.trys.push([0, 2, , 3]);
                        publicKeys = ['bank_name', 'account_number', 'account_holder', 'whatsapp_number'];
                        return [4 /*yield*/, prisma_js_1.default.setting.findMany({
                                where: {
                                    key: { in: publicKeys }
                                }
                            })];
                    case 1:
                        settings = _a.sent();
                        settingsObj_2 = {};
                        settings.forEach(function (setting) {
                            settingsObj_2[setting.key] = setting.value;
                        });
                        res.json({
                            success: true,
                            data: settingsObj_2
                        });
                        return [3 /*break*/, 3];
                    case 2:
                        error_2 = _a.sent();
                        res.status(500).json({
                            success: false,
                            message: error_2.message
                        });
                        return [3 /*break*/, 3];
                    case 3: return [2 /*return*/];
                }
            });
        });
    };
    // Get specific setting
    SettingsController.prototype.getSetting = function (req, res) {
        return __awaiter(this, void 0, void 0, function () {
            var key, setting, error_3;
            return __generator(this, function (_a) {
                switch (_a.label) {
                    case 0:
                        _a.trys.push([0, 2, , 3]);
                        key = req.params.key;
                        if (typeof key !== 'string') {
                            return [2 /*return*/, res.status(400).json({
                                    success: false,
                                    message: 'Invalid key parameter'
                                })];
                        }
                        return [4 /*yield*/, prisma_js_1.default.setting.findUnique({
                                where: { key: key }
                            })];
                    case 1:
                        setting = _a.sent();
                        if (!setting) {
                            return [2 /*return*/, res.status(404).json({
                                    success: false,
                                    message: 'Setting not found'
                                })];
                        }
                        res.json({
                            success: true,
                            data: {
                                key: setting.key,
                                value: setting.value
                            }
                        });
                        return [3 /*break*/, 3];
                    case 2:
                        error_3 = _a.sent();
                        res.status(500).json({
                            success: false,
                            message: error_3.message
                        });
                        return [3 /*break*/, 3];
                    case 3: return [2 /*return*/];
                }
            });
        });
    };
    // Update settings (batch)
    SettingsController.prototype.updateSettings = function (req, res) {
        return __awaiter(this, void 0, void 0, function () {
            var settings, updates, _i, _a, _b, key, value, error_4;
            return __generator(this, function (_c) {
                switch (_c.label) {
                    case 0:
                        _c.trys.push([0, 2, , 3]);
                        settings = req.body;
                        updates = [];
                        for (_i = 0, _a = Object.entries(settings); _i < _a.length; _i++) {
                            _b = _a[_i], key = _b[0], value = _b[1];
                            updates.push(prisma_js_1.default.setting.upsert({
                                where: { key: key },
                                update: { value: String(value) },
                                create: { key: key, value: String(value) }
                            }));
                        }
                        return [4 /*yield*/, Promise.all(updates)];
                    case 1:
                        _c.sent();
                        res.json({
                            success: true,
                            message: 'Settings updated successfully'
                        });
                        return [3 /*break*/, 3];
                    case 2:
                        error_4 = _c.sent();
                        res.status(500).json({
                            success: false,
                            message: error_4.message
                        });
                        return [3 /*break*/, 3];
                    case 3: return [2 /*return*/];
                }
            });
        });
    };
    // Update single setting
    SettingsController.prototype.updateSetting = function (req, res) {
        return __awaiter(this, void 0, void 0, function () {
            var key, value, setting, error_5;
            return __generator(this, function (_a) {
                switch (_a.label) {
                    case 0:
                        _a.trys.push([0, 2, , 3]);
                        key = req.params.key;
                        value = req.body.value;
                        if (typeof key !== 'string') {
                            return [2 /*return*/, res.status(400).json({
                                    success: false,
                                    message: 'Invalid key parameter'
                                })];
                        }
                        return [4 /*yield*/, prisma_js_1.default.setting.upsert({
                                where: { key: key },
                                update: { value: String(value) },
                                create: { key: key, value: String(value) }
                            })];
                    case 1:
                        setting = _a.sent();
                        res.json({
                            success: true,
                            data: setting
                        });
                        return [3 /*break*/, 3];
                    case 2:
                        error_5 = _a.sent();
                        res.status(500).json({
                            success: false,
                            message: error_5.message
                        });
                        return [3 /*break*/, 3];
                    case 3: return [2 /*return*/];
                }
            });
        });
    };
    // Delete setting
    SettingsController.prototype.deleteSetting = function (req, res) {
        return __awaiter(this, void 0, void 0, function () {
            var key, error_6;
            return __generator(this, function (_a) {
                switch (_a.label) {
                    case 0:
                        _a.trys.push([0, 2, , 3]);
                        key = req.params.key;
                        if (typeof key !== 'string') {
                            return [2 /*return*/, res.status(400).json({
                                    success: false,
                                    message: 'Invalid key parameter'
                                })];
                        }
                        return [4 /*yield*/, prisma_js_1.default.setting.delete({
                                where: { key: key }
                            })];
                    case 1:
                        _a.sent();
                        res.json({
                            success: true,
                            message: 'Setting deleted successfully'
                        });
                        return [3 /*break*/, 3];
                    case 2:
                        error_6 = _a.sent();
                        res.status(500).json({
                            success: false,
                            message: error_6.message
                        });
                        return [3 /*break*/, 3];
                    case 3: return [2 /*return*/];
                }
            });
        });
    };
    return SettingsController;
}());
exports.default = new SettingsController();
