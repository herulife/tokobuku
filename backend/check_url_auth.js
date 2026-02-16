import axios from 'axios';

const apiKey = 'mPKXAhtf5dad13a7ba03f27bYBtVMvjI';
const urls = [
    'https://api.collaborator.komerce.id/destination/domestic-destination?search=jakarta',
    'https://api.collaborator.komerce.id/api/v1/destination/domestic-destination?search=jakarta',
    'https://api.collaborator.komerce.id/v1/destination/domestic-destination?search=jakarta',
    'https://api.collaborator.komerce.id/api/v1/destination/search?keyword=jakarta' // Old path check
];

async function check() {
    for (const url of urls) {
        try {
            console.log(`Checking ${url}...`);
            const res = await axios.get(url, {
                headers: { 'x-api-key': apiKey },
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
