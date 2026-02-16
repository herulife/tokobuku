import axios from 'axios';

const urls = [
    'https://api.collaborator.komerce.id/api/v1/destination/domestic-destination',
    'https://api.collaborator.komerce.id/v1/destination/domestic-destination',
    'https://api.collaborator.komerce.id/destination/domestic-destination',
    'https://api.collaborator.komerce.id/api/v1/calculate',
    'https://api.collaborator.komerce.id/v1/calculate',
    'https://api.collaborator.komerce.id/calculate'
];

async function check() {
    for (const url of urls) {
        try {
            console.log(`Checking ${url}...`);
            const res = await axios.get(url, { validateStatus: () => true });
            console.log(`Status: ${res.status}`);
            console.log(`Data (first 200 chars):`, JSON.stringify(res.data).substring(0, 200));
        } catch (err) {
            console.error(`Error: ${err.message}`);
        }
    }
}

check();
