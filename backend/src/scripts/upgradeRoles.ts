import { PrismaClient } from '@prisma/client';

const prisma = new PrismaClient();

async function upgradeAdminsToSuperAdmin() {
    try {
        console.log('🔄 Mengupgrade ADMIN menjadi SUPER_ADMIN...\n');

        // Update all existing ADMINs to SUPER_ADMIN
        const result = await prisma.user.updateMany({
            where: { role: 'ADMIN' },
            data: { role: 'SUPER_ADMIN' }
        });

        console.log(`✅ ${result.count} user berhasil diupgrade dari ADMIN → SUPER_ADMIN`);

        // Show current users
        const users = await prisma.user.findMany({
            select: {
                name: true,
                email: true,
                role: true
            }
        });

        console.log('\n📋 Daftar user setelah upgrade:');
        users.forEach(u => {
            const emoji = u.role === 'SUPER_ADMIN' ? '👑' : u.role === 'ADMIN' ? '⚙️' : '👤';
            console.log(`   ${emoji} ${u.name} (${u.email}) - ${u.role}`);
        });

        console.log('\n✨ Selesai! Sistem sekarang menggunakan 3 role:');
        console.log('   👑 SUPER_ADMIN: Full access (settings, user management, all features)');
        console.log('   ⚙️ ADMIN: Product & order management (no settings/user management)');
        console.log('   👤 USER: Customer access');

    } catch (error) {
        console.error('❌ Error:', error);
    } finally {
        await prisma.$disconnect();
    }
}

upgradeAdminsToSuperAdmin();
