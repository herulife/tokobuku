const axios = require('axios');

const apiKey = 'd5a8e43de70cb0dfd7b717e19f76fdefc9df62c74f4094f7ed9e759103ca5157';

async function check() {
    try {
        console.log("Testing Region API WITHOUT /v1...");
        const res = await axios.get('https://api.binderbyte.com/wilayah/provinsi', {
            params: { api_key: apiKey }
        });
        console.log("Status:", res.status);
        console.log("Data:", JSON.stringify(res.data, null, 2));
    } catch (e) {
        console.log("Error without /v1:", e.message);
        if (e.response) console.log("Response:", e.response.data);
    }

    console.log("---------------------------------------------------");

    try {
        console.log("Testing Region API WITH /v1 (Previous Code)...");
        const res = await axios.get('https://api.binderbyte.com/v1/wilayah/provinsi', {
            params: { api_key: apiKey }
        });
        console.log("Status:", res.status);
    } catch (e) {
        console.log("Error with /v1:", e.message);
        if (e.response) console.log("Response:", e.response.status);
    }
}

check();
