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
var __spreadArray = (this && this.__spreadArray) || function (to, from, pack) {
    if (pack || arguments.length === 2) for (var i = 0, l = from.length, ar; i < l; i++) {
        if (ar || !(i in from)) {
            if (!ar) ar = Array.prototype.slice.call(from, 0, i);
            ar[i] = from[i];
        }
    }
    return to.concat(ar || Array.prototype.slice.call(from));
};
Object.defineProperty(exports, "__esModule", { value: true });
var region_data_1 = require("../data/region-data");
var district_data_1 = require("../data/district-data");
var BinderByteService = /** @class */ (function () {
    function BinderByteService() {
    }
    /**
     * Search destination locally using region and district data
     */
    BinderByteService.prototype.searchDestination = function (keyword) {
        return __awaiter(this, void 0, void 0, function () {
            var lowerKeyword, cityMatches, districtMatches, allMatches;
            return __generator(this, function (_a) {
                console.log("Searching destination for: ".concat(keyword));
                lowerKeyword = keyword.toLowerCase();
                cityMatches = region_data_1.regencies.filter(function (r) {
                    return r.name.toLowerCase().includes(lowerKeyword) ||
                        (r.alt_name && r.alt_name.toLowerCase().includes(lowerKeyword));
                }).map(function (r) { return ({
                    id: r.id,
                    name: r.name,
                    type: r.name.startsWith('KOTA') ? 'Kota' : 'Kabupaten',
                    label: r.name
                }); });
                districtMatches = district_data_1.districts.filter(function (d) {
                    return d.name.toLowerCase().includes(lowerKeyword);
                }).map(function (d) {
                    // Find parent regency for better label
                    var parentRegency = region_data_1.regencies.find(function (r) { return r.id === d.regency_id; });
                    var regencyName = parentRegency ? parentRegency.name : '';
                    return {
                        id: d.id,
                        name: d.name,
                        type: 'Kecamatan',
                        label: "Kec. ".concat(d.name, ", ").concat(regencyName)
                    };
                });
                allMatches = __spreadArray(__spreadArray([], cityMatches, true), districtMatches, true);
                return [2 /*return*/, allMatches.slice(0, 20)];
            });
        });
    };
    /**
     * Calculate Shipping Cost - MANUAL LOGIC
     * Based on zones: Jakarta -> Indonesia regions
     */
    BinderByteService.prototype.calculateCost = function (origin, destination, weight, courier) {
        return __awaiter(this, void 0, void 0, function () {
            var originRegency, destRegencyId_1, destIsDistrict, district, destRegency, cost, etd, originProvPrefix, destProvPrefix, originIsJava, destProvId, destProvId, destProvId, destProvId, destProvId, weightKg;
            return __generator(this, function (_a) {
                console.log("Calculating Manual Cost: Origin=".concat(origin, " -> Dest=").concat(destination));
                try {
                    originRegency = region_data_1.regencies.find(function (r) { return r.id === origin; });
                    destRegencyId_1 = destination;
                    destIsDistrict = false;
                    if (destination.length > 4) {
                        district = district_data_1.districts.find(function (d) { return d.id === destination; });
                        if (district) {
                            destRegencyId_1 = district.regency_id;
                            destIsDistrict = true;
                        }
                    }
                    destRegency = region_data_1.regencies.find(function (r) { return r.id === destRegencyId_1; });
                    if (!originRegency || !destRegency) {
                        console.warn('Manual Calc: Regions not found locally.');
                        return [2 /*return*/, this.getManualRates(50000, 55000)];
                    }
                    cost = 30000;
                    etd = '3-5';
                    if (originRegency.id === destRegency.id) {
                        // SAMA KOTA/KABUPATEN (Jakarta ke Jakarta)
                        cost = 12000;
                        etd = '1-2';
                    }
                    else if (originRegency.province_id === destRegency.province_id) {
                        // SAMA PROVINSI (Jakarta Timur ke Jakarta Barat/Bekasi/Depok/Tangerang)
                        cost = 16000;
                        etd = '1-2';
                    }
                    else {
                        originProvPrefix = originRegency.province_id.substring(0, 1);
                        destProvPrefix = destRegency.province_id.substring(0, 1);
                        originIsJava = ['31', '32', '33', '34', '35', '36'].includes(originRegency.province_id);
                        if (originIsJava) {
                            // Logic from Java (Jakarta) to others
                            if (destProvPrefix === '3') {
                                destProvId = destRegency.province_id;
                                if (destProvId === '32') {
                                    // Jawa Barat (Bandung, Bogor area)
                                    cost = 20000;
                                    etd = '2-3';
                                }
                                else if (destProvId === '33' || destProvId === '34') {
                                    // Jawa Tengah & DIY (Semarang, Solo, Yogya)
                                    cost = 28000;
                                    etd = '3-4';
                                }
                                else if (destProvId === '35') {
                                    // Jawa Timur (Surabaya, Malang, Madiun)
                                    cost = 32000;
                                    etd = '3-5';
                                }
                                else {
                                    // Banten
                                    cost = 18000;
                                    etd = '2-3';
                                }
                            }
                            else if (destProvPrefix === '1' || destProvPrefix === '2') {
                                destProvId = parseInt(destRegency.province_id);
                                if (destProvId >= 11 && destProvId <= 13) {
                                    // Sumatra Utara (Aceh, Sumut)
                                    cost = 52000;
                                    etd = '4-6';
                                }
                                else if (destProvId >= 14 && destProvId <= 15) {
                                    // Riau, Kepri
                                    cost = 48000;
                                    etd = '4-6';
                                }
                                else {
                                    // Sumatra Selatan (Jambi, Sumsel, Bengkulu, Lampung, Babel)
                                    cost = 40000;
                                    etd = '3-5';
                                }
                            }
                            else if (destProvPrefix === '5') {
                                destProvId = parseInt(destRegency.province_id);
                                if (destProvId === 51) {
                                    // Bali
                                    cost = 42000;
                                    etd = '3-5';
                                }
                                else if (destProvId === 52) {
                                    // NTB (Lombok, Sumbawa)
                                    cost = 50000;
                                    etd = '4-6';
                                }
                                else {
                                    // NTT (Kupang, Flores)
                                    cost = 58000;
                                    etd = '5-7';
                                }
                            }
                            else if (destProvPrefix === '6') {
                                destProvId = parseInt(destRegency.province_id);
                                if (destProvId === 61) {
                                    // Kalbar (Pontianak)
                                    cost = 55000;
                                    etd = '4-6';
                                }
                                else if (destProvId === 64 || destProvId === 65) {
                                    // Kaltim, Kaltara (Balikpapan, Samarinda)
                                    cost = 62000;
                                    etd = '4-7';
                                }
                                else {
                                    // Kalteng, Kalsel
                                    cost = 58000;
                                    etd = '4-6';
                                }
                            }
                            else if (destProvPrefix === '7') {
                                destProvId = parseInt(destRegency.province_id);
                                if (destProvId === 73) {
                                    // Sulsel (Makassar)
                                    cost = 65000;
                                    etd = '4-7';
                                }
                                else if (destProvId === 71) {
                                    // Sulut (Manado)
                                    cost = 75000;
                                    etd = '5-8';
                                }
                                else {
                                    // Sulteng, Sulbar, Sultra, Gorontalo
                                    cost = 70000;
                                    etd = '5-7';
                                }
                            }
                            else if (destProvPrefix === '8') {
                                // To Maluku
                                // Ambon: ~95rb, Ternate: ~100rb
                                cost = 98000;
                                etd = '7-10';
                            }
                            else if (destProvPrefix === '9') {
                                // To Papua
                                // Jayapura: ~125rb, Timika: ~135rb, Sorong: ~130rb
                                cost = 128000;
                                etd = '8-14';
                            }
                            else {
                                // Others / Fallback
                                cost = 50000;
                                etd = '5-7';
                            }
                        }
                        else {
                            // Origin NOT Java (General Fallback)
                            if (originProvPrefix === destProvPrefix) {
                                cost = 30000;
                                etd = '3-5';
                            }
                            else {
                                cost = 60000;
                                etd = '5-10';
                            }
                        }
                    }
                    weightKg = Math.ceil(weight / 1000);
                    if (weightKg > 1) {
                        cost += (weightKg - 1) * 5000;
                    }
                    return [2 /*return*/, this.getManualRates(cost, cost + 5000, etd)];
                }
                catch (error) {
                    console.error('Manual Cost Error:', error);
                    return [2 /*return*/, this.getManualRates(50000, 55000)];
                }
                return [2 /*return*/];
            });
        });
    };
    BinderByteService.prototype.getManualRates = function (regularCost, expressCost, etdReg) {
        if (etdReg === void 0) { etdReg = '2-4'; }
        return [
            {
                code: 'wahana',
                name: 'Wahana',
                costs: [
                    {
                        service: 'REG',
                        description: 'Layanan Reguler',
                        cost: [{ value: regularCost, etd: etdReg }]
                    }
                ]
            },
            {
                code: 'lion',
                name: 'Lion Parcel',
                costs: [
                    {
                        service: 'REG',
                        description: 'Layanan Reguler',
                        cost: [{ value: regularCost - 1000, etd: etdReg }]
                    }
                ]
            },
            {
                code: 'sentral',
                name: 'Sentral Cargo',
                costs: [
                    {
                        service: 'REG',
                        description: 'Layanan Reguler',
                        cost: [{ value: regularCost + 2000, etd: etdReg }]
                    }
                ]
            },
            {
                code: 'indah',
                name: 'Indah Cargo',
                costs: [
                    {
                        service: 'REG',
                        description: 'Layanan Reguler',
                        cost: [{ value: regularCost - 500, etd: etdReg }]
                    }
                ]
            }
        ];
    };
    return BinderByteService;
}());
exports.default = new BinderByteService();
