import service from './services/rajaongkir.service.js';
import prisma from './lib/prisma.js';

async function testIntegration() {
    try {
        console.log('--- TEST INTEGRATION KOMERCE (SANDBOX) ---');

        // 0. Force User Provided Base URL with /tariff/api/v1 (Sandbox)
        const userBaseUrl = 'https://api-sandbox.collaborator.komerce.id/tariff/api/v1';
        console.log(`0. Setting Base URL to ${userBaseUrl}`);

        await prisma.setting.upsert({
            where: { key: 'rajaongkir_base_url' },
            create: { key: 'rajaongkir_base_url', value: userBaseUrl },
            update: { value: userBaseUrl }
        });

        // 1. Search for Origin (e.g., "Sleman")
        console.log('\n1. Searching Origin "Sleman"...');
        const origins = await service.searchDestination('Sleman');
        console.log(`Found ${origins.length} locations for "Sleman".`);
        if (origins.length === 0) throw new Error('No origin found');

        const origin = origins[0];
        console.log('Selected Origin:', origin);

        // 2. Search for Destination (e.g., "Gambir")
        console.log('\n2. Searching Destination "Gambir"...');
        const destinations = await service.searchDestination('Gambir');
        console.log(`Found ${destinations.length} locations for "Gambir".`);
        if (destinations.length === 0) throw new Error('No destination found');

        const destination = destinations[0];
        console.log('Selected Destination:', destination);

        // 3. Update Settings (mimic Admin saving settings)
        console.log('\n3. Updating Settings...');
        await prisma.setting.upsert({
            where: { key: 'rajaongkir_origin_city_id' },
            create: { key: 'rajaongkir_origin_city_id', value: String(origin.id) },
            update: { value: String(origin.id) }
        });

        await prisma.setting.upsert({
            where: { key: 'rajaongkir_origin_city_name' },
            create: { key: 'rajaongkir_origin_city_name', value: origin.label || origin.name || origin.destination_name },
            update: { value: origin.label || origin.name || origin.destination_name }
        });

        // 4. Calculate Cost
        console.log('\n4. Calculating Cost...');
        const weight = 1000; // 1kg
        const courier = 'jne';

        const costs = await service.calculateCost(String(origin.id), String(destination.id), weight, courier);
        console.log('Costs calculated:', JSON.stringify(costs, null, 2));

        if (costs.length > 0) {
            console.log('\nSUCCESS: Shipping costs retrieved.');
        } else {
            console.log('\nWARNING: No costs returned (empty list).');
        }

    } catch (error: any) {
        console.error('TEST FAILED:', error.message);
        if (error.response) {
            console.error('Response Status:', error.response.status);
            console.error('Response Data:', error.response.data);
        }
    } finally {
        await prisma.$disconnect();
    }
}

testIntegration();
