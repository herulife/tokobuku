import { PrismaClient } from '@prisma/client';
import bcrypt from 'bcrypt';

const prisma = new PrismaClient();

async function createTestAdmin() {
    try {
        console.log('👤 Membuat akun ADMIN test...\n');

        const hashedPassword = await bcrypt.hash('admin123', 10);

        const admin = await prisma.user.create({
            data: {
                name: 'Test Admin',
                email: 'testadmin@cintabuku.com',
                password: hashedPassword,
                role: 'ADMIN'
            }
        });

        console.log(`✅ Akun ADMIN test berhasil dibuat:`);
        console.log(`   Email: ${admin.email}`);
        console.log(`   Password: admin123`);
        console.log(`   Role: ${admin.role}`);
        console.log('\n💡 Silakan login dengan akun ini untuk test fitur ADMIN');
        console.log('   (Settings & Users menu TIDAK akan muncul)');

    } catch (error: any) {
        if (error.code === 'P2002') {
            console.log('⚠️  Akun testadmin@cintabuku.com sudah ada');
        } else {
            console.error('❌ Error:', error);
        }
    } finally {
        await prisma.$disconnect();
    }
}

createTestAdmin();
