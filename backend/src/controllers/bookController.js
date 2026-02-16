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
exports.deleteBulkBooks = exports.deleteBook = exports.updateBook = exports.createBook = exports.getBookBySlug = exports.getBook = exports.getAllBooks = void 0;
var client_1 = require("@prisma/client");
var AppError_1 = require("../utils/AppError");
var asyncHandler_1 = require("../middlewares/asyncHandler");
var slugify_1 = require("slugify");
var prisma = new client_1.PrismaClient();
exports.getAllBooks = (0, asyncHandler_1.asyncHandler)(function (req, res, next) { return __awaiter(void 0, void 0, void 0, function () {
    var _a, _b, page, _c, limit, sort, search, category, minPrice, maxPrice, inStock, pageNum, limitNum, skip, where, orderBy, _d, field, direction, _e, books, total;
    return __generator(this, function (_f) {
        switch (_f.label) {
            case 0:
                _a = req.query, _b = _a.page, page = _b === void 0 ? 1 : _b, _c = _a.limit, limit = _c === void 0 ? 10 : _c, sort = _a.sort, search = _a.search, category = _a.category, minPrice = _a.minPrice, maxPrice = _a.maxPrice, inStock = _a.inStock;
                pageNum = Number(page);
                limitNum = Number(limit);
                skip = (pageNum - 1) * limitNum;
                where = {};
                if (search) {
                    where.OR = [
                        { title: { contains: String(search) } },
                        { author: { contains: String(search) } },
                    ];
                }
                if (category) {
                    where.category = {
                        slug: String(category),
                    };
                }
                if (minPrice || maxPrice) {
                    where.price = {};
                    if (minPrice)
                        where.price.gte = Number(minPrice);
                    if (maxPrice)
                        where.price.lte = Number(maxPrice);
                }
                if (inStock === 'true') {
                    where.stock = { gt: 0 };
                }
                orderBy = {};
                if (sort) {
                    _d = String(sort).split(':'), field = _d[0], direction = _d[1];
                    if (field === 'price')
                        orderBy.price = direction === 'desc' ? 'desc' : 'asc';
                    if (field === 'rating')
                        orderBy.rating = direction === 'desc' ? 'desc' : 'asc';
                    if (field === 'newest')
                        orderBy.createdAt = 'desc';
                }
                else {
                    orderBy.createdAt = 'desc';
                }
                return [4 /*yield*/, Promise.all([
                        prisma.book.findMany({
                            where: where,
                            skip: skip,
                            take: limitNum,
                            orderBy: orderBy,
                            include: { category: true },
                        }),
                        prisma.book.count({ where: where }),
                    ])];
            case 1:
                _e = _f.sent(), books = _e[0], total = _e[1];
                res.status(200).json({
                    status: 'success',
                    results: books.length,
                    total: total,
                    totalPages: Math.ceil(total / limitNum),
                    currentPage: pageNum,
                    data: { books: books },
                });
                return [2 /*return*/];
        }
    });
}); });
exports.getBook = (0, asyncHandler_1.asyncHandler)(function (req, res, next) { return __awaiter(void 0, void 0, void 0, function () {
    var id, bookId, book;
    return __generator(this, function (_a) {
        switch (_a.label) {
            case 0:
                id = req.params.id;
                bookId = String(id);
                return [4 /*yield*/, prisma.book.findUnique({
                        where: { id: bookId },
                        include: { category: true },
                    })];
            case 1:
                book = _a.sent();
                if (!book) {
                    return [2 /*return*/, next(new AppError_1.AppError('No book found with that ID', 404))];
                }
                res.status(200).json({
                    status: 'success',
                    data: { book: book },
                });
                return [2 /*return*/];
        }
    });
}); });
exports.getBookBySlug = (0, asyncHandler_1.asyncHandler)(function (req, res, next) { return __awaiter(void 0, void 0, void 0, function () {
    var paramSlug, slug, book;
    return __generator(this, function (_a) {
        switch (_a.label) {
            case 0:
                paramSlug = req.params.slug;
                slug = String(paramSlug);
                return [4 /*yield*/, prisma.book.findUnique({
                        where: { slug: slug },
                        include: { category: true },
                    })];
            case 1:
                book = _a.sent();
                if (!book) {
                    return [2 /*return*/, next(new AppError_1.AppError('No book found with that slug', 404))];
                }
                res.status(200).json({
                    status: 'success',
                    data: { book: book },
                });
                return [2 /*return*/];
        }
    });
}); });
exports.createBook = (0, asyncHandler_1.asyncHandler)(function (req, res, next) { return __awaiter(void 0, void 0, void 0, function () {
    var _a, title, author, publisher, isbn, description, price, stock, weight, coverImage, categoryId, pages, language, bookData, newBook;
    return __generator(this, function (_b) {
        switch (_b.label) {
            case 0:
                _a = req.body, title = _a.title, author = _a.author, publisher = _a.publisher, isbn = _a.isbn, description = _a.description, price = _a.price, stock = _a.stock, weight = _a.weight, coverImage = _a.coverImage, categoryId = _a.categoryId, pages = _a.pages, language = _a.language;
                bookData = {
                    title: title,
                    author: author,
                    publisher: publisher,
                    isbn: isbn,
                    description: description,
                    price: Number(price),
                    stock: Number(stock),
                    weight: weight ? Number(weight) : 300,
                    coverImage: coverImage,
                    pages: pages ? Number(pages) : undefined,
                    language: language,
                    categoryId: categoryId && typeof categoryId === 'string' ? categoryId : undefined
                };
                // Auto generate slug if not provided
                if (!req.body.slug && title) {
                    bookData.slug = (0, slugify_1.default)(title, { lower: true, strict: true });
                }
                return [4 /*yield*/, prisma.book.create({
                        data: bookData,
                    })];
            case 1:
                newBook = _b.sent();
                res.status(201).json({
                    status: 'success',
                    data: { book: newBook },
                });
                return [2 /*return*/];
        }
    });
}); });
exports.updateBook = (0, asyncHandler_1.asyncHandler)(function (req, res, next) { return __awaiter(void 0, void 0, void 0, function () {
    var id, bookId, _a, title, author, publisher, isbn, description, price, discountPrice, stock, coverImage, samplePdf, categoryId, isPreorder, preorderDate, pages, language, weight, data, updatedBook;
    return __generator(this, function (_b) {
        switch (_b.label) {
            case 0:
                id = req.params.id;
                bookId = String(id);
                _a = req.body, title = _a.title, author = _a.author, publisher = _a.publisher, isbn = _a.isbn, description = _a.description, price = _a.price, discountPrice = _a.discountPrice, stock = _a.stock, coverImage = _a.coverImage, samplePdf = _a.samplePdf, categoryId = _a.categoryId, isPreorder = _a.isPreorder, preorderDate = _a.preorderDate, pages = _a.pages, language = _a.language, weight = _a.weight;
                data = {
                    title: title,
                    author: author,
                    publisher: publisher,
                    isbn: isbn,
                    description: description,
                    price: price ? Number(price) : undefined,
                    discountPrice: discountPrice ? Number(discountPrice) : undefined,
                    stock: stock ? Number(stock) : undefined,
                    coverImage: coverImage,
                    samplePdf: samplePdf,
                    isPreorder: isPreorder !== undefined ? Boolean(isPreorder) : undefined,
                    preorderDate: preorderDate ? new Date(preorderDate) : undefined,
                    rating: req.body.rating ? Number(req.body.rating) : undefined,
                    totalRating: req.body.totalRating ? Number(req.body.totalRating) : undefined,
                    pages: pages ? Number(pages) : undefined,
                    language: language,
                    weight: weight ? Number(weight) : undefined
                };
                // Only add categoryId if it's provided and not null/undefined/object
                if (categoryId && typeof categoryId === 'string') {
                    data.categoryId = categoryId;
                }
                if (data.title && !req.body.slug) {
                    data.slug = (0, slugify_1.default)(data.title, { lower: true, strict: true });
                }
                // Remove undefined keys
                Object.keys(data).forEach(function (key) { return data[key] === undefined && delete data[key]; });
                return [4 /*yield*/, prisma.book.update({
                        where: { id: bookId },
                        data: data,
                    })];
            case 1:
                updatedBook = _b.sent();
                if (!updatedBook) {
                    return [2 /*return*/, next(new AppError_1.AppError('No book found with that ID', 404))];
                }
                res.status(200).json({
                    status: 'success',
                    data: { book: updatedBook },
                });
                return [2 /*return*/];
        }
    });
}); });
exports.deleteBook = (0, asyncHandler_1.asyncHandler)(function (req, res, next) { return __awaiter(void 0, void 0, void 0, function () {
    var id, bookId, inOrder;
    return __generator(this, function (_a) {
        switch (_a.label) {
            case 0:
                id = req.params.id;
                bookId = String(id);
                return [4 /*yield*/, prisma.orderItem.findFirst({
                        where: { bookId: bookId }
                    })];
            case 1:
                inOrder = _a.sent();
                if (inOrder) {
                    return [2 /*return*/, next(new AppError_1.AppError('Buku tidak dapat dihapus karena memiliki riwayat pesanan. Non-aktifkan stok saja.', 400))];
                }
                return [4 /*yield*/, prisma.book.delete({
                        where: { id: bookId },
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
exports.deleteBulkBooks = (0, asyncHandler_1.asyncHandler)(function (req, res, next) { return __awaiter(void 0, void 0, void 0, function () {
    var ids, booksInOrders, nonDeletableIds, deletableIds, deletedCount, result;
    return __generator(this, function (_a) {
        switch (_a.label) {
            case 0:
                ids = req.body.ids;
                if (!ids || !Array.isArray(ids) || ids.length === 0) {
                    return [2 /*return*/, next(new AppError_1.AppError('Please provide an array of IDs to delete', 400))];
                }
                return [4 /*yield*/, prisma.orderItem.findMany({
                        where: {
                            bookId: { in: ids }
                        },
                        select: { bookId: true },
                        distinct: ['bookId']
                    })];
            case 1:
                booksInOrders = _a.sent();
                nonDeletableIds = booksInOrders.map(function (b) { return b.bookId; });
                deletableIds = ids.filter(function (id) { return !nonDeletableIds.includes(id); });
                deletedCount = 0;
                if (!(deletableIds.length > 0)) return [3 /*break*/, 3];
                return [4 /*yield*/, prisma.book.deleteMany({
                        where: {
                            id: { in: deletableIds }
                        }
                    })];
            case 2:
                result = _a.sent();
                deletedCount = result.count;
                _a.label = 3;
            case 3:
                if (nonDeletableIds.length > 0) {
                    return [2 /*return*/, res.status(200).json({
                            status: 'success',
                            message: "".concat(deletedCount, " buku dihapus. ").concat(nonDeletableIds.length, " buku tidak bisa dihapus karena ada di pesanan."),
                            data: {
                                deleted: deletableIds,
                                failed: nonDeletableIds
                            }
                        })];
                }
                res.status(200).json({
                    status: 'success',
                    message: "".concat(deletedCount, " buku berhasil dihapus")
                });
                return [2 /*return*/];
        }
    });
}); });
