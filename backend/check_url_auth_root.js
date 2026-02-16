import axios from 'axios';

const apiKey = 'mPKXAhtf5dad13a7ba03f27bYBtVMvjI';
const urls = [
    'https://api.collaborator.komerce.id',
    'https://api.collaborator.komerce.id/',
    'https://api.collaborator.komerce.id/v1/courier', // Guessing common endpoints
    'https://api.collaborator.komerce.id/api/v1/courier'
];

async function check() {
    for (const url of urls) {
        try {
            console.log(`Checking ${url}...`);
            const res = await axios.get(url, {
                headers: {
                    'x-api-key': apiKey,
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
                },
                validateStatus: () => true
            });
            console.log(`Status: ${res.status}`);
            console.log(`Data (first 200 chars):`, JSON.stringify(res.data).substring(0, 200));
        } catch (err) {
            console.error(`Error: ${err.message}`);
        }
    }
}

check();
