
import { PrismaClient } from '@prisma/client';

const prisma = new PrismaClient();

async function main() {
    const count = await prisma.book.count();
    console.log(`Total books in database: ${count}`);

    if (count > 0) {
        const firstBook = await prisma.book.findFirst();
        console.log('Sample book:', firstBook?.title);
    }
}

main()
    .catch((e) => {
        console.error(e);
        process.exit(1);
    })
    .finally(async () => {
        await prisma.$disconnect();
    });
