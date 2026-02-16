
import { PrismaClient } from '@prisma/client';

const prisma = new PrismaClient();

async function main() {
    console.log('--- Updating Origin City Setting ---');

    const result = await prisma.setting.update({
        where: { key: 'rajaongkir_origin_city_id' },
        data: { value: '3278' } // '3278' is Kota Tasikmalaya
    });

    console.log('Updated Origin Setting:', result);
    console.log('Now the shipping cost for Kota Tasikmalaya should be 10.000');
}

main()
    .catch(e => console.error(e))
    .finally(async () => {
        await prisma.$disconnect();
    });
