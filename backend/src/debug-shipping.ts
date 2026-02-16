
import { PrismaClient } from '@prisma/client';
import { regencies } from './data/region-data';
import { districts } from './data/district-data';

const prisma = new PrismaClient();

async function main() {
    console.log('--- Debugging Shipping Cost Logic ---');

    // 1. Check Origin Setting
    const originSetting = await prisma.setting.findUnique({
        where: { key: 'rajaongkir_origin_city_id' }
    });
    console.log('Origin Setting:', originSetting);

    const originId = originSetting?.value;
    const originRegency = regencies.find(r => r.id === originId);
    console.log('Resolved Origin Regency:', originRegency ? `${originRegency.name} (${originRegency.id})` : 'NOT FOUND');

    // 2. Check Destination: Kec. CIBEUREUM, KOTA TASIKMALAYA
    // We need to find "CIBEUREUM" that belongs to KOTA TASIKMALAYA (ID 3278)
    // First, verify KOTA TASIKMALAYA ID
    const kotaTasik = regencies.find(r => r.name === 'KOTA TASIKMALAYA');
    console.log('Kota Tasikmalaya ID:', kotaTasik?.id);

    if (kotaTasik) {
        const cibeureum = districts.find(d => d.name === 'CIBEUREUM' && d.regency_id === kotaTasik.id);
        console.log('Found Cibeureum in Kota Tasik?', cibeureum);

        if (cibeureum) {
            console.log('Destination Regency resolved via District:', regencies.find(r => r.id === cibeureum.regency_id)?.name);
        }
    }

    // 3. Simulate Calculation
    if (!originRegency) {
        console.log('Result: Origin not found. Returning 50k fallback.');
    } else if (kotaTasik) {
        // Assume destination is resolved to Kota Tasik
        if (originRegency.id === kotaTasik.id) {
            console.log('Result: Same City (10k)');
        } else if (originRegency.province_id === kotaTasik.province_id) {
            console.log('Result: Same Province (20k)');
        } else {
            console.log('Result: Different Province');
        }
    }
}

main()
    .catch(e => console.error(e))
    .finally(async () => {
        await prisma.$disconnect();
    });
