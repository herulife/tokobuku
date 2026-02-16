import { PrismaClient } from '@prisma/client';

const prisma = new PrismaClient();

async function setAdminAsSuperAdmin() {
    try {
        console.log('👑 Mengupgrade akun admin menjadi SUPER_ADMIN...\n');

        const admin = await prisma.user.update({
            where: { email: 'admin@cintabuku.com' },
            data: { role: 'SUPER_ADMIN' }
        });

        console.log(`✅ ${admin.name} (${admin.email}) → SUPER_ADMIN`);
        console.log('\n✨ Akun admin sudah diupgrade ke SUPER_ADMIN!');

    } catch (error) {
        console.error('❌ Error:', error);
    } finally {
        await prisma.$disconnect();
    }
}

setAdminAsSuperAdmin();
