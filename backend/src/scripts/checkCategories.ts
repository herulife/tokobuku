import { PrismaClient } from '@prisma/client';

const prisma = new PrismaClient();

async function checkAndSeedCategories() {
    try {
        const categories = await prisma.category.findMany();

        if (categories.length === 0) {
            console.log('📝 Tidak ada kategori, membuat kategori default...\n');

            const defaultCategories = [
                { name: 'Fiksi', slug: 'fiksi' },
                { name: 'Nonfiksi', slug: 'nonfiksi' },
                { name: 'Self Improvement', slug: 'self-improvement' },
                { name: 'Bisnis', slug: 'bisnis' },
                { name: 'Anak', slug: 'anak' },
                { name: 'Komik', slug: 'komik' }
            ];

            for (const cat of defaultCategories) {
                await prisma.category.create({ data: cat });
                console.log(`✅ Kategori "${cat.name}" dibuat`);
            }

            console.log('\n✨ Kategori berhasil dibuat!');
        } else {
            console.log('✅ Kategori yang tersedia:');
            categories.forEach(cat => {
                console.log(`   - ${cat.name} (${cat.slug})`);
            });
        }
    } catch (error) {
        console.error('❌ Error:', error);
    } finally {
        await prisma.$disconnect();
    }
}

checkAndSeedCategories();
