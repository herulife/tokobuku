import axios from 'axios';

const apiKey = 'd5a8e43de70cb0dfd7b717e19f76fdefc9df62c74f4094f7ed9e759103ca5157';
const baseUrl = 'https://api.binderbyte.com/v1/cost';

async function check() {
    try {
        console.log(`Checking Cost with city names...`);
        const res = await axios.get(baseUrl, {
            params: {
                api_key: apiKey,
                courier: 'jne',
                origin: 'jakarta',
                destination: 'bandung',
                weight: '1000'
            },
            validateStatus: () => true
        });
        console.log(`City Name Status: ${res.status}`);
        console.log(`City Name Data:`, JSON.stringify(res.data).substring(0, 200));

        // Try with city IDs (RajaOngkir style)
        console.log(`Checking Cost with city IDs...`);
        const resId = await axios.get(baseUrl, {
            params: {
                api_key: apiKey,
                courier: 'jne',
                origin: '152', // Jakarta Pusat (RajaOngkir ID)
                destination: '23', // Bandung (RajaOngkir ID)
                weight: '1000'
            },
            validateStatus: () => true
        });
        console.log(`City ID Status: ${resId.status}`);
        console.log(`City ID Data:`, JSON.stringify(resId.data).substring(0, 200));

    } catch (err) {
        console.error(`Error: ${err.message}`);
    }
}

check();
