import { PrismaClient } from '@prisma/client';

const prisma = new PrismaClient();

async function cleanupRajaOngkirSettings() {
    try {
        console.log('🧹 Menghapus settings RajaOngkir...\n');

        const rajaOngkirKeys = [
            'rajaongkir_api_key',
            'rajaongkir_base_url',
            'rajaongkir_origin_city_id',
            'rajaongkir_origin_city_name',
            'default_book_weight'
        ];

        const result = await prisma.setting.deleteMany({
            where: {
                key: {
                    in: rajaOngkirKeys
                }
            }
        });

        console.log(`✅ ${result.count} settings RajaOngkir berhasil dihapus`);

        // Show remaining settings
        const remaining = await prisma.setting.findMany();
        console.log('\n📋 Settings yang tersisa:');
        remaining.forEach(s => {
            console.log(`   - ${s.key}: ${s.value}`);
        });

        if (remaining.length === 0) {
            console.log('   (Tidak ada settings)');
        }

    } catch (error) {
        console.error('❌ Error:', error);
    } finally {
        await prisma.$disconnect();
    }
}

cleanupRajaOngkirSettings();
