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
var binderbyte_service_js_1 = require("../services/binderbyte.service.js");
var ShippingController = /** @class */ (function () {
    function ShippingController() {
    }
    // Replaced getProvinces with searchDestination
    ShippingController.prototype.searchDestination = function (req, res) {
        return __awaiter(this, void 0, void 0, function () {
            var keyword, data, error_1, status_1, message;
            var _a, _b, _c, _d;
            return __generator(this, function (_e) {
                switch (_e.label) {
                    case 0:
                        _e.trys.push([0, 2, , 3]);
                        keyword = req.query.keyword;
                        if (!keyword || typeof keyword !== 'string' || keyword.length < 3) {
                            return [2 /*return*/, res.json({ success: true, data: [] })];
                        }
                        return [4 /*yield*/, binderbyte_service_js_1.default.searchDestination(keyword)];
                    case 1:
                        data = _e.sent();
                        res.json({
                            success: true,
                            data: data
                        });
                        return [3 /*break*/, 3];
                    case 2:
                        error_1 = _e.sent();
                        console.error('Error in searchDestination:', error_1.message);
                        status_1 = ((_a = error_1.response) === null || _a === void 0 ? void 0 : _a.status) || 500;
                        message = ((_d = (_c = (_b = error_1.response) === null || _b === void 0 ? void 0 : _b.data) === null || _c === void 0 ? void 0 : _c.meta) === null || _d === void 0 ? void 0 : _d.message) || error_1.message || 'Internal Server Error';
                        res.status(status_1).json({
                            success: false,
                            message: message
                        });
                        return [3 /*break*/, 3];
                    case 3: return [2 /*return*/];
                }
            });
        });
    };
    // Keep getCities for backward compatibility but it handles nothing or search? 
    // We will direct route /provinces and /cities to fail or strict usage.
    ShippingController.prototype.getProvinces = function (req, res) {
        return __awaiter(this, void 0, void 0, function () {
            return __generator(this, function (_a) {
                res.json({ success: true, data: [] });
                return [2 /*return*/];
            });
        });
    };
    ShippingController.prototype.getCities = function (req, res) {
        return __awaiter(this, void 0, void 0, function () {
            return __generator(this, function (_a) {
                res.json({ success: true, data: [] });
                return [2 /*return*/];
            });
        });
    };
    ShippingController.prototype.calculateCost = function (req, res) {
        return __awaiter(this, void 0, void 0, function () {
            var _a, origin_1, destination, weight, courier, result, error_2;
            return __generator(this, function (_b) {
                switch (_b.label) {
                    case 0:
                        _b.trys.push([0, 2, , 3]);
                        _a = req.body, origin_1 = _a.origin, destination = _a.destination, weight = _a.weight, courier = _a.courier;
                        // Hardcoded origin: Jakarta Timur (since we use custom shipping calculation)
                        if (!origin_1) {
                            origin_1 = '3172'; // Jakarta Timur city ID
                        }
                        // Validation
                        if (!destination || !weight || !courier) {
                            return [2 /*return*/, res.status(400).json({
                                    success: false,
                                    message: "Missing required fields: destination, weight, courier"
                                })];
                        }
                        return [4 /*yield*/, binderbyte_service_js_1.default.calculateCost(origin_1, destination, Number(weight), courier)];
                    case 1:
                        result = _b.sent();
                        res.json({
                            success: true,
                            data: result
                        });
                        return [3 /*break*/, 3];
                    case 2:
                        error_2 = _b.sent();
                        console.error('Error in calculateCost:', error_2);
                        res.status(500).json({
                            success: false,
                            message: error_2.message || 'Failed to calculate shipping cost'
                        });
                        return [3 /*break*/, 3];
                    case 3: return [2 /*return*/];
                }
            });
        });
    };
    ShippingController.prototype.checkConnection = function (req, res) {
        return __awaiter(this, void 0, void 0, function () {
            var testResult, error_3;
            return __generator(this, function (_a) {
                switch (_a.label) {
                    case 0:
                        _a.trys.push([0, 2, , 3]);
                        return [4 /*yield*/, binderbyte_service_js_1.default.searchDestination('Jakarta')];
                    case 1:
                        testResult = _a.sent();
                        if (testResult && testResult.length >= 0) {
                            return [2 /*return*/, res.json({ success: true, message: 'Connection successful' })];
                        }
                        else {
                            return [2 /*return*/, res.status(400).json({ success: false, message: 'Connection failed' })];
                        }
                        return [3 /*break*/, 3];
                    case 2:
                        error_3 = _a.sent();
                        return [2 /*return*/, res.status(500).json({ success: false, message: error_3.message })];
                    case 3: return [2 /*return*/];
                }
            });
        });
    };
    return ShippingController;
}());
exports.default = new ShippingController();
