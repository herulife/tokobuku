
import dotenv from 'dotenv';
dotenv.config();

import komerceService from './services/rajaongkir.service.js';
import prisma from './lib/prisma.js';

async function test() {
    console.log('--- TESTING KOMERCE SHIPPING SERVICE ---');

    // FORCE UPDATE BASE URL TO SANDBOX
    try {
        await prisma.setting.upsert({
            where: { key: 'rajaongkir_base_url' },
            update: { value: 'https://api-sandbox.collaborator.komerce.id' },
            create: {
                key: 'rajaongkir_base_url',
                value: 'https://api-sandbox.collaborator.komerce.id'
            }
        });
        console.log('Updated DB to Sandbox URL');
    } catch (e: any) {
        console.error('Failed to update DB setting:', e.message);
    }



    // DEBUG: Probe rajaongkir.komerce.id
    const axios = (await import('axios')).default;
    const apiKey = 'mPKXAhtf5dad13a7ba03f27bYBtVMvjI';
    const domain = 'https://rajaongkir.komerce.id';

    console.log('\n--- DEBUG PROBE RAJAONGKIR.KOMERCE.ID ---');

    // 1. Check Root Auth
    try {
        console.log(`\n[ROOT] ${domain}/`);
        const r1 = await axios.get(`${domain}/`, { headers: { 'key': apiKey } });
        console.log('  Header [key]: 200 OK -', JSON.stringify(r1.data));
    } catch (e: any) { console.log('  Header [key]:', e.response?.status); }

    try {
        const r2 = await axios.get(`${domain}/`, { headers: { 'x-api-key': apiKey } });
        console.log('  Header [x-api-key]: 200 OK -', JSON.stringify(r2.data));
    } catch (e: any) { console.log('  Header [x-api-key]:', e.response?.status); }

    try {
        const r3 = await axios.get(`${domain}/`);
        console.log('  No Header: 200 OK -', JSON.stringify(r3.data));
    } catch (e: any) { console.log('  No Header:', e.response?.status); }

    // 2. Check Paths
    const paths = [
        '/tariff/api/v1/destination/search',
        '/api/v1/destination/search',
        '/v1/destination/search',
        '/destination/search',
        '/search'
    ];

    for (const p of paths) {
        console.log(`\n[PATH] ${p}`);
        try {
            await axios.get(`${domain}${p}`, { headers: { 'key': apiKey }, params: { keyword: 'Gambir' } });
            console.log('  Header [key]: SUCCESS');
        } catch (e: any) { process.stdout.write(`  [key:${e.response?.status}]`); }

        try {
            await axios.get(`${domain}${p}`, { headers: { 'x-api-key': apiKey }, params: { keyword: 'Gambir' } });
            console.log('  Header [x-api-key]: SUCCESS');
        } catch (e: any) { process.stdout.write(`  [x-api-key:${e.response?.status}]`); }
    }


    /*
    // OLD TEST LOGIC COMMENTED OUT
    try {
        // 1. Search Destination
        const keyword = 'Kecamatan Gambir'; // Try a specific location
        console.log(`\n1. Searching for: ${keyword}`);
        const locations = await komerceService.searchDestination(keyword);
        console.log(`Found ${locations.length} locations.`);
        if (locations.length > 0) {
            console.log('Sample:', JSON.stringify(locations[0], null, 2));
        } else {
            console.warn('No locations found. Check API Key or Keyword.');
        }

        // 2. Calculate Cost
        // Needs valid IDs. If search found something, use it.
        // Otherwise use hardcoded IDs if known, or skip.

        // We can't easily guess IDs without search result.
        if (locations.length > 0) {
            const destinationId = locations[0].id; // Adjust based on actual response structure
            // Let's search origin 'Banyumas' (example)
            const paramOrigin = 'Banyumas';
            const originLocs = await komerceService.searchDestination(paramOrigin);

            if (originLocs.length > 0) {
                const realOriginId = originLocs[0].id; // Adjust field name
                console.log(`Origin: ${originLocs[0].label} (${realOriginId})`);

                console.log(`\n2. Calculating Cost from ${paramOrigin} (${realOriginId}) to ${keyword} (${destinationId})`);
                const weight = 1000; // 1kg

                // Komerce returns ALL couriers. 'jne' filter might result in empty if JNE not available in sandbox or route.
                // Try courier 'all' first.
                const costs = await komerceService.calculateCost(realOriginId, destinationId, weight, 'all');
                console.log(`\nFound ${costs.length} shipping options.`);
                console.log(JSON.stringify(costs, null, 2));
            }
        }

    } catch (error: any) {
        console.error('Test Failed:', error.message);
        if (error.response) {
            console.error('Response Status:', error.response.status);
            console.error('Response Data:', error.response.data);
        }
    } finally {
        await prisma.$disconnect();
    }
    */
}

test();
