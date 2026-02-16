import { PrismaClient } from '@prisma/client';
import bcrypt from 'bcrypt';

const prisma = new PrismaClient();

async function main() {
    // 1. Create Categories (Parenting Focus)
    const categories = [
        { name: 'Parenting', slug: 'parenting' },
        { name: 'Aqidah', slug: 'aqidah' },
        { name: 'Fiqih', slug: 'fiqih' },
        { name: 'Hadits', slug: 'hadits' },
        { name: 'Psikologi', slug: 'psikologi' },
        { name: 'Keluarga', slug: 'keluarga' },
    ];

    for (const cat of categories) {
        await prisma.category.upsert({
            where: { slug: cat.slug },
            update: {},
            create: cat,
        });
    }

    // 2. Create Admin & User
    const password = await bcrypt.hash('password123', 12);
    await prisma.user.upsert({
        where: { email: 'admin@cintabuku.com' },
        update: {},
        create: {
            email: 'admin@cintabuku.com',
            name: 'Admin Koalisi',
            password,
            role: 'ADMIN',
        },
    });

    await prisma.user.upsert({
        where: { email: 'user@cintabuku.com' },
        update: {},
        create: {
            email: 'user@cintabuku.com',
            name: 'User Cinta Buku',
            password,
            role: 'USER',
        },
    });

    // 3. Get Category IDs
    const catParenting = await prisma.category.findUnique({ where: { slug: 'parenting' } });
    const catAqidah = await prisma.category.findUnique({ where: { slug: 'aqidah' } });
    const catKeluarga = await prisma.category.findUnique({ where: { slug: 'keluarga' } });

    if (!catParenting || !catAqidah || !catKeluarga) return;

    // 4. Create Books (Parenting Collcetion)
    const books = [
        {
            title: 'Mendidik Anak Laki-Laki',
            slug: 'mendidik-anak-laki-laki',
            author: 'dr. Aisyah Dahlan',
            price: 95000,
            stock: 50,
            coverImage: 'https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?q=80&w=800&auto=format&fit=crop', // Placeholder
            categoryId: catParenting.id,
            description: 'Memahami karakter dan psikologi anak laki-laki berbasis brain-based parenting.',
        },
        {
            title: 'Mendidik Anak Perempuan',
            slug: 'mendidik-anak-perempuan',
            author: 'dr. Aisyah Dahlan',
            price: 95000,
            stock: 45,
            coverImage: 'https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?q=80&w=800&auto=format&fit=crop',
            categoryId: catParenting.id,
            description: 'Seni mendidik anak perempuan agar menjadi sosok shalihah namun tetap tangguh.',
        },
        {
            title: 'Kakak Beradik',
            slug: 'kakak-beradik',
            author: 'Elly Risman',
            price: 85000,
            stock: 30,
            coverImage: 'https://images.unsplash.com/photo-1603525528854-ce291c3d1836?q=80&w=800&auto=format&fit=crop',
            categoryId: catKeluarga.id,
            description: 'Mengelola konflik dan membangun bonding antar saudara kandung.',
        },
        {
            title: 'Mencetak Generasi Rabbani',
            slug: 'mencetak-generasi-rabbani',
            author: 'Salim A. Fillah',
            price: 110000,
            stock: 60,
            coverImage: 'https://images.unsplash.com/photo-1512820790803-83ca734da794?q=80&w=800&auto=format&fit=crop',
            categoryId: catKeluarga.id,
            description: 'Visi misi keluarga muslim dalam mendidik anak di akhir zaman.',
        },
        {
            title: 'Parenting Rasulullah',
            slug: 'parenting-rasulullah',
            author: 'Syaikh Jamal Abdurrahman',
            price: 135000,
            stock: 25,
            coverImage: 'https://images.unsplash.com/photo-1589829085413-56de8ae18c73?q=80&w=800&auto=format&fit=crop',
            categoryId: catParenting.id,
            description: 'Meneladani metode pendidikan anak yang diterapkan oleh Nabi Muhammad SAW.',
        },
        {
            title: 'Keluarga Sakinah',
            slug: 'keluarga-sakinah',
            author: 'Yazid bin Abdul Qadir Jawas',
            price: 100000,
            stock: 40,
            coverImage: 'https://images.unsplash.com/photo-1606782516422-995a0a399120?q=80&w=800&auto=format&fit=crop',
            categoryId: catKeluarga.id,
            description: 'Panduan lengkap membangun rumah tangga bahagia sesuai sunnah.',
        },
    ];

    for (const book of books) {
        await prisma.book.upsert({
            where: { slug: book.slug },
            update: {
                ...book,
                categoryId: book.categoryId, // Ensure category is updated if needed
            },
            create: book,
        });
    }

    console.log('Seeding completed with Parenting books.');
}

main()
    .catch((e) => {
        console.error(e);
        process.exit(1);
    })
    .finally(async () => {
        await prisma.$disconnect();
    });
