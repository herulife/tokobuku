import fs from 'fs';
import https from 'https';

const dir = 'src/data';
if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir, { recursive: true });
}

// Download JSON first into memory (90KB is fine)
let data = '';

https.get("https://raw.githubusercontent.com/yusufsyaifudin/wilayah-indonesia/master/data/list_of_area/regencies.json", function (response) {
    if (response.statusCode !== 200) {
        console.error(`Failed to download: ${response.statusCode}`);
        return;
    }

    response.on('data', (chunk) => {
        data += chunk;
    });

    response.on('end', () => {
        try {
            const json = JSON.parse(data);
            const tsContent = `export interface Regency {
    id: string;
    province_id: string;
    name: string;
    alt_name: string;
    latitude: number;
    longitude: number;
}

export const regencies: Regency[] = ${JSON.stringify(json, null, 2)};
`;
            fs.writeFileSync("src/data/region-data.ts", tsContent);
            console.log("Download and conversion completed.");
        } catch (e) {
            console.error("Error parsing JSON:", e);
        }
    });

}).on('error', (err) => {
    console.error(`Error downloading: ${err.message}`);
});
