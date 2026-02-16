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
var express_1 = require("express");
var cors_1 = require("cors");
var cookie_parser_1 = require("cookie-parser");
var helmet_1 = require("helmet");
var dotenv_1 = require("dotenv");
var client_1 = require("@prisma/client");
var authRoutes_js_1 = require("./routes/authRoutes.js");
var bookRoutes_js_1 = require("./routes/bookRoutes.js");
var cartRoutes_js_1 = require("./routes/cartRoutes.js");
var wishlistRoutes_js_1 = require("./routes/wishlistRoutes.js");
var orderRoutes_js_1 = require("./routes/orderRoutes.js");
var reviewRoutes_js_1 = require("./routes/reviewRoutes.js");
var categoryRoutes_js_1 = require("./routes/categoryRoutes.js");
var userRoutes_js_1 = require("./routes/userRoutes.js");
var adminRoutes_js_1 = require("./routes/adminRoutes.js");
var settingRoutes_js_1 = require("./routes/settingRoutes.js");
var shippingRoutes_js_1 = require("./routes/shippingRoutes.js");
var errorHandler_js_1 = require("./middlewares/errorHandler.js");
var AppError_js_1 = require("./utils/AppError.js");
var express_rate_limit_1 = require("express-rate-limit");
var logger_js_1 = require("./utils/logger.js");
var validateEnv_js_1 = require("./utils/validateEnv.js");
dotenv_1.default.config();
// Validate environment variables
(0, validateEnv_js_1.validateEnv)();
var app = (0, express_1.default)();
var PORT = process.env.PORT || 5000;
var prisma = new client_1.PrismaClient();
// Middleware
app.use((0, helmet_1.default)({
    crossOriginResourcePolicy: { policy: "cross-origin" },
}));
app.use((0, cookie_parser_1.default)());
app.use(express_1.default.json());
app.use(express_1.default.urlencoded({ extended: true }));
app.use((0, cors_1.default)({
    origin: process.env.CLIENT_URL || 'http://localhost:3000',
    credentials: true,
}));
// Rate Limiting
var limiter = (0, express_rate_limit_1.default)({
    windowMs: 15 * 60 * 1000, // 15 minutes
    max: 100, // Limit each IP to 100 requests per windowMs
    message: 'Too many requests from this IP, please try again later.',
    standardHeaders: true,
    legacyHeaders: false,
    handler: function (req, res) {
        logger_js_1.default.warn("Rate limit exceeded for IP: ".concat(req.ip));
        res.status(429).json({
            status: 'error',
            message: 'Too many requests, please try again later.'
        });
    }
});
// Apply rate limiting to all API routes
app.use('/api/', limiter);
// Request logging middleware
app.use(function (req, res, next) {
    logger_js_1.default.info("".concat(req.method, " ").concat(req.originalUrl), {
        ip: req.ip,
        userAgent: req.get('user-agent')
    });
    next();
});
// Serve static uploads
app.use('/uploads', express_1.default.static('public/uploads'));
// Routes
app.use('/api/v1/auth', authRoutes_js_1.default);
app.use('/api/v1/books', bookRoutes_js_1.default);
app.use('/api/v1/cart', cartRoutes_js_1.default);
app.use('/api/v1/wishlist', wishlistRoutes_js_1.default);
app.use('/api/v1/orders', orderRoutes_js_1.default);
app.use('/api/v1/reviews', reviewRoutes_js_1.default);
app.use('/api/v1/categories', categoryRoutes_js_1.default);
app.use('/api/v1/users', userRoutes_js_1.default); // For Delete /reviews/:id
app.use('/api/v1/admin', adminRoutes_js_1.default);
app.use('/api/v1/admin/settings', settingRoutes_js_1.default);
app.use('/api/v1/settings', settingRoutes_js_1.default); // Public access for /public endpoint
app.use('/api/v1/shipping', shippingRoutes_js_1.default);
// Health Check
app.get('/health', function (req, res) {
    res.status(200).json({
        status: 'ok',
        timestamp: new Date().toISOString(),
        uptime: process.uptime(),
        environment: process.env.NODE_ENV || 'development'
    });
});
app.get('/', function (req, res) {
    res.json({ message: 'Welcome to Koalisi Cinta Buku API' });
});
// 404 Handler
app.all('*', function (req, res, next) {
    next(new AppError_js_1.AppError("Can't find ".concat(req.originalUrl, " on this server!"), 404));
});
// Global Error Handler
app.use(errorHandler_js_1.errorHandler);
// Start server
app.listen(PORT, function () {
    logger_js_1.default.info("\uD83D\uDE80 Server running on port ".concat(PORT));
    logger_js_1.default.info("Environment: ".concat(process.env.NODE_ENV || 'development'));
    logger_js_1.default.info("CORS enabled for: ".concat(process.env.CLIENT_URL || 'http://localhost:3000'));
    console.log("\n\u2705 Server running on port ".concat(PORT));
    console.log("\uD83D\uDCCA Health check: http://localhost:".concat(PORT, "/health\n"));
});
process.on('SIGINT', function () { return __awaiter(void 0, void 0, void 0, function () {
    return __generator(this, function (_a) {
        switch (_a.label) {
            case 0:
                logger_js_1.default.info('Shutting down gracefully...');
                return [4 /*yield*/, prisma.$disconnect()];
            case 1:
                _a.sent();
                logger_js_1.default.info('Database connection closed');
                process.exit(0);
                return [2 /*return*/];
        }
    });
}); });
process.on('SIGTERM', function () { return __awaiter(void 0, void 0, void 0, function () {
    return __generator(this, function (_a) {
        switch (_a.label) {
            case 0:
                logger_js_1.default.info('SIGTERM signal received: closing HTTP server');
                return [4 /*yield*/, prisma.$disconnect()];
            case 1:
                _a.sent();
                process.exit(0);
                return [2 /*return*/];
        }
    });
}); });
// Uncaught Exception Handler
process.on('uncaughtException', function (error) {
    logger_js_1.default.error('UNCAUGHT EXCEPTION! Shutting down...', { error: error.message, stack: error.stack });
    process.exit(1);
});
// Unhandled Rejection Handler
process.on('unhandledRejection', function (reason) {
    logger_js_1.default.error('UNHANDLED REJECTION! Shutting down...', { reason: reason });
    process.exit(1);
});
