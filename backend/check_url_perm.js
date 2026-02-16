import axios from 'axios';

const apiKey = 'mPKXAhtf5dad13a7ba03f27bYBtVMvjI';
const hosts = [
    'https://api.collaborator.komerce.id',
    'https://api-sandbox.collaborator.komerce.id'
];

const paths = [
    '',
    '/v1',
    '/api',
    '/api/v1',
    '/destination/domestic-destination',
    '/v1/destination/domestic-destination',
    '/api/v1/destination/domestic-destination',
    '/destination/search',
    '/v1/destination/search',
    '/api/v1/destination/search'
];

async function check() {
    for (const host of hosts) {
        for (const path of paths) {
            const url = `${host}${path}`;
            try {
                const res = await axios.get(url, {
                    headers: {
                        'x-api-key': apiKey,
                        'User-Agent': 'Mozilla/5.0',
                        'Content-Type': 'application/json'
                    },
                    validateStatus: () => true,
                    timeout: 5000
                });
                console.log(`${url} -> ${res.status}`);
            } catch (err) {
                console.log(`${url} -> Error: ${err.message}`);
            }
        }
    }
}

check();
