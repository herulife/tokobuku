
import { PrismaClient } from '@prisma/client';
import axios from 'axios';

const prisma = new PrismaClient();

async function main() {
    console.log('--- Testing API Cost Endpoint ---');

    const apiKeySetting = await prisma.setting.findUnique({
        where: { key: 'rajaongkir_api_key' }
    });

    const token = 'EryXeiVR78e23652ad1e2f93giZZc37G';
    console.log('Using API Key:', token.substring(0, 10) + '...');

    try {
        const response = await axios.get(`https://api.binderbyte.com/v1/cost`, {
            headers: { 'x-api-key': token },
            params: {
                origin: '3172',
                destination: '3278',
                weight: 1000,
                courier: 'jne'
            }
        });

        if (response.data && response.data.data) {
            console.log('✅ API Cost Response:', JSON.stringify(response.data.data, null, 2));
        } else {
            console.log('⚠️ API seems valid but returned empty data structure:', response.data);
        }

    } catch (error: any) {
        console.error('❌ API Error.');
        if (error.response) {
            console.error('Status:', error.response.status);
            console.error('Data:', error.response.data);
        } else {
            console.error('Error:', error.message);
        }
    }
}

main()
    .catch(e => console.error(e))
    .finally(async () => {
        await prisma.$disconnect();
    });
