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
exports.processPaymentProof = exports.resizeImage = exports.upload = void 0;
var multer_1 = require("multer");
var sharp_1 = require("sharp");
var fs_1 = require("fs");
var path_1 = require("path");
var AppError_1 = require("../utils/AppError");
// Ensure upload directory exists
var uploadDir = 'public/uploads';
if (!fs_1.default.existsSync(uploadDir)) {
    fs_1.default.mkdirSync(uploadDir, { recursive: true });
}
// Multer Storage (Memory for processing)
var storage = multer_1.default.memoryStorage();
// Multer Filter
var multerFilter = function (req, file, cb) {
    if (file.mimetype.startsWith('image')) {
        cb(null, true);
    }
    else {
        cb(new AppError_1.AppError('Not an image! Please upload only images.', 400), false);
    }
};
exports.upload = (0, multer_1.default)({
    storage: storage,
    fileFilter: multerFilter
});
var resizeImage = function (req, res, next) { return __awaiter(void 0, void 0, void 0, function () {
    var filename, filepath, error_1;
    return __generator(this, function (_a) {
        switch (_a.label) {
            case 0:
                if (!req.file)
                    return [2 /*return*/, next()];
                filename = "book-".concat(Date.now(), "-").concat(Math.round(Math.random() * 1E9), ".webp");
                filepath = path_1.default.join(uploadDir, filename);
                _a.label = 1;
            case 1:
                _a.trys.push([1, 3, , 4]);
                return [4 /*yield*/, (0, sharp_1.default)(req.file.buffer)
                        .resize(800, 1200, {
                        fit: 'cover',
                        withoutEnlargement: true
                    })
                        .toFormat('webp')
                        .webp({ quality: 80 })
                        .toFile(filepath)];
            case 2:
                _a.sent();
                req.body.coverImage = "/uploads/".concat(filename);
                next();
                return [3 /*break*/, 4];
            case 3:
                error_1 = _a.sent();
                next(new AppError_1.AppError('Error processing image', 500));
                return [3 /*break*/, 4];
            case 4: return [2 /*return*/];
        }
    });
}); };
exports.resizeImage = resizeImage;
var processPaymentProof = function (req, res, next) { return __awaiter(void 0, void 0, void 0, function () {
    var filename, filepath, error_2;
    return __generator(this, function (_a) {
        switch (_a.label) {
            case 0:
                if (!req.file)
                    return [2 /*return*/, next()];
                filename = "proof-".concat(Date.now(), "-").concat(Math.round(Math.random() * 1E9), ".webp");
                filepath = path_1.default.join(uploadDir, filename);
                _a.label = 1;
            case 1:
                _a.trys.push([1, 3, , 4]);
                return [4 /*yield*/, (0, sharp_1.default)(req.file.buffer)
                        .resize(1000, 1000, {
                        fit: 'inside',
                        withoutEnlargement: true
                    })
                        .toFormat('webp')
                        .webp({ quality: 80 })
                        .toFile(filepath)];
            case 2:
                _a.sent();
                req.body.paymentProof = "/uploads/".concat(filename);
                next();
                return [3 /*break*/, 4];
            case 3:
                error_2 = _a.sent();
                next(new AppError_1.AppError('Error processing image', 500));
                return [3 /*break*/, 4];
            case 4: return [2 /*return*/];
        }
    });
}); };
exports.processPaymentProof = processPaymentProof;
