import axios from 'axios';

const apiKey = 'd5a8e43de70cb0dfd7b717e19f76fdefc9df62c74f4094f7ed9e759103ca5157';

async function check() {
    try {
        console.log('Checking Provinces with Header...');
        const res = await axios.get('https://api.binderbyte.com/wilayah/provinsi', {
            headers: { 'api_key': apiKey }, // Try header 'api_key'
            validateStatus: () => true
        });
        console.log(`Status (Header 'api_key'): ${res.status}`);
        if (res.status === 200) console.log(JSON.stringify(res.data).substring(0, 200));

        const res2 = await axios.get('https://api.binderbyte.com/wilayah/provinsi', {
            params: { 'api_key': apiKey }, // Try query param again just in case
            validateStatus: () => true
        });
        console.log(`Status (Query 'api_key'): ${res2.status}`);

    } catch (e) {
        console.error(e.message);
    }
}

check();
