import prisma from './src/lib/prisma.js';

const newKey = 'd5a8e43de70cb0dfd7b717e19f76fdefc9df62c74f4094f7ed9e759103ca5157';

async function update() {
    try {
        const result = await prisma.setting.update({
            where: { key: 'rajaongkir_api_key' },
            data: { value: newKey }
        });
        console.log('Updated Key:', result.value);
    } catch (e) {
        // If not found, create
        if (e.code === 'P2025') {
            const result = await prisma.setting.create({
                data: { key: 'rajaongkir_api_key', value: newKey }
            });
            console.log('Created Key:', result.value);
        } else {
            console.error(e);
        }
    }
}

update();
