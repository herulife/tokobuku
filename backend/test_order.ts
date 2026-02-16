
const API_URL = 'http://localhost:5000/api/v1';

async function test() {
    try {
        // 1. Register User
        const email = `testorder_${Date.now()}@example.com`;
        console.log(`Registering user: ${email}`);
        const regRes = await fetch(`${API_URL}/auth/register`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                email,
                password: 'password123',
                confirmPassword: 'password123',
                name: 'Order Tester'
            })
        });

        const regData = await regRes.json();
        if (!regRes.ok) throw new Error(`Register failed: ${JSON.stringify(regData)}`);
        const token = regData.token;
        console.log('User registered.');

        // 2. Get Books
        const bookRes = await fetch(`${API_URL}/books?limit=1`);
        const bookData = await bookRes.json();
        const bookId = bookData.data.books[0]?.id;
        if (!bookId) throw new Error('No books found');
        console.log(`Using Book ID: ${bookId}`);

        // 3. Add to Cart
        console.log('Adding to cart...');
        await fetch(`${API_URL}/cart/items`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({ bookId, quantity: 1 })
        });

        // 4. Create Order (Checkout)
        console.log('Creating Order...');
        const orderRes = await fetch(`${API_URL}/orders`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({
                shippingAddress: 'Jalan Kenangan No. 123',
                paymentMethod: 'TRANSFER_BCA',
                courier: 'JNE'
            })
        });
        const orderData = await orderRes.json();
        if (!orderRes.ok) throw new Error(`Create Order failed: ${JSON.stringify(orderData)}`);
        const orderId = orderData.data.order.id;
        console.log(`Order created. ID: ${orderId}, Invoice: ${orderData.data.order.invoiceNumber}`);

        // 5. Get My Orders
        console.log('Fetching my orders...');
        const myOrdersRes = await fetch(`${API_URL}/orders`, {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        const myOrdersData = await myOrdersRes.json();
        if (myOrdersData.data.orders.length === 0) throw new Error('My orders is empty');
        console.log(`My Orders count: ${myOrdersData.data.orders.length}`);

        // 6. Get Order Detail
        console.log('Fetching order detail...');
        const detailRes = await fetch(`${API_URL}/orders/${orderId}`, {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        if (!detailRes.ok) throw new Error('Get order detail failed');
        console.log('Order detail fetched.');

        // 7. Test Admin - Login as Admin (Need to seed admin or upgrade user)
        // For now, we'll just test the user APIs. To test admin properly we need an admin account.
        // Let's create another user pending cancellation test. But we are good for basic flow.

        console.log('ALL ORDER TESTS PASSED');

    } catch (error) {
        console.error('TEST FAILED:', error.message);
        process.exit(1);
    }
}

test();
