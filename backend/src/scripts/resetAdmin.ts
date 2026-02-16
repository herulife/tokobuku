
import { PrismaClient } from '@prisma/client';
import bcrypt from 'bcrypt';

const prisma = new PrismaClient();

async function main() {
    try {
        const hashedPassword = await bcrypt.hash('admin123', 12);
        const user = await prisma.user.update({
            where: { email: 'admin@cintabuku.com' },
            data: { password: hashedPassword, role: 'SUPER_ADMIN' }
        });
        console.log(`Updated user ${user.email} (Role: ${user.role}) - Password reset to admin123`);
    } catch (e) {
        console.error(e);
    } finally {
        await prisma.$disconnect();
    }
}

main();
