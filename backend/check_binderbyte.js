import axios from 'axios';

const apiKey = 'd5a8e43de70cb0dfd7b717e19f76fdefc9df62c74f4094f7ed9e759103ca5157';
const urls = [
    'https://api.binderbyte.com/v1/list_courier',
    'https://api.binderbyte.com/v1/courier',
    'https://api.binderbyte.com/v1/track?courier=jne&awb=1234567890', // Dummy
    'https://api.binderbyte.com/v1/cost?origin=501&destination=114&weight=1700&courier=jne' // RajaOngkir style params
];

async function check() {
    for (const url of urls) {
        try {
            console.log(`Checking ${url}...`);
            // Try with api_key query param
            const resQuery = await axios.get(`${url}${url.includes('?') ? '&' : '?'}api_key=${apiKey}`, {
                validateStatus: () => true
            });
            console.log(`Query Param Status: ${resQuery.status}`);
            if (resQuery.status === 200) console.log(`Data:`, JSON.stringify(resQuery.data).substring(0, 200));

            // Try with header (if query failed)
            if (resQuery.status !== 200) {
                console.log(`Retrying with header...`);
                // Try different header names
                const headers = {};
                // headers['api_key'] = apiKey; // Common
                // headers['x-api-key'] = apiKey; // Common
                // headers['x-api-co-id'] = apiKey; // Mentioned in search result?

                // Let's try x-api-key first as it is standard
                const resHeader = await axios.get(url, {
                    headers: { 'api_key': apiKey },
                    validateStatus: () => true
                });
                console.log(`Header 'api_key' Status: ${resHeader.status}`);
            }

        } catch (err) {
            console.error(`Error: ${err.message}`);
        }
    }
}

check();
