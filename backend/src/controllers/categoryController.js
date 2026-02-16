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
exports.deleteCategory = exports.updateCategory = exports.createCategory = exports.getAllCategories = void 0;
var client_1 = require("@prisma/client");
var asyncHandler_js_1 = require("../middlewares/asyncHandler.js");
var AppError_js_1 = require("../utils/AppError.js");
var prisma = new client_1.PrismaClient();
var slugify = function (text) {
    return text.toString().toLowerCase()
        .replace(/\s+/g, '-') // Replace spaces with -
        .replace(/[^\w\-]+/g, '') // Remove all non-word chars
        .replace(/\-\-+/g, '-') // Replace multiple - with single -
        .replace(/^-+/, '') // Trim - from start of text
        .replace(/-+$/, ''); // Trim - from end of text
};
exports.getAllCategories = (0, asyncHandler_js_1.asyncHandler)(function (req, res, next) { return __awaiter(void 0, void 0, void 0, function () {
    var categories;
    return __generator(this, function (_a) {
        switch (_a.label) {
            case 0: return [4 /*yield*/, prisma.category.findMany({
                    orderBy: { name: 'asc' },
                    include: {
                        _count: {
                            select: { books: true }
                        }
                    }
                })];
            case 1:
                categories = _a.sent();
                res.status(200).json({
                    status: 'success',
                    results: categories.length,
                    data: { categories: categories },
                });
                return [2 /*return*/];
        }
    });
}); });
exports.createCategory = (0, asyncHandler_js_1.asyncHandler)(function (req, res, next) { return __awaiter(void 0, void 0, void 0, function () {
    var name, slug, existingCategory, category;
    return __generator(this, function (_a) {
        switch (_a.label) {
            case 0:
                name = req.body.name;
                if (!name) {
                    return [2 /*return*/, next(new AppError_js_1.AppError('Category name is required', 400))];
                }
                slug = slugify(name);
                return [4 /*yield*/, prisma.category.findUnique({
                        where: { slug: slug }
                    })];
            case 1:
                existingCategory = _a.sent();
                if (existingCategory) {
                    return [2 /*return*/, next(new AppError_js_1.AppError('Category already exists', 400))];
                }
                return [4 /*yield*/, prisma.category.create({
                        data: { name: name, slug: slug }
                    })];
            case 2:
                category = _a.sent();
                res.status(201).json({
                    status: 'success',
                    data: { category: category },
                });
                return [2 /*return*/];
        }
    });
}); });
exports.updateCategory = (0, asyncHandler_js_1.asyncHandler)(function (req, res, next) { return __awaiter(void 0, void 0, void 0, function () {
    var id, name, slug, existingCategory, category;
    return __generator(this, function (_a) {
        switch (_a.label) {
            case 0:
                id = req.params.id;
                name = req.body.name;
                if (!name) {
                    return [2 /*return*/, next(new AppError_js_1.AppError('Category name is required', 400))];
                }
                slug = slugify(name);
                return [4 /*yield*/, prisma.category.findUnique({
                        where: { slug: slug }
                    })];
            case 1:
                existingCategory = _a.sent();
                if (existingCategory && existingCategory.id !== id) {
                    return [2 /*return*/, next(new AppError_js_1.AppError('Category name already exists', 400))];
                }
                return [4 /*yield*/, prisma.category.update({
                        where: { id: id },
                        data: { name: name, slug: slug }
                    })];
            case 2:
                category = _a.sent();
                res.status(200).json({
                    status: 'success',
                    data: { category: category },
                });
                return [2 /*return*/];
        }
    });
}); });
exports.deleteCategory = (0, asyncHandler_js_1.asyncHandler)(function (req, res, next) { return __awaiter(void 0, void 0, void 0, function () {
    var id, category;
    return __generator(this, function (_a) {
        switch (_a.label) {
            case 0:
                id = req.params.id;
                return [4 /*yield*/, prisma.category.findUnique({
                        where: { id: id },
                        include: {
                            _count: {
                                select: { books: true }
                            }
                        }
                    })];
            case 1:
                category = _a.sent();
                if (!category) {
                    return [2 /*return*/, next(new AppError_js_1.AppError('Category not found', 404))];
                }
                if (category._count.books > 0) {
                    return [2 /*return*/, next(new AppError_js_1.AppError('Cannot delete category with associated books', 400))];
                }
                return [4 /*yield*/, prisma.category.delete({
                        where: { id: id }
                    })];
            case 2:
                _a.sent();
                res.status(204).json({
                    status: 'success',
                    data: null,
                });
                return [2 /*return*/];
        }
    });
}); });
