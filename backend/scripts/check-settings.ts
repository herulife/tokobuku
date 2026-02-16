import prisma from '../src/lib/prisma';

async function main() {
    const settings = await prisma.setting.findMany();
    console.log(settings);
}

main()
    .catch(e => console.error(e))
    .finally(async () => {
        await prisma.$disconnect();
    });
