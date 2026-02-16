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
exports.deleteUser = exports.createUser = exports.updateUserRole = exports.getAllUsers = exports.updateProfile = void 0;
var client_1 = require("@prisma/client");
var bcrypt_1 = require("bcrypt");
var asyncHandler_js_1 = require("../middlewares/asyncHandler.js");
var AppError_js_1 = require("../utils/AppError.js");
var prisma = new client_1.PrismaClient();
exports.updateProfile = (0, asyncHandler_js_1.asyncHandler)(function (req, res, next) { return __awaiter(void 0, void 0, void 0, function () {
    var userId, _a, name, password, confirmPassword, dataToUpdate, _b, updatedUser;
    return __generator(this, function (_c) {
        switch (_c.label) {
            case 0:
                userId = req.user.id;
                _a = req.body, name = _a.name, password = _a.password, confirmPassword = _a.confirmPassword;
                dataToUpdate = { name: name };
                if (!password) return [3 /*break*/, 2];
                if (password !== confirmPassword) {
                    return [2 /*return*/, next(new AppError_js_1.AppError('Konfirmasi password tidak cocok', 400))];
                }
                _b = dataToUpdate;
                return [4 /*yield*/, bcrypt_1.default.hash(password, 12)];
            case 1:
                _b.password = _c.sent();
                _c.label = 2;
            case 2: return [4 /*yield*/, prisma.user.update({
                    where: { id: userId },
                    data: dataToUpdate,
                    select: {
                        id: true,
                        name: true,
                        email: true,
                        role: true,
                        avatar: true,
                    },
                })];
            case 3:
                updatedUser = _c.sent();
                res.status(200).json({
                    status: 'success',
                    data: {
                        user: updatedUser,
                    },
                });
                return [2 /*return*/];
        }
    });
}); });
// Admin Controllers
exports.getAllUsers = (0, asyncHandler_js_1.asyncHandler)(function (req, res, next) { return __awaiter(void 0, void 0, void 0, function () {
    var _a, _b, page, _c, limit, search, pageNum, limitNum, skip, where, _d, users, total;
    return __generator(this, function (_e) {
        switch (_e.label) {
            case 0:
                _a = req.query, _b = _a.page, page = _b === void 0 ? 1 : _b, _c = _a.limit, limit = _c === void 0 ? 10 : _c, search = _a.search;
                pageNum = Number(page);
                limitNum = Number(limit);
                skip = (pageNum - 1) * limitNum;
                where = {};
                if (search) {
                    where.OR = [
                        { name: { contains: String(search) } }, // Remove mode: insensitive for SQLite if needed, but Prisma usually handles it. Wait, SQLite does NOT support mode insensitive in older versions, but Prisma client polyfills it? No.
                        // For SQLite, contains is case insensitive by default for ASCII but not unicode?
                        // Let's stick to standard contains for now. If issues arise, we valid.
                        { email: { contains: String(search) } },
                    ];
                }
                return [4 /*yield*/, Promise.all([
                        prisma.user.findMany({
                            where: where,
                            skip: skip,
                            take: limitNum,
                            orderBy: { createdAt: 'desc' },
                            select: {
                                id: true,
                                name: true,
                                email: true,
                                role: true,
                                createdAt: true,
                                _count: {
                                    select: { orders: true }
                                }
                            }
                        }),
                        prisma.user.count({ where: where })
                    ])];
            case 1:
                _d = _e.sent(), users = _d[0], total = _d[1];
                res.status(200).json({
                    status: 'success',
                    results: users.length,
                    total: total,
                    totalPages: Math.ceil(total / limitNum),
                    currentPage: pageNum,
                    data: { users: users }
                });
                return [2 /*return*/];
        }
    });
}); });
exports.updateUserRole = (0, asyncHandler_js_1.asyncHandler)(function (req, res, next) { return __awaiter(void 0, void 0, void 0, function () {
    var id, userId, role, user;
    return __generator(this, function (_a) {
        switch (_a.label) {
            case 0:
                id = req.params.id;
                userId = String(id);
                role = req.body.role;
                if (!['USER', 'ADMIN', 'SUPER_ADMIN'].includes(role)) {
                    return [2 /*return*/, next(new AppError_js_1.AppError('Role invalid', 400))];
                }
                return [4 /*yield*/, prisma.user.update({
                        where: { id: userId },
                        data: { role: role },
                        select: { id: true, name: true, email: true, role: true }
                    })];
            case 1:
                user = _a.sent();
                res.status(200).json({
                    status: 'success',
                    data: { user: user }
                });
                return [2 /*return*/];
        }
    });
}); });
exports.createUser = (0, asyncHandler_js_1.asyncHandler)(function (req, res, next) { return __awaiter(void 0, void 0, void 0, function () {
    var _a, name, email, password, role, existingUser, hashedPassword, newUser;
    return __generator(this, function (_b) {
        switch (_b.label) {
            case 0:
                _a = req.body, name = _a.name, email = _a.email, password = _a.password, role = _a.role;
                return [4 /*yield*/, prisma.user.findUnique({ where: { email: String(email) } })];
            case 1:
                existingUser = _b.sent();
                if (existingUser) {
                    return [2 /*return*/, next(new AppError_js_1.AppError('Email already registered', 400))];
                }
                return [4 /*yield*/, bcrypt_1.default.hash(String(password), 12)];
            case 2:
                hashedPassword = _b.sent();
                return [4 /*yield*/, prisma.user.create({
                        data: {
                            name: String(name),
                            email: String(email),
                            password: hashedPassword,
                            role: String(role || 'USER')
                        },
                        select: {
                            id: true,
                            name: true,
                            email: true,
                            role: true,
                            createdAt: true
                        }
                    })];
            case 3:
                newUser = _b.sent();
                res.status(201).json({
                    status: 'success',
                    data: { user: newUser }
                });
                return [2 /*return*/];
        }
    });
}); });
exports.deleteUser = (0, asyncHandler_js_1.asyncHandler)(function (req, res, next) { return __awaiter(void 0, void 0, void 0, function () {
    var id, userId, currentUserId;
    return __generator(this, function (_a) {
        switch (_a.label) {
            case 0:
                id = req.params.id;
                userId = String(id);
                currentUserId = req.user.id;
                if (userId === currentUserId) {
                    return [2 /*return*/, next(new AppError_js_1.AppError('Cannot delete yourself', 400))];
                }
                return [4 /*yield*/, prisma.user.delete({
                        where: { id: userId }
                    })];
            case 1:
                _a.sent();
                res.status(204).json({
                    status: 'success',
                    data: null
                });
                return [2 /*return*/];
        }
    });
}); });
