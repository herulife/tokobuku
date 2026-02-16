import axios from 'axios';

const apiKey = 'd5a8e43de70cb0dfd7b717e19f76fdefc9df62c74f4094f7ed9e759103ca5157';

async function check() {
    try {
        console.log("Testing /wilayah/kabupaten WITHOUT id_provinsi...");
        const res = await axios.get('https://api.binderbyte.com/wilayah/kabupaten', {
            params: { api_key: apiKey },
            validateStatus: () => true
        });
        console.log("Status:", res.status);
        console.log("Response Count:", res.data.value ? res.data.value.length : 0);
        if (res.data.value && res.data.value.length > 0) {
            console.log("Sample:", JSON.stringify(res.data.value[0], null, 2));
        } else {
            console.log("Response:", JSON.stringify(res.data, null, 2));
        }
    } catch (e) {
        console.log("Error without id_provinsi:", e.message);
    }
}

check();
