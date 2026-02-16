
import axios from 'axios';

async function main() {
    console.log('--- Testing RajaOngkir API Key ---');
    const apiKey = 'EryXeiVR78e23652ad1e2f93giZZc37G'; // User provided key

    // RajaOngkir Starter URL
    const baseURL = 'https://api.rajaongkir.com/starter';

    try {
        // Test /city endpoint
        console.log(`Checking City endpoint: ${baseURL}/city?id=501`); // 501 is Yogyakarta
        const response = await axios.get(`${baseURL}/city`, {
            headers: { key: apiKey },
            params: { id: 501 }
        });

        if (response.data && response.data.rajaongkir.status.code === 200) {
            console.log('✅ API Key is VALID.');
            console.log('Data:', response.data.rajaongkir.results);
        } else {
            console.log('⚠️ API returned non-200 status:', response.data.rajaongkir.status);
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

main().catch(console.error);
