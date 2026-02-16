import binderByteService from './src/services/binderbyte.service';

async function test() {
    console.log('Testing BinderByteService...');

    try {
        console.log('1. Get API Key');
        const key = await binderByteService.getApiKey();
        console.log('API Key:', key ? 'Found' : 'Not Found');

        console.log('2. Search Destination (Mock)');
        const destinations = await binderByteService.searchDestination('jakarta');
        console.log('Destinations:', destinations);

        console.log('3. Calculate Cost (Expect Error/Empty due to subscription)');
        const costs = await binderByteService.calculateCost('jakarta', 'bandung', 1000, 'jne');
        console.log('Costs:', costs);

        console.log('4. Get Couriers');
        const couriers = await binderByteService.getCouriers();
        console.log('Couriers:', JSON.stringify(couriers).substring(0, 100));

    } catch (err) {
        console.error('Test Error:', err);
    }
}

test();
