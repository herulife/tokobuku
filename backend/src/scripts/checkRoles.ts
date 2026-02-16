import { PrismaClient } from '@prisma/client';

const prisma = new PrismaClient();

async function checkRoles() {
    try {
        const users = await prisma.user.findMany({
            where: {
                email: {
                    in: ['admin@cintabuku.com', 'testadmin@cintabuku.com']
                }
            },
            select: {
                email: true,
                role: true,
                name: true
            }
        });

        console.log('📊 Current Roles:');
        users.forEach(u => {
            console.log(`   - ${u.email}: ${u.role}`);
        });

    } catch (error) {
        console.error(error);
    } finally {
        await prisma.$disconnect();
    }
}

checkRoles();
