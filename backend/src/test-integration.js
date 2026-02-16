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
var rajaongkir_service_js_1 = require("./services/rajaongkir.service.js");
var prisma_js_1 = require("./lib/prisma.js");
function testIntegration() {
    return __awaiter(this, void 0, void 0, function () {
        var userBaseUrl, origins, origin_1, destinations, destination, weight, courier, costs, error_1;
        return __generator(this, function (_a) {
            switch (_a.label) {
                case 0:
                    _a.trys.push([0, 7, 8, 10]);
                    console.log('--- TEST INTEGRATION KOMERCE (SANDBOX) ---');
                    userBaseUrl = 'https://api-sandbox.collaborator.komerce.id/tariff/api/v1';
                    console.log("0. Setting Base URL to ".concat(userBaseUrl));
                    return [4 /*yield*/, prisma_js_1.default.setting.upsert({
                            where: { key: 'rajaongkir_base_url' },
                            create: { key: 'rajaongkir_base_url', value: userBaseUrl },
                            update: { value: userBaseUrl }
                        })];
                case 1:
                    _a.sent();
                    // 1. Search for Origin (e.g., "Sleman")
                    console.log('\n1. Searching Origin "Sleman"...');
                    return [4 /*yield*/, rajaongkir_service_js_1.default.searchDestination('Sleman')];
                case 2:
                    origins = _a.sent();
                    console.log("Found ".concat(origins.length, " locations for \"Sleman\"."));
                    if (origins.length === 0)
                        throw new Error('No origin found');
                    origin_1 = origins[0];
                    console.log('Selected Origin:', origin_1);
                    // 2. Search for Destination (e.g., "Gambir")
                    console.log('\n2. Searching Destination "Gambir"...');
                    return [4 /*yield*/, rajaongkir_service_js_1.default.searchDestination('Gambir')];
                case 3:
                    destinations = _a.sent();
                    console.log("Found ".concat(destinations.length, " locations for \"Gambir\"."));
                    if (destinations.length === 0)
                        throw new Error('No destination found');
                    destination = destinations[0];
                    console.log('Selected Destination:', destination);
                    // 3. Update Settings (mimic Admin saving settings)
                    console.log('\n3. Updating Settings...');
                    return [4 /*yield*/, prisma_js_1.default.setting.upsert({
                            where: { key: 'rajaongkir_origin_city_id' },
                            create: { key: 'rajaongkir_origin_city_id', value: String(origin_1.id) },
                            update: { value: String(origin_1.id) }
                        })];
                case 4:
                    _a.sent();
                    return [4 /*yield*/, prisma_js_1.default.setting.upsert({
                            where: { key: 'rajaongkir_origin_city_name' },
                            create: { key: 'rajaongkir_origin_city_name', value: origin_1.label || origin_1.name || origin_1.destination_name },
                            update: { value: origin_1.label || origin_1.name || origin_1.destination_name }
                        })];
                case 5:
                    _a.sent();
                    // 4. Calculate Cost
                    console.log('\n4. Calculating Cost...');
                    weight = 1000;
                    courier = 'jne';
                    return [4 /*yield*/, rajaongkir_service_js_1.default.calculateCost(String(origin_1.id), String(destination.id), weight, courier)];
                case 6:
                    costs = _a.sent();
                    console.log('Costs calculated:', JSON.stringify(costs, null, 2));
                    if (costs.length > 0) {
                        console.log('\nSUCCESS: Shipping costs retrieved.');
                    }
                    else {
                        console.log('\nWARNING: No costs returned (empty list).');
                    }
                    return [3 /*break*/, 10];
                case 7:
                    error_1 = _a.sent();
                    console.error('TEST FAILED:', error_1.message);
                    if (error_1.response) {
                        console.error('Response Status:', error_1.response.status);
                        console.error('Response Data:', error_1.response.data);
                    }
                    return [3 /*break*/, 10];
                case 8: return [4 /*yield*/, prisma_js_1.default.$disconnect()];
                case 9:
                    _a.sent();
                    return [7 /*endfinally*/];
                case 10: return [2 /*return*/];
            }
        });
    });
}
testIntegration();
