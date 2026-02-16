
import { PrismaClient } from '@prisma/client';
import axios from 'axios';

const prisma = new PrismaClient();

async function main() {
    console.log('--- Testing API Key Validity (BinderByte) ---');

    const token = 'EryXeiVR78e23652ad1e2f93giZZc37G';
    console.log('Using API Key:', token.substring(0, 10) + '...');

    try {
        const response = await axios.get(`https://api.binderbyte.com/v1/list_courier`, {
            params: { api_key: token }
        });

        if (response.data && response.data.length > 0) {
            console.log('✅ API Key is VALID. Connection successful.');
            console.log(`Found ${response.data.length} couriers.`);
        } else {
            console.log('⚠️ API Key seems valid but returned empty data.');
        }

    } catch (error: any) {
        console.error('❌ API Key might be INVALID or Expired.');
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
