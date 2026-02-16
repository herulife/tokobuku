import { PrismaClient } from '@prisma/client';
import bcrypt from 'bcrypt';

const prisma = new PrismaClient();

async function promoteAdmin() {
    const email = 'admin@example.com';
    const password = 'password123';
    const hashedPassword = await bcrypt.hash(password, 12);

    try {
        const existingUser = await prisma.user.findUnique({ where: { email } });

        if (existingUser) {
            console.log(`User ${email} found. Promoting to ADMIN...`);
            await prisma.user.update({
                where: { email },
                data: { role: 'ADMIN' }
            });
        } else {
            console.log(`User ${email} not found. Creating ADMIN user...`);
            await prisma.user.create({
                data: {
                    name: 'Super Admin',
                    email,
                    password: hashedPassword,
                    role: 'ADMIN'
                }
            });
        }
        console.log('Admin user ready.');
    } catch (e) {
        console.error(e);
    } finally {
        await prisma.$disconnect();
    }
}

promoteAdmin();
