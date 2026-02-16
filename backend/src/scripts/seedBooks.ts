import { PrismaClient } from '@prisma/client';

const prisma = new PrismaClient();

async function seedBooks() {
    try {
        console.log('📚 Menambahkan 20 buku...\n');

        // Ambil semua kategori
        const categories = await prisma.category.findMany();
        const categoryMap = categories.reduce((acc, cat) => {
            acc[cat.slug] = cat.id;
            return acc;
        }, {} as Record<string, string>);

        const books = [
            // Parenting
            {
                title: 'Positive Parenting',
                slug: 'positive-parenting',
                author: 'Dr. Jane Nelson',
                publisher: 'Gramedia',
                isbn: '9786020633183',
                description: 'Panduan lengkap mengasuh anak dengan pendekatan positif dan penuh kasih sayang.',
                price: 95000,
                discountPrice: 82000,
                stock: 30,
                weight: 380,
                coverImage: 'https://images.unsplash.com/photo-1544947950-fa07a98d237f?w=400',
                categoryId: categoryMap['parenting'],
                pages: 368,
                language: 'Indonesia'
            },
            {
                title: 'Mendidik Anak Di Era Digital',
                slug: 'mendidik-anak-di-era-digital',
                author: 'Elly Risman',
                publisher: 'Bentang Pustaka',
                isbn: '9786022914372',
                description: 'Strategi mengasuh anak di tengah tantangan teknologi dan media sosial.',
                price: 88000,
                stock: 25,
                weight: 350,
                coverImage: 'https://images.unsplash.com/photo-1512820790803-83ca734da794?w=400',
                categoryId: categoryMap['parenting'],
                pages: 324,
                language: 'Indonesia'
            },
            {
                title: 'Parenting with Love and Logic',
                slug: 'parenting-with-love-and-logic',
                author: 'Foster Cline & Jim Fay',
                publisher: 'Mizan',
                isbn: '9786024018466',
                description: 'Mengajarkan tanggung jawab pada anak dengan cinta dan logika yang seimbang.',
                price: 92000,
                discountPrice: 79000,
                stock: 28,
                weight: 360,
                coverImage: 'https://images.unsplash.com/photo-1543002588-bfa74002ed7e?w=400',
                categoryId: categoryMap['parenting'],
                pages: 356,
                language: 'Indonesia'
            },

            // Aqidah
            {
                title: 'Tauhid untuk Pemula',
                slug: 'tauhid-untuk-pemula',
                author: 'Ustadz Khalid Basalamah',
                publisher: 'Pustaka Imam Syafii',
                isbn: '9786025478123',
                description: 'Penjelasan mendalam tentang konsep tauhid dalam Islam untuk pemula.',
                price: 68000,
                stock: 40,
                weight: 320,
                coverImage: 'https://images.unsplash.com/photo-1481627834876-b7833e8f5570?w=400',
                categoryId: categoryMap['aqidah'],
                pages: 288,
                language: 'Indonesia'
            },
            {
                title: 'Aqidah Ahlus Sunnah Wal Jamaah',
                slug: 'aqidah-ahlus-sunnah',
                author: 'Dr. Yazid bin Abdul Qadir Jawas',
                publisher: 'Pustaka Taimiyah',
                isbn: '9786025478130',
                description: 'Penjelasan komprehensif tentang aqidah yang benar sesuai manhaj salaf.',
                price: 75000,
                discountPrice: 65000,
                stock: 35,
                weight: 340,
                coverImage: 'https://images.unsplash.com/photo-1506880018603-83d5b814b5a6?w=400',
                categoryId: categoryMap['aqidah'],
                pages: 312,
                language: 'Indonesia'
            },
            {
                title: 'Meluruskan Aqidah',
                slug: 'meluruskan-aqidah',
                author: 'Syaikh Muhammad bin Shalih Al-Utsaimin',
                publisher: 'Darul Haq',
                isbn: '9786025478147',
                description: 'Koreksi dan pelurusan aqidah yang menyimpang dalam masyarakat.',
                price: 58000,
                stock: 45,
                weight: 280,
                coverImage: 'https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?w=400',
                categoryId: categoryMap['aqidah'],
                pages: 256,
                language: 'Indonesia'
            },

            // Fiqih
            {
                title: 'Fiqih Sunnah',
                slug: 'fiqih-sunnah',
                author: 'Sayyid Sabiq',
                publisher: 'Pena Pundi Aksara',
                isbn: '9786025478154',
                description: 'Panduan lengkap ibadah sehari-hari sesuai sunnah Rasulullah SAW.',
                price: 125000,
                discountPrice: 110000,
                stock: 30,
                weight: 520,
                coverImage: 'https://images.unsplash.com/photo-1532012197267-da84d127e765?w=400',
                categoryId: categoryMap['fiqih'],
                pages: 648,
                language: 'Indonesia'
            },
            {
                title: 'Fikih Wanita',
                slug: 'fikih-wanita',
                author: 'Ustadz Abu Malik Kamal',
                publisher: 'Pustaka Ibnu Katsir',
                isbn: '9786025478161',
                description: 'Hukum-hukum Islam yang khusus berkaitan dengan wanita.',
                price: 78000,
                stock: 38,
                weight: 360,
                coverImage: 'https://images.unsplash.com/photo-1579621970563-ebec7560ff3e?w=400',
                categoryId: categoryMap['fiqih'],
                pages: 384,
                language: 'Indonesia'
            },
            {
                title: 'Panduan Shalat Lengkap',
                slug: 'panduan-shalat-lengkap',
                author: 'Ustadz Abdul Somad',
                publisher: 'Tafaqquh',
                isbn: '9786025478178',
                description: 'Tata cara shalat yang benar dari takbiratul ihram hingga salam.',
                price: 62000,
                discountPrice: 52000,
                stock: 50,
                weight: 280,
                coverImage: 'https://images.unsplash.com/photo-1553729459-efe14ef6055d?w=400',
                categoryId: categoryMap['fiqih'],
                pages: 264,
                language: 'Indonesia'
            },

            // Hadits
            {
                title: 'Hadits Arba\'in An-Nawawi',
                slug: 'hadits-arbain-nawawi',
                author: 'Imam Nawawi',
                publisher: 'Darul Haq',
                isbn: '9786025478185',
                description: '40 hadits pilihan yang merangkum pokok-pokok ajaran Islam.',
                price: 48000,
                stock: 55,
                weight: 240,
                coverImage: 'https://images.unsplash.com/photo-1542744173-8e7e53415bb0?w=400',
                categoryId: categoryMap['hadits'],
                pages: 216,
                language: 'Indonesia'
            },
            {
                title: 'Riyadhus Shalihin',
                slug: 'riyadhus-shalihin',
                author: 'Imam Nawawi',
                publisher: 'Pustaka Azzam',
                isbn: '9786025478192',
                description: 'Kumpulan hadits pilihan tentang akhlak dan adab seorang muslim.',
                price: 98000,
                discountPrice: 85000,
                stock: 32,
                weight: 480,
                coverImage: 'https://images.unsplash.com/photo-1497633762265-9d179a990aa6?w=400',
                categoryId: categoryMap['hadits'],
                pages: 528,
                language: 'Indonesia'
            },
            {
                title: 'Shahih Bukhari Ringkas',
                slug: 'shahih-bukhari-ringkas',
                author: 'Imam Bukhari',
                publisher: 'Griya Ilmu',
                isbn: '9786025478208',
                description: 'Ringkasan hadits-hadits shahih pilihan dari kitab Shahih Bukhari.',
                price: 115000,
                stock: 28,
                weight: 520,
                coverImage: 'https://images.unsplash.com/photo-1456513080510-7bf3a84b82f8?w=400',
                categoryId: categoryMap['hadits'],
                pages: 584,
                language: 'Indonesia'
            },

            // Psikologi
            {
                title: 'Psikologi Komunikasi',
                slug: 'psikologi-komunikasi',
                author: 'Dr. Jalaluddin Rakhmat',
                publisher: 'Remaja Rosda Karya',
                isbn: '9786024246976',
                description: 'Pengantar komprehensif tentang psikologi dalam komunikasi antar manusia.',
                price: 89000,
                stock: 35,
                weight: 380,
                coverImage: 'https://images.unsplash.com/photo-1589998059171-988d887df646?w=400',
                categoryId: categoryMap['psikologi'],
                pages: 352,
                language: 'Indonesia'
            },
            {
                title: 'Psikologi Perkembangan Anak',
                slug: 'psikologi-perkembangan-anak',
                author: 'Dr. Singgih D. Gunarsa',
                publisher: 'BPK Gunung Mulia',
                isbn: '9786024018473',
                description: 'Tahapan perkembangan psikologis anak dari bayi hingga remaja.',
                price: 95000,
                discountPrice: 82000,
                stock: 30,
                weight: 400,
                coverImage: 'https://images.unsplash.com/photo-1584467735815-f778f274e296?w=400',
                categoryId: categoryMap['psikologi'],
                pages: 416,
                language: 'Indonesia'
            },
            {
                title: 'Emotional Intelligence',
                slug: 'emotional-intelligence',
                author: 'Daniel Goleman',
                publisher: 'Gramedia',
                isbn: '9786020822396',
                description: 'Mengapa EQ lebih penting daripada IQ dalam menentukan kesuksesan hidup.',
                price: 105000,
                stock: 26,
                weight: 420,
                coverImage: 'https://images.unsplash.com/photo-1580519542036-c47de6196ba5?w=400',
                categoryId: categoryMap['psikologi'],
                pages: 448,
                language: 'Indonesia'
            },

            // Keluarga
            {
                title: 'Membangun Keluarga Sakinah',
                slug: 'membangun-keluarga-sakinah',
                author: 'Ustadz Adi Hidayat',
                publisher: 'Pro-U Media',
                isbn: '9786025478215',
                description: 'Panduan membangun rumah tangga yang harmonis menurut syariat Islam.',
                price: 72000,
                discountPrice: 62000,
                stock: 42,
                weight: 320,
                coverImage: 'https://images.unsplash.com/photo-1495640388908-05fa85288e61?w=400',
                categoryId: categoryMap['keluarga'],
                pages: 296,
                language: 'Indonesia'
            },
            {
                title: 'The 5 Love Languages',
                slug: 'the-5-love-languages',
                author: 'Gary Chapman',
                publisher: 'Gramedia',
                isbn: '9786020822402',
                description: 'Rahasia cinta yang tahan lama dengan memahami bahasa cinta pasangan.',
                price: 88000,
                stock: 36,
                weight: 340,
                coverImage: 'https://images.unsplash.com/photo-1618519764620-7403abdbdfe9?w=400',
                categoryId: categoryMap['keluarga'],
                pages: 328,
                language: 'Indonesia'
            },

            // Matematika
            {
                title: 'Matematika Asyik untuk SD',
                slug: 'matematika-asyik-untuk-sd',
                author: 'Tim Guru Indonesia',
                publisher: 'Erlangga',
                isbn: '9786024018480',
                description: 'Belajar matematika yang menyenangkan dengan metode visual dan interaktif.',
                price: 65000,
                stock: 48,
                weight: 340,
                coverImage: 'https://images.unsplash.com/photo-1612036782180-6f0b6cd846fe?w=400',
                categoryId: categoryMap['matematika'],
                pages: 264,
                language: 'Indonesia'
            },
            {
                title: 'Jago Matematika SMP',
                slug: 'jago-matematika-smp',
                author: 'Prof. Ridwan Hasan',
                publisher: 'Yrama Widya',
                isbn: '9786024018497',
                description: 'Kumpulan rumus dan soal-soal matematika SMP yang lengkap dan mudah dipahami.',
                price: 78000,
                discountPrice: 68000,
                stock: 40,
                weight: 380,
                coverImage: 'https://images.unsplash.com/photo-1621351183012-e2f9972dd9bf?w=400',
                categoryId: categoryMap['matematika'],
                pages: 384,
                language: 'Indonesia'
            }
        ];

        let created = 0;
        for (const book of books) {
            await prisma.book.create({ data: book });
            created++;
            console.log(`✅ ${created}. ${book.title} - ${book.author}`);
        }

        console.log(`\n🎉 Berhasil menambahkan ${created} buku!`);

    } catch (error) {
        console.error('❌ Error:', error);
    } finally {
        await prisma.$disconnect();
    }
}

seedBooks();
