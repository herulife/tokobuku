import { PrismaClient } from '@prisma/client';

const prisma = new PrismaClient();

async function resetData() {
    try {
        console.log('🧹 Membersihkan database...\n');

        // 1. Hapus OrderItems (karena ada relasi ke Orders)
        const deletedOrderItems = await prisma.orderItem.deleteMany();
        console.log(`✅ ${deletedOrderItems.count} OrderItems dihapus`);

        // 2. Hapus Orders
        const deletedOrders = await prisma.order.deleteMany();
        console.log(`✅ ${deletedOrders.count} Orders dihapus`);

        // 3. Hapus Reviews
        const deletedReviews = await prisma.review.deleteMany();
        console.log(`✅ ${deletedReviews.count} Reviews dihapus`);

        // 4. Hapus CartItems
        const deletedCartItems = await prisma.cartItem.deleteMany();
        console.log(`✅ ${deletedCartItems.count} CartItems dihapus`);

        // 5. Hapus Carts
        const deletedCarts = await prisma.cart.deleteMany();
        console.log(`✅ ${deletedCarts.count} Carts dihapus`);

        // 6. Hapus Wishlists
        const deletedWishlists = await prisma.wishlist.deleteMany();
        console.log(`✅ ${deletedWishlists.count} Wishlists dihapus`);

        // 7. Hapus Books
        const deletedBooks = await prisma.book.deleteMany();
        console.log(`✅ ${deletedBooks.count} Books dihapus`);

        console.log('\n✨ Database berhasil dibersihkan!');
        console.log('📝 Data yang tersisa: Users & Categories');

    } catch (error) {
        console.error('❌ Error:', error);
    } finally {
        await prisma.$disconnect();
    }
}

resetData();
