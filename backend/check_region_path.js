import axios from 'axios';

const apiKey = 'd5a8e43de70cb0dfd7b717e19f76fdefc9df62c74f4094f7ed9e759103ca5157';
const urls = [
    'https://api.binderbyte.com/wilayah/provinsi', // Previous 500
    'http://api.binderbyte.com/wilayah/provinsi', // HTTP
    'https://api.binderbyte.com/v1/wilayah/provinsi', // Versioned
    'https://api.binderbyte.com/api/wilayah/provinsi'
];

async function check() {
    for (const url of urls) {
        try {
            console.log(`Checking ${url}...`);
            const res = await axios.get(`${url}${url.includes('?') ? '&' : '?'}api_key=${apiKey}`, { validateStatus: () => true });
            console.log(`Status: ${res.status}`);
            if (res.status === 200) console.log(`Data:`, JSON.stringify(res.data).substring(0, 200));
        } catch (err) {
            console.error(`Error: ${err.message}`);
        }
    }
}

check();
