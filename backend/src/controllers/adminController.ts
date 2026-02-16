import { Request, Response, NextFunction } from 'express';
import { PrismaClient } from '@prisma/client';
import { asyncHandler } from '../middlewares/asyncHandler';

const prisma = new PrismaClient();

export const getDashboardStats = asyncHandler(async (req: Request, res: Response, next: NextFunction) => {
    // 1. Basic Counts
    const [totalBooks, totalUsers, totalOrders] = await Promise.all([
        prisma.book.count(),
        prisma.user.count(),
        prisma.order.count()
    ]);

    // 2. Total Revenue (Only PAID, SHIPPED, DELIVERED)
    const revenueResult = await prisma.order.aggregate({
        _sum: {
            total: true
        },
        where: {
            status: {
                in: ['PAID', 'SHIPPED', 'DELIVERED']
            }
        }
    });
    const totalRevenue = revenueResult._sum.total || 0;

    // 3. Pending Orders
    const pendingOrders = await prisma.order.count({
        where: { status: 'PENDING' }
    });

    // 4. Recent Orders (5)
    const recentOrders = await prisma.order.findMany({
        take: 5,
        orderBy: { createdAt: 'desc' },
        include: {
            user: {
                select: { name: true, email: true }
            }
        }
    });

    // 5. Sales Chart (Last 7 Days)
    // Prisma doesn't support complex date grouping easily across databases without raw query.
    // We will fetch orders from last 7 days and group in JS for simplicity & DB compatibility.
    const sevenDaysAgo = new Date();
    sevenDaysAgo.setDate(sevenDaysAgo.getDate() - 7);

    const last7DaysOrders = await prisma.order.findMany({
        where: {
            createdAt: { gte: sevenDaysAgo },
            status: { in: ['PAID', 'SHIPPED', 'DELIVERED'] }
        },
        select: {
            createdAt: true,
            total: true
        }
    });

    // Group by date
    const salesChart = [];
    for (let i = 6; i >= 0; i--) {
        const date = new Date();
        date.setDate(date.getDate() - i);
        const dateStr = date.toISOString().split('T')[0]; // YYYY-MM-DD

        const dailyTotal = last7DaysOrders
            .filter(o => o.createdAt.toISOString().split('T')[0] === dateStr)
            .reduce((acc, curr) => acc + curr.total, 0);

        salesChart.push({
            date: dateStr, // Or format as 'DD MMM'
            total: dailyTotal
        });
    }

    res.status(200).json({
        status: 'success',
        data: {
            stats: {
                totalBooks,
                totalUsers,
                totalOrders,
                totalRevenue,
                pendingOrders,
                recentOrders,
                salesChart
            }
        }
    });
});
