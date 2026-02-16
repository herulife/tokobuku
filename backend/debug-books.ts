
import { PrismaClient } from '@prisma/client';

const prisma = new PrismaClient();

async function main() {
    const books = await prisma.book.findMany({
        select: { title: true, coverImage: true, id: true },
        take: 5,
        orderBy: { createdAt: 'desc' }
    });
    console.log('Recent books:', JSON.stringify(books, null, 2));
}

main()
    .catch(e => console.error(e))
    .finally(async () => await prisma.$disconnect());
