import express from 'express';
import cors from 'cors';
import cookieParser from 'cookie-parser';
import helmet from 'helmet';
import dotenv from 'dotenv';
import { PrismaClient } from '@prisma/client';
import authRoutes from './routes/authRoutes';
import bookRoutes from './routes/bookRoutes';
import cartRoutes from './routes/cartRoutes';
import wishlistRoutes from './routes/wishlistRoutes';
import orderRoutes from './routes/orderRoutes';
import reviewRoutes from './routes/reviewRoutes';
import categoryRoutes from './routes/categoryRoutes';
import userRoutes from './routes/userRoutes';
import adminRoutes from './routes/adminRoutes';
import settingRoutes from './routes/settingRoutes';
import shippingRoutes from './routes/shippingRoutes';
import { errorHandler } from './middlewares/errorHandler';
import { AppError } from './utils/AppError';
import rateLimit from 'express-rate-limit';
import logger from './utils/logger';
import { validateEnv } from './utils/validateEnv';

dotenv.config();

// CRITICAL: Handle errors BEFORE anything else
process.on('uncaughtException', (error: Error) => {
    console.error('❌ UNCAUGHT EXCEPTION:', error.message);
    console.error('Stack:', error.stack);
    logger.error('UNCAUGHT EXCEPTION! Shutting down...', { error: error.message, stack: error.stack });
    process.exit(1);
});

process.on('unhandledRejection', (reason: any, promise: Promise<any>) => {
    console.error('❌ UNHANDLED REJECTION at:', promise);
    console.error('Reason:', reason);
    logger.error('UNHANDLED REJECTION! Shutting down...', { reason });
    process.exit(1);
});

// Validate environment variables
try {
    validateEnv();
    console.log('✅ Environment validated');
} catch (error) {
    console.error('❌ Environment validation failed:', error);
    process.exit(1);
}

const app = express();
const PORT = process.env.PORT || 5000;
const prisma = new PrismaClient();

// Middleware
app.use(helmet({
    crossOriginResourcePolicy: { policy: "cross-origin" },
}));
app.use(cookieParser());
app.use(express.json());
app.use(express.urlencoded({ extended: true }));
app.use(cors({
    origin: process.env.CLIENT_URL || 'http://localhost:3000',
    credentials: true,
}));

// Rate Limiting
const limiter = rateLimit({
    windowMs: 15 * 60 * 1000, // 15 minutes
    max: 100, // Limit each IP to 100 requests per windowMs
    message: 'Too many requests from this IP, please try again later.',
    standardHeaders: true,
    legacyHeaders: false,
    handler: (req, res) => {
        logger.warn(`Rate limit exceeded for IP: ${req.ip}`);
        res.status(429).json({
            status: 'error',
            message: 'Too many requests, please try again later.'
        });
    }
});

// Apply rate limiting to all API routes
app.use('/api/', limiter);

// Request logging middleware
app.use((req, res, next) => {
    logger.info(`${req.method} ${req.originalUrl}`, {
        ip: req.ip,
        userAgent: req.get('user-agent')
    });
    next();
});

// Serve static uploads
app.use('/uploads', express.static('public/uploads'));

// Routes
app.use('/api/v1/auth', authRoutes);
app.use('/api/v1/books', bookRoutes);
app.use('/api/v1/cart', cartRoutes);
app.use('/api/v1/wishlist', wishlistRoutes);
app.use('/api/v1/orders', orderRoutes);
app.use('/api/v1/reviews', reviewRoutes);
app.use('/api/v1/categories', categoryRoutes);
app.use('/api/v1/users', userRoutes); // For Delete /reviews/:id
app.use('/api/v1/admin', adminRoutes);
app.use('/api/v1/admin/settings', settingRoutes);
app.use('/api/v1/settings', settingRoutes); // Public access for /public endpoint
app.use('/api/v1/shipping', shippingRoutes);

// Health Check
app.get('/health', (req, res) => {
    res.status(200).json({
        status: 'ok',
        timestamp: new Date().toISOString(),
        uptime: process.uptime(),
        environment: process.env.NODE_ENV || 'development'
    });
});

app.get('/', (req, res) => {
    res.json({ message: 'Welcome to Koalisi Cinta Buku API' });
});

// 404 Handler
app.all('*', (req, res, next) => {
    next(new AppError(`Can't find ${req.originalUrl} on this server!`, 404));
});

// Global Error Handler
app.use(errorHandler);

// Start server and store reference
const server = app.listen(PORT, () => {
    logger.info(`🚀 Server running on port ${PORT}`);
    logger.info(`Environment: ${process.env.NODE_ENV || 'development'}`);
    logger.info(`CORS enabled for: ${process.env.CLIENT_URL || 'http://localhost:3000'}`);
    console.log(`\n✅ Server running on port ${PORT}`);
    console.log(`📊 Health check: http://localhost:${PORT}/health`);
    console.log(`⏰ Server started at: ${new Date().toISOString()}`);
    console.log(`🔄 Process will keep running...\n`);
});

// Keep server alive
server.on('error', (error) => {
    console.error('❌ Server error:', error);
    logger.error('Server error', { error });
});

// Prevent premature exit
process.stdin.resume();

process.on('SIGINT', async () => {
    console.log('\n🛑 SIGINT received, shutting down gracefully...');
    logger.info('Shutting down gracefully...');
    server.close(() => {
        console.log('✅ Server closed');
    });
    await prisma.$disconnect();
    logger.info('Database connection closed');
    process.exit(0);
});

process.on('SIGTERM', async () => {
    console.log('\n🛑 SIGTERM received, shutting down gracefully...');
    logger.info('SIGTERM signal received: closing HTTP server');
    server.close(() => {
        console.log('✅ Server closed');
    });
    await prisma.$disconnect();
    process.exit(0);
});
