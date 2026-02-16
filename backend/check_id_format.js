import axios from 'axios';

const apiKey = 'd5a8e43de70cb0dfd7b717e19f76fdefc9df62c74f4094f7ed9e759103ca5157';
// Origin IDs to test:
// 152: Jakarta Pusat (RajaOngkir)
// 31.71: Jakarta Pusat (Kemendagri)
// 3171: Jakarta Pusat (Kemendagri no dot)
// "JKT": Random string
const origins = ['152', '31.71', '3171', 'Jakarta Pusat'];

async function check() {
    for (const origin of origins) {
        try {
            console.log(`Testing Origin: ${origin}`);
            const res = await axios.get('https://api.binderbyte.com/v1/cost', {
                params: {
                    api_key: apiKey,
                    origin: origin,
                    destination: '151', // Jakarta Barat (RajaOngkir)
                    weight: 1000,
                    courier: 'jne'
                },
                validateStatus: () => true
            });
            // If message is "Account not yet subscribed", the ID format is likely VALID
            // If message is "Origin not found" or similar, ID is INVALID
            console.log(`Status: ${res.status}`);
            console.log(`Response:`, JSON.stringify(res.data));
        } catch (e) {
            console.error(e.message);
        }
        console.log('---');
    }
}

check();
