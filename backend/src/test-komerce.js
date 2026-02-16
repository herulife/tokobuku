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
var dotenv_1 = require("dotenv");
dotenv_1.default.config();
var prisma_js_1 = require("./lib/prisma.js");
function test() {
    return __awaiter(this, void 0, void 0, function () {
        var e_1, axios, apiKey, domain, r1, e_2, r2, e_3, r3, e_4, paths, _i, paths_1, p, e_5, e_6;
        var _a, _b, _c, _d, _e;
        return __generator(this, function (_f) {
            switch (_f.label) {
                case 0:
                    console.log('--- TESTING KOMERCE SHIPPING SERVICE ---');
                    _f.label = 1;
                case 1:
                    _f.trys.push([1, 3, , 4]);
                    return [4 /*yield*/, prisma_js_1.default.setting.upsert({
                            where: { key: 'rajaongkir_base_url' },
                            update: { value: 'https://api-sandbox.collaborator.komerce.id' },
                            create: {
                                key: 'rajaongkir_base_url',
                                value: 'https://api-sandbox.collaborator.komerce.id'
                            }
                        })];
                case 2:
                    _f.sent();
                    console.log('Updated DB to Sandbox URL');
                    return [3 /*break*/, 4];
                case 3:
                    e_1 = _f.sent();
                    console.error('Failed to update DB setting:', e_1.message);
                    return [3 /*break*/, 4];
                case 4: return [4 /*yield*/, Promise.resolve().then(function () { return require('axios'); })];
                case 5:
                    axios = (_f.sent()).default;
                    apiKey = 'mPKXAhtf5dad13a7ba03f27bYBtVMvjI';
                    domain = 'https://rajaongkir.komerce.id';
                    console.log('\n--- DEBUG PROBE RAJAONGKIR.KOMERCE.ID ---');
                    _f.label = 6;
                case 6:
                    _f.trys.push([6, 8, , 9]);
                    console.log("\n[ROOT] ".concat(domain, "/"));
                    return [4 /*yield*/, axios.get("".concat(domain, "/"), { headers: { 'key': apiKey } })];
                case 7:
                    r1 = _f.sent();
                    console.log('  Header [key]: 200 OK -', JSON.stringify(r1.data));
                    return [3 /*break*/, 9];
                case 8:
                    e_2 = _f.sent();
                    console.log('  Header [key]:', (_a = e_2.response) === null || _a === void 0 ? void 0 : _a.status);
                    return [3 /*break*/, 9];
                case 9:
                    _f.trys.push([9, 11, , 12]);
                    return [4 /*yield*/, axios.get("".concat(domain, "/"), { headers: { 'x-api-key': apiKey } })];
                case 10:
                    r2 = _f.sent();
                    console.log('  Header [x-api-key]: 200 OK -', JSON.stringify(r2.data));
                    return [3 /*break*/, 12];
                case 11:
                    e_3 = _f.sent();
                    console.log('  Header [x-api-key]:', (_b = e_3.response) === null || _b === void 0 ? void 0 : _b.status);
                    return [3 /*break*/, 12];
                case 12:
                    _f.trys.push([12, 14, , 15]);
                    return [4 /*yield*/, axios.get("".concat(domain, "/"))];
                case 13:
                    r3 = _f.sent();
                    console.log('  No Header: 200 OK -', JSON.stringify(r3.data));
                    return [3 /*break*/, 15];
                case 14:
                    e_4 = _f.sent();
                    console.log('  No Header:', (_c = e_4.response) === null || _c === void 0 ? void 0 : _c.status);
                    return [3 /*break*/, 15];
                case 15:
                    paths = [
                        '/tariff/api/v1/destination/search',
                        '/api/v1/destination/search',
                        '/v1/destination/search',
                        '/destination/search',
                        '/search'
                    ];
                    _i = 0, paths_1 = paths;
                    _f.label = 16;
                case 16:
                    if (!(_i < paths_1.length)) return [3 /*break*/, 24];
                    p = paths_1[_i];
                    console.log("\n[PATH] ".concat(p));
                    _f.label = 17;
                case 17:
                    _f.trys.push([17, 19, , 20]);
                    return [4 /*yield*/, axios.get("".concat(domain).concat(p), { headers: { 'key': apiKey }, params: { keyword: 'Gambir' } })];
                case 18:
                    _f.sent();
                    console.log('  Header [key]: SUCCESS');
                    return [3 /*break*/, 20];
                case 19:
                    e_5 = _f.sent();
                    process.stdout.write("  [key:".concat((_d = e_5.response) === null || _d === void 0 ? void 0 : _d.status, "]"));
                    return [3 /*break*/, 20];
                case 20:
                    _f.trys.push([20, 22, , 23]);
                    return [4 /*yield*/, axios.get("".concat(domain).concat(p), { headers: { 'x-api-key': apiKey }, params: { keyword: 'Gambir' } })];
                case 21:
                    _f.sent();
                    console.log('  Header [x-api-key]: SUCCESS');
                    return [3 /*break*/, 23];
                case 22:
                    e_6 = _f.sent();
                    process.stdout.write("  [x-api-key:".concat((_e = e_6.response) === null || _e === void 0 ? void 0 : _e.status, "]"));
                    return [3 /*break*/, 23];
                case 23:
                    _i++;
                    return [3 /*break*/, 16];
                case 24: return [2 /*return*/];
            }
        });
    });
}
test();
