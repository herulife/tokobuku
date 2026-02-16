import axios from 'axios';

const apiKey = 'd5a8e43de70cb0dfd7b717e19f76fdefc9df62c74f4094f7ed9e759103ca5157';
const urls = [
    'https://api.binderbyte.com/wilayah/provinsi',
    'https://api.binderbyte.com/wilayah/kabupaten?api_key=' + apiKey + '&name=jakarta', // Guessing query param
    'https://api.binderbyte.com/wilayah/kecamatan?api_key=' + apiKey + '&name=gambir',
    'https://api.binderbyte.com/wilayah/kelurahan?api_key=' + apiKey + '&name=gambir'
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
