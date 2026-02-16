import prisma from './src/lib/prisma.js';

async function check() {
    const setting = await prisma.setting.findUnique({
        where: { key: 'rajaongkir_api_key' }
    });
    console.log('Current Key:', setting?.value);
}

check();
