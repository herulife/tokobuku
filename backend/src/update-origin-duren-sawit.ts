
import { PrismaClient } from '@prisma/client';

const prisma = new PrismaClient();

async function main() {
    console.log('--- Updating Origin City Setting to JAKARTA TIMUR ---');

    // Duren Sawit is in Jakarta Timur (Regency ID 3172)
    const result = await prisma.setting.update({
        where: { key: 'rajaongkir_origin_city_id' },
        data: { value: '3172' }
    });

    console.log('Updated Origin Setting:', result);
}

main()
    .catch(e => console.error(e))
    .finally(async () => {
        await prisma.$disconnect();
    });
