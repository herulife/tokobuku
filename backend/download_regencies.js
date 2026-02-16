import fs from 'fs';
import https from 'https';
import path from 'path';

const dir = 'src/data';
if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir, { recursive: true });
}

const file = fs.createWriteStream("src/data/regencies.json");
const request = https.get("https://raw.githubusercontent.com/yusufsyaifudin/wilayah-indonesia/master/data/list_of_area/regencies.json", function (response) {
    if (response.statusCode !== 200) {
        console.error(`Failed to download: ${response.statusCode}`);
        return;
    }
    response.pipe(file);
    file.on('finish', () => {
        file.close();
        console.log("Download completed.");
    });
}).on('error', (err) => {
    fs.unlink("src/data/regencies.json", () => { }); // Delete the file async
    console.error(`Error downloading: ${err.message}`);
});
