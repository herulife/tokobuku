
const API_URL = 'http://localhost:5000/api/v1';

async function test() {
    try {
        // 1. Register User
        const email = `testcart_${Date.now()}@example.com`;
        console.log(`Registering user: ${email}`);
        const regRes = await fetch(`${API_URL}/auth/register`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                email,
                password: 'password123',
                confirmPassword: 'password123',
                name: 'Cart Tester'
            })
        });

        const regData = await regRes.json();
        if (!regRes.ok) throw new Error(`Register failed: ${JSON.stringify(regData)}`);
        const token = regData.token;
        console.log('User registered. Token:', token ? 'OK' : 'MISSING');

        // 2. Get Books
        console.log('Fetching books...');
        const bookRes = await fetch(`${API_URL}/books?limit=1`);
        const bookData = await bookRes.json();
        if (!bookRes.ok) throw new Error(`Get books failed: ${JSON.stringify(bookData)}`);

        const bookId = bookData.data.books[0]?.id;
        if (!bookId) throw new Error('No books found to test with');
        console.log(`Using Book ID: ${bookId}`);

        // 3. Add to Cart
        console.log('Adding to cart...');
        const addCartRes = await fetch(`${API_URL}/cart/items`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({ bookId, quantity: 1 })
        });
        const addCartData = await addCartRes.json();
        if (!addCartRes.ok) throw new Error(`Add to cart failed: ${JSON.stringify(addCartData)}`);
        console.log('Added to cart. Items:', addCartData.data.cart.items.length);

        // 4. Get Cart
        console.log('Fetching cart...');
        const getCartRes = await fetch(`${API_URL}/cart`, {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        const getCartData = await getCartRes.json();
        if (!getCartRes.ok) throw new Error(`Get cart failed: ${JSON.stringify(getCartData)}`);
        console.log('Cart fetched. Items:', getCartData.data.cart.items.length);

        // 5. Add to Wishlist
        console.log('Adding to wishlist...');
        const wishRes = await fetch(`${API_URL}/wishlist`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({ bookId })
        });
        const wishData = await wishRes.json();
        if (!wishRes.ok) throw new Error(`Add to wishlist failed: ${JSON.stringify(wishData)}`);
        console.log('Added to wishlist.');

        // 6. Get Wishlist
        console.log('Fetching wishlist...');
        const getWishRes = await fetch(`${API_URL}/wishlist`, {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        const getWishData = await getWishRes.json();
        if (!getWishRes.ok) throw new Error(`Get wishlist failed: ${JSON.stringify(getWishData)}`);
        console.log('Wishlist fetched. Items:', getWishData.data.wishlist.length);

        console.log('ALL TESTS PASSED');

    } catch (error) {
        console.error('TEST FAILED:', error.message);
        process.exit(1);
    }
}

test();
