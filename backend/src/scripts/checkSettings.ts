
import { PrismaClient } from '@prisma/client';
const prisma = new PrismaClient();

async function main() {
    try {
        const settings = await prisma.setting.findMany();
        console.log('--- SETTINGS START ---');
        console.log(JSON.stringify(settings, null, 2));
        console.log('--- SETTINGS END ---');
    } catch (e) {
        console.error(e);
    } finally {
        await prisma.$disconnect();
    }
}

main();
