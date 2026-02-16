"use strict";
var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
var __generator = (this && this.__generator) || function (thisArg, body) {
    var _ = { label: 0, sent: function() { if (t[0] & 1) throw t[1]; return t[1]; }, trys: [], ops: [] }, f, y, t, g = Object.create((typeof Iterator === "function" ? Iterator : Object).prototype);
    return g.next = verb(0), g["throw"] = verb(1), g["return"] = verb(2), typeof Symbol === "function" && (g[Symbol.iterator] = function() { return this; }), g;
    function verb(n) { return function (v) { return step([n, v]); }; }
    function step(op) {
        if (f) throw new TypeError("Generator is already executing.");
        while (g && (g = 0, op[0] && (_ = 0)), _) try {
            if (f = 1, y && (t = op[0] & 2 ? y["return"] : op[0] ? y["throw"] || ((t = y["return"]) && t.call(y), 0) : y.next) && !(t = t.call(y, op[1])).done) return t;
            if (y = 0, t) op = [op[0] & 2, t.value];
            switch (op[0]) {
                case 0: case 1: t = op; break;
                case 4: _.label++; return { value: op[1], done: false };
                case 5: _.label++; y = op[1]; op = [0]; continue;
                case 7: op = _.ops.pop(); _.trys.pop(); continue;
                default:
                    if (!(t = _.trys, t = t.length > 0 && t[t.length - 1]) && (op[0] === 6 || op[0] === 2)) { _ = 0; continue; }
                    if (op[0] === 3 && (!t || (op[1] > t[0] && op[1] < t[3]))) { _.label = op[1]; break; }
                    if (op[0] === 6 && _.label < t[1]) { _.label = t[1]; t = op; break; }
                    if (t && _.label < t[2]) { _.label = t[2]; _.ops.push(op); break; }
                    if (t[2]) _.ops.pop();
                    _.trys.pop(); continue;
            }
            op = body.call(thisArg, _);
        } catch (e) { op = [6, e]; y = 0; } finally { f = t = 0; }
        if (op[0] & 5) throw op[1]; return { value: op[0] ? op[1] : void 0, done: true };
    }
};
Object.defineProperty(exports, "__esModule", { value: true });
var client_1 = require("@prisma/client");
var prisma = new client_1.PrismaClient();
function seedBooks() {
    return __awaiter(this, void 0, void 0, function () {
        var categories, categoryMap, books, created, _i, books_1, book, error_1;
        return __generator(this, function (_a) {
            switch (_a.label) {
                case 0:
                    _a.trys.push([0, 6, 7, 9]);
                    console.log('📚 Menambahkan 20 buku...\n');
                    return [4 /*yield*/, prisma.category.findMany()];
                case 1:
                    categories = _a.sent();
                    categoryMap = categories.reduce(function (acc, cat) {
                        acc[cat.slug] = cat.id;
                        return acc;
                    }, {});
                    books = [
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
                    created = 0;
                    _i = 0, books_1 = books;
                    _a.label = 2;
                case 2:
                    if (!(_i < books_1.length)) return [3 /*break*/, 5];
                    book = books_1[_i];
                    return [4 /*yield*/, prisma.book.create({ data: book })];
                case 3:
                    _a.sent();
                    created++;
                    console.log("\u2705 ".concat(created, ". ").concat(book.title, " - ").concat(book.author));
                    _a.label = 4;
                case 4:
                    _i++;
                    return [3 /*break*/, 2];
                case 5:
                    console.log("\n\uD83C\uDF89 Berhasil menambahkan ".concat(created, " buku!"));
                    return [3 /*break*/, 9];
                case 6:
                    error_1 = _a.sent();
                    console.error('❌ Error:', error_1);
                    return [3 /*break*/, 9];
                case 7: return [4 /*yield*/, prisma.$disconnect()];
                case 8:
                    _a.sent();
                    return [7 /*endfinally*/];
                case 9: return [2 /*return*/];
            }
        });
    });
}
seedBooks();
