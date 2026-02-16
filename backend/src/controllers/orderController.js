"use strict";
var __assign = (this && this.__assign) || function () {
    __assign = Object.assign || function(t) {
        for (var s, i = 1, n = arguments.length; i < n; i++) {
            s = arguments[i];
            for (var p in s) if (Object.prototype.hasOwnProperty.call(s, p))
                t[p] = s[p];
        }
        return t;
    };
    return __assign.apply(this, arguments);
};
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
exports.deleteOrder = exports.uploadPaymentProof = exports.updateOrderStatus = exports.getAllOrders = exports.cancelOrder = exports.getOrderById = exports.getMyOrders = exports.createOrder = void 0;
var client_1 = require("@prisma/client");
var asyncHandler_js_1 = require("../middlewares/asyncHandler.js");
var AppError_js_1 = require("../utils/AppError.js");
var prisma = new client_1.PrismaClient();
// Generate Invoice Number: INV/20231027/CUID-SUFFIX
var generateInvoiceNumber = function () {
    var date = new Date().toISOString().slice(0, 10).replace(/-/g, '');
    var random = Math.floor(Math.random() * 10000).toString().padStart(4, '0');
    return "INV/".concat(date, "/").concat(random);
};
exports.createOrder = (0, asyncHandler_js_1.asyncHandler)(function (req, res, next) { return __awaiter(void 0, void 0, void 0, function () {
    var userId, _a, shippingAddress, paymentMethod, courier, cart, total, orderItemsData, _i, _b, item, price, order;
    return __generator(this, function (_c) {
        switch (_c.label) {
            case 0:
                userId = req.user.id;
                _a = req.body, shippingAddress = _a.shippingAddress, paymentMethod = _a.paymentMethod, courier = _a.courier;
                if (!shippingAddress || !paymentMethod) {
                    return [2 /*return*/, next(new AppError_js_1.AppError('Shipping address and payment method are required', 400))];
                }
                return [4 /*yield*/, prisma.cart.findUnique({
                        where: { userId: userId },
                        include: {
                            items: {
                                include: { book: true }
                            }
                        }
                    })];
            case 1:
                cart = _c.sent();
                if (!cart || cart.items.length === 0) {
                    return [2 /*return*/, next(new AppError_js_1.AppError('Cart is empty', 400))];
                }
                total = 0;
                orderItemsData = [];
                for (_i = 0, _b = cart.items; _i < _b.length; _i++) {
                    item = _b[_i];
                    if (item.book.stock < item.quantity) {
                        return [2 /*return*/, next(new AppError_js_1.AppError("Book '".concat(item.book.title, "' is out of stock or insufficient quantity"), 400))];
                    }
                    price = item.book.discountPrice || item.book.price;
                    total += price * item.quantity;
                    orderItemsData.push({
                        bookId: item.bookId,
                        quantity: item.quantity,
                        price: price
                    });
                }
                return [4 /*yield*/, prisma.$transaction(function (tx) { return __awaiter(void 0, void 0, void 0, function () {
                        var newOrder, _i, _a, item;
                        return __generator(this, function (_b) {
                            switch (_b.label) {
                                case 0: return [4 /*yield*/, tx.order.create({
                                        data: {
                                            userId: userId,
                                            invoiceNumber: generateInvoiceNumber(),
                                            total: total,
                                            status: 'PENDING',
                                            paymentMethod: paymentMethod,
                                            shippingAddress: shippingAddress,
                                            courier: courier,
                                            items: {
                                                create: orderItemsData
                                            }
                                        },
                                        include: {
                                            items: {
                                                include: { book: true }
                                            }
                                        }
                                    })];
                                case 1:
                                    newOrder = _b.sent();
                                    _i = 0, _a = cart.items;
                                    _b.label = 2;
                                case 2:
                                    if (!(_i < _a.length)) return [3 /*break*/, 5];
                                    item = _a[_i];
                                    return [4 /*yield*/, tx.book.update({
                                            where: { id: item.bookId },
                                            data: { stock: { decrement: item.quantity } }
                                        })];
                                case 3:
                                    _b.sent();
                                    _b.label = 4;
                                case 4:
                                    _i++;
                                    return [3 /*break*/, 2];
                                case 5: 
                                // Clear Cart
                                return [4 /*yield*/, tx.cartItem.deleteMany({
                                        where: { cartId: cart.id }
                                    })];
                                case 6:
                                    // Clear Cart
                                    _b.sent();
                                    return [2 /*return*/, newOrder];
                            }
                        });
                    }); })];
            case 2:
                order = _c.sent();
                res.status(201).json({
                    status: 'success',
                    data: { order: order }
                });
                return [2 /*return*/];
        }
    });
}); });
exports.getMyOrders = (0, asyncHandler_js_1.asyncHandler)(function (req, res, next) { return __awaiter(void 0, void 0, void 0, function () {
    var userId, orders;
    return __generator(this, function (_a) {
        switch (_a.label) {
            case 0:
                userId = req.user.id;
                return [4 /*yield*/, prisma.order.findMany({
                        where: { userId: userId },
                        orderBy: { createdAt: 'desc' },
                        include: {
                            items: {
                                include: { book: true }
                            }
                        }
                    })];
            case 1:
                orders = _a.sent();
                res.status(200).json({
                    status: 'success',
                    data: { orders: orders }
                });
                return [2 /*return*/];
        }
    });
}); });
exports.getOrderById = (0, asyncHandler_js_1.asyncHandler)(function (req, res, next) { return __awaiter(void 0, void 0, void 0, function () {
    var id, userId, userRole, order;
    return __generator(this, function (_a) {
        switch (_a.label) {
            case 0:
                id = req.params.id;
                userId = req.user.id;
                userRole = req.user.role;
                return [4 /*yield*/, prisma.order.findUnique({
                        where: { id: id },
                        include: {
                            user: {
                                select: { name: true, email: true }
                            },
                            items: {
                                include: { book: true }
                            }
                        }
                    })];
            case 1:
                order = _a.sent();
                if (!order) {
                    return [2 /*return*/, next(new AppError_js_1.AppError('Order not found', 404))];
                }
                // Check ownership or admin role
                if (order.userId !== userId && userRole !== 'admin' && userRole !== 'ADMIN') {
                    return [2 /*return*/, next(new AppError_js_1.AppError('You do not have permission to view this order', 403))];
                }
                res.status(200).json({
                    status: 'success',
                    data: { order: order }
                });
                return [2 /*return*/];
        }
    });
}); });
exports.cancelOrder = (0, asyncHandler_js_1.asyncHandler)(function (req, res, next) { return __awaiter(void 0, void 0, void 0, function () {
    var id, userId, order;
    return __generator(this, function (_a) {
        switch (_a.label) {
            case 0:
                id = req.params.id;
                userId = req.user.id;
                return [4 /*yield*/, prisma.order.findUnique({
                        where: { id: id }
                    })];
            case 1:
                order = _a.sent();
                if (!order) {
                    return [2 /*return*/, next(new AppError_js_1.AppError('Order not found', 404))];
                }
                if (order.userId !== userId) {
                    return [2 /*return*/, next(new AppError_js_1.AppError('You do not have permission to cancel this order', 403))];
                }
                if (order.status !== 'PENDING') {
                    return [2 /*return*/, next(new AppError_js_1.AppError('Cannot cancel order that is not pending', 400))];
                }
                // Restore stock and update status
                return [4 /*yield*/, prisma.$transaction(function (tx) { return __awaiter(void 0, void 0, void 0, function () {
                        var orderItems, _i, orderItems_1, item;
                        return __generator(this, function (_a) {
                            switch (_a.label) {
                                case 0: return [4 /*yield*/, tx.orderItem.findMany({
                                        where: { orderId: id }
                                    })];
                                case 1:
                                    orderItems = _a.sent();
                                    _i = 0, orderItems_1 = orderItems;
                                    _a.label = 2;
                                case 2:
                                    if (!(_i < orderItems_1.length)) return [3 /*break*/, 5];
                                    item = orderItems_1[_i];
                                    return [4 /*yield*/, tx.book.update({
                                            where: { id: item.bookId },
                                            data: { stock: { increment: item.quantity } }
                                        })];
                                case 3:
                                    _a.sent();
                                    _a.label = 4;
                                case 4:
                                    _i++;
                                    return [3 /*break*/, 2];
                                case 5: return [4 /*yield*/, tx.order.update({
                                        where: { id: id },
                                        data: { status: 'CANCELLED' }
                                    })];
                                case 6:
                                    _a.sent();
                                    return [2 /*return*/];
                            }
                        });
                    }); })];
            case 2:
                // Restore stock and update status
                _a.sent();
                res.status(200).json({
                    status: 'success',
                    message: 'Order cancelled successfully'
                });
                return [2 /*return*/];
        }
    });
}); });
// Admin Controllers
exports.getAllOrders = (0, asyncHandler_js_1.asyncHandler)(function (req, res, next) { return __awaiter(void 0, void 0, void 0, function () {
    var orders;
    return __generator(this, function (_a) {
        switch (_a.label) {
            case 0: return [4 /*yield*/, prisma.order.findMany({
                    orderBy: { createdAt: 'desc' },
                    include: {
                        user: {
                            select: { name: true, email: true }
                        },
                        items: {
                            include: { book: true } // Don't include book details to keep response light if many orders? Maybe ok for now.
                        }
                    }
                })];
            case 1:
                orders = _a.sent();
                res.status(200).json({
                    status: 'success',
                    data: { orders: orders }
                });
                return [2 /*return*/];
        }
    });
}); });
exports.updateOrderStatus = (0, asyncHandler_js_1.asyncHandler)(function (req, res, next) { return __awaiter(void 0, void 0, void 0, function () {
    var id, _a, status, resi, order;
    return __generator(this, function (_b) {
        switch (_b.label) {
            case 0:
                id = req.params.id;
                _a = req.body, status = _a.status, resi = _a.resi;
                return [4 /*yield*/, prisma.order.update({
                        where: { id: id },
                        data: __assign(__assign(__assign({ status: status, resi: resi || undefined }, (status === 'SHIPPED' ? { shippedAt: new Date() } : {})), (status === 'DELIVERED' ? { deliveredAt: new Date() } : {})), (status === 'PAID' ? { paidAt: new Date() } : {}))
                    })];
            case 1:
                order = _b.sent();
                res.status(200).json({
                    status: 'success',
                    data: { order: order }
                });
                return [2 /*return*/];
        }
    });
}); });
exports.uploadPaymentProof = (0, asyncHandler_js_1.asyncHandler)(function (req, res, next) { return __awaiter(void 0, void 0, void 0, function () {
    var id, userId, paymentProof, order, updatedOrder;
    return __generator(this, function (_a) {
        switch (_a.label) {
            case 0:
                id = req.params.id;
                userId = req.user.id;
                paymentProof = req.body.paymentProof;
                // Validate if file was uploaded
                if (!paymentProof) {
                    return [2 /*return*/, next(new AppError_js_1.AppError('No image uploaded', 400))];
                }
                return [4 /*yield*/, prisma.order.findUnique({
                        where: { id: id }
                    })];
            case 1:
                order = _a.sent();
                if (!order) {
                    return [2 /*return*/, next(new AppError_js_1.AppError('Order not found', 404))];
                }
                // Ensure user owns the order
                if (order.userId !== userId) {
                    return [2 /*return*/, next(new AppError_js_1.AppError('You do not have permission to upload proof for this order', 403))];
                }
                return [4 /*yield*/, prisma.order.update({
                        where: { id: id },
                        data: { paymentProof: paymentProof }
                    })];
            case 2:
                updatedOrder = _a.sent();
                res.status(200).json({
                    status: 'success',
                    data: { order: updatedOrder }
                });
                return [2 /*return*/];
        }
    });
}); });
exports.deleteOrder = (0, asyncHandler_js_1.asyncHandler)(function (req, res, next) { return __awaiter(void 0, void 0, void 0, function () {
    var id, order;
    return __generator(this, function (_a) {
        switch (_a.label) {
            case 0:
                id = req.params.id;
                return [4 /*yield*/, prisma.order.findUnique({
                        where: { id: id },
                        include: { items: true }
                    })];
            case 1:
                order = _a.sent();
                if (!order) {
                    return [2 /*return*/, next(new AppError_js_1.AppError('Order not found', 404))];
                }
                return [4 /*yield*/, prisma.$transaction(function (tx) { return __awaiter(void 0, void 0, void 0, function () {
                        var _i, _a, item;
                        return __generator(this, function (_b) {
                            switch (_b.label) {
                                case 0:
                                    if (!(order.status !== 'CANCELLED')) return [3 /*break*/, 4];
                                    _i = 0, _a = order.items;
                                    _b.label = 1;
                                case 1:
                                    if (!(_i < _a.length)) return [3 /*break*/, 4];
                                    item = _a[_i];
                                    return [4 /*yield*/, tx.book.update({
                                            where: { id: item.bookId },
                                            data: { stock: { increment: item.quantity } }
                                        })];
                                case 2:
                                    _b.sent();
                                    _b.label = 3;
                                case 3:
                                    _i++;
                                    return [3 /*break*/, 1];
                                case 4: 
                                // Delete order (Cascade deletion of OrderItems should happen if schema is configured, otherwise delete items first)
                                // Let's delete items explicitly to be safe
                                return [4 /*yield*/, tx.orderItem.deleteMany({
                                        where: { orderId: id }
                                    })];
                                case 5:
                                    // Delete order (Cascade deletion of OrderItems should happen if schema is configured, otherwise delete items first)
                                    // Let's delete items explicitly to be safe
                                    _b.sent();
                                    return [4 /*yield*/, tx.order.delete({
                                            where: { id: id }
                                        })];
                                case 6:
                                    _b.sent();
                                    return [2 /*return*/];
                            }
                        });
                    }); })];
            case 2:
                _a.sent();
                res.status(204).json({
                    status: 'success',
                    data: null
                });
                return [2 /*return*/];
        }
    });
}); });
