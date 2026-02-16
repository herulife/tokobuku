import axios from 'axios';

const apiKey = 'mPKXAhtf5dad13a7ba03f27bYBtVMvjI';
const urls = [
    'https://api.collaborator.komerce.id/client/api/v1/destination/search?keyword=jakarta', // From search result
    'https://api.collaborator.komerce.id/client/api/v1/destination/domestic-destination?search=jakarta',
    'https://api.collaborator.komerce.id/api/v1/destination/domestic-destination', // Try POST
];

async function check() {
    for (const url of urls) {
        try {
            console.log(`Checking GET ${url}...`);
            const res = await axios.get(url, {
                headers: { 'x-api-key': apiKey },
                validateStatus: () => true
            });
            console.log(`GET Status: ${res.status}`);
            if (res.status !== 404) console.log(`Data:`, JSON.stringify(res.data).substring(0, 200));

            // Try POST for domestic-destination
            if (url.includes('domestic-destination')) {
                console.log(`Checking POST ${url}...`);
                const resPost = await axios.post(url, { search: 'jakarta' }, {
                    headers: { 'x-api-key': apiKey },
                    validateStatus: () => true
                });
                console.log(`POST Status: ${resPost.status}`);
                if (resPost.status !== 404) console.log(`Data:`, JSON.stringify(resPost.data).substring(0, 200));
            }

        } catch (err) {
            console.error(`Error: ${err.message}`);
        }
    }
}

check();
