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
exports.deleteReview = exports.getBookReviews = exports.createReview = void 0;
var client_1 = require("@prisma/client");
var asyncHandler_js_1 = require("../middlewares/asyncHandler.js");
var AppError_js_1 = require("../utils/AppError.js");
var prisma = new client_1.PrismaClient();
exports.createReview = (0, asyncHandler_js_1.asyncHandler)(function (req, res, next) { return __awaiter(void 0, void 0, void 0, function () {
    var userId, paramBookId, bookId, _a, rating, comment, book, existingReview, review, aggregations;
    return __generator(this, function (_b) {
        switch (_b.label) {
            case 0:
                userId = req.user.id;
                paramBookId = req.params.bookId;
                bookId = String(paramBookId);
                _a = req.body, rating = _a.rating, comment = _a.comment;
                if (!rating || rating < 1 || rating > 5) {
                    return [2 /*return*/, next(new AppError_js_1.AppError('Rating must be between 1 and 5', 400))];
                }
                return [4 /*yield*/, prisma.book.findUnique({ where: { id: bookId } })];
            case 1:
                book = _b.sent();
                if (!book) {
                    return [2 /*return*/, next(new AppError_js_1.AppError('Book not found', 404))];
                }
                return [4 /*yield*/, prisma.review.findUnique({
                        where: {
                            userId_bookId: {
                                userId: userId,
                                bookId: bookId,
                            },
                        },
                    })];
            case 2:
                existingReview = _b.sent();
                if (existingReview) {
                    return [2 /*return*/, next(new AppError_js_1.AppError('You have already reviewed this book', 400))];
                }
                return [4 /*yield*/, prisma.review.create({
                        data: {
                            userId: userId,
                            bookId: bookId,
                            rating: Number(rating),
                            comment: comment,
                        },
                        include: {
                            user: {
                                select: {
                                    id: true,
                                    name: true,
                                    avatar: true,
                                },
                            },
                        },
                    })];
            case 3:
                review = _b.sent();
                return [4 /*yield*/, prisma.review.aggregate({
                        where: { bookId: bookId },
                        _avg: { rating: true },
                        _count: { rating: true },
                    })];
            case 4:
                aggregations = _b.sent();
                return [4 /*yield*/, prisma.book.update({
                        where: { id: bookId },
                        data: {
                            rating: aggregations._avg.rating || 0,
                            totalRating: aggregations._count.rating || 0,
                        },
                    })];
            case 5:
                _b.sent();
                res.status(201).json({
                    status: 'success',
                    data: { review: review },
                });
                return [2 /*return*/];
        }
    });
}); });
exports.getBookReviews = (0, asyncHandler_js_1.asyncHandler)(function (req, res, next) { return __awaiter(void 0, void 0, void 0, function () {
    var paramBookId, bookId, reviews;
    return __generator(this, function (_a) {
        switch (_a.label) {
            case 0:
                paramBookId = req.params.bookId;
                bookId = String(paramBookId);
                return [4 /*yield*/, prisma.review.findMany({
                        where: { bookId: bookId },
                        include: {
                            user: {
                                select: {
                                    id: true,
                                    name: true,
                                    avatar: true,
                                },
                            },
                        },
                        orderBy: { createdAt: 'desc' },
                    })];
            case 1:
                reviews = _a.sent();
                res.status(200).json({
                    status: 'success',
                    results: reviews.length,
                    data: { reviews: reviews },
                });
                return [2 /*return*/];
        }
    });
}); });
exports.deleteReview = (0, asyncHandler_js_1.asyncHandler)(function (req, res, next) { return __awaiter(void 0, void 0, void 0, function () {
    var userId, userRole, id, reviewId, review, bookId, aggregations;
    return __generator(this, function (_a) {
        switch (_a.label) {
            case 0:
                userId = req.user.id;
                userRole = req.user.role;
                id = req.params.id;
                reviewId = String(id);
                return [4 /*yield*/, prisma.review.findUnique({ where: { id: reviewId } })];
            case 1:
                review = _a.sent();
                if (!review) {
                    return [2 /*return*/, next(new AppError_js_1.AppError('Review not found', 404))];
                }
                // Only allow deletion if user is owner or admin
                if (review.userId !== userId && userRole !== 'ADMIN') {
                    return [2 /*return*/, next(new AppError_js_1.AppError('You update not authorized to delete this review', 403))];
                }
                return [4 /*yield*/, prisma.review.delete({ where: { id: reviewId } })];
            case 2:
                _a.sent();
                bookId = review.bookId;
                return [4 /*yield*/, prisma.review.aggregate({
                        where: { bookId: bookId },
                        _avg: { rating: true },
                        _count: { rating: true },
                    })];
            case 3:
                aggregations = _a.sent();
                return [4 /*yield*/, prisma.book.update({
                        where: { id: bookId },
                        data: {
                            rating: aggregations._avg.rating || 0,
                            totalRating: aggregations._count.rating || 0,
                        },
                    })];
            case 4:
                _a.sent();
                res.status(204).json({
                    status: 'success',
                    data: null,
                });
                return [2 /*return*/];
        }
    });
}); });
