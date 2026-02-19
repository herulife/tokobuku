"use strict";
var __assign = (this && this.__assign) || function () {
    __assign = Object.assign || function(t) {
        for (var s, i = 1, n = arguments.length; i < n; i++) {
            s = arguments[i];
            for (var p in s) if (Object.prototype.hasOwnProperty.call(s, p))
                t[p] = s[p];
        }
        return t;
    };
    return __assign.apply(this, arguments);
};
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
var bcrypt_1 = require("bcrypt");
var prisma = new client_1.PrismaClient();
function main() {
    return __awaiter(this, void 0, void 0, function () {
        var categories, _i, categories_1, cat, password, catParenting, catAqidah, catKeluarga, books, _a, books_1, book;
        return __generator(this, function (_b) {
            switch (_b.label) {
                case 0:
                    categories = [
                        { name: 'Parenting', slug: 'parenting' },
                        { name: 'Aqidah', slug: 'aqidah' },
                        { name: 'Fiqih', slug: 'fiqih' },
                        { name: 'Hadits', slug: 'hadits' },
                        { name: 'Psikologi', slug: 'psikologi' },
                        { name: 'Keluarga', slug: 'keluarga' },
                    ];
                    _i = 0, categories_1 = categories;
                    _b.label = 1;
                case 1:
                    if (!(_i < categories_1.length)) return [3 /*break*/, 4];
                    cat = categories_1[_i];
                    return [4 /*yield*/, prisma.category.upsert({
                            where: { slug: cat.slug },
                            update: {},
                            create: cat,
                        })];
                case 2:
                    _b.sent();
                    _b.label = 3;
                case 3:
                    _i++;
                    return [3 /*break*/, 1];
                case 4: return [4 /*yield*/, bcrypt_1.default.hash('password123', 12)];
                case 5:
                    password = _b.sent();
                    return [4 /*yield*/, prisma.user.upsert({
                            where: { email: 'admin@cintabuku.com' },
                            update: {},
                            create: {
                                email: 'admin@cintabuku.com',
                                name: 'Admin Koalisi',
                                password: password,
                                role: 'ADMIN',
                            },
                        })];
                case 6:
                    _b.sent();
                    return [4 /*yield*/, prisma.user.upsert({
                            where: { email: 'user@cintabuku.com' },
                            update: {},
                            create: {
                                email: 'user@cintabuku.com',
                                name: 'User Cinta Buku',
                                password: password,
                                role: 'USER',
                            },
                        })];
                case 7:
                    _b.sent();
                    return [4 /*yield*/, prisma.category.findUnique({ where: { slug: 'parenting' } })];
                case 8:
                    catParenting = _b.sent();
                    return [4 /*yield*/, prisma.category.findUnique({ where: { slug: 'aqidah' } })];
                case 9:
                    catAqidah = _b.sent();
                    return [4 /*yield*/, prisma.category.findUnique({ where: { slug: 'keluarga' } })];
                case 10:
                    catKeluarga = _b.sent();
                    if (!catParenting || !catAqidah || !catKeluarga)
                        return [2 /*return*/];
                    books = [
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
                    _a = 0, books_1 = books;
                    _b.label = 11;
                case 11:
                    if (!(_a < books_1.length)) return [3 /*break*/, 14];
                    book = books_1[_a];
                    return [4 /*yield*/, prisma.book.upsert({
                            where: { slug: book.slug },
                            update: __assign(__assign({}, book), { categoryId: book.categoryId }),
                            create: book,
                        })];
                case 12:
                    _b.sent();
                    _b.label = 13;
                case 13:
                    _a++;
                    return [3 /*break*/, 11];
                case 14:
                    console.log('Seeding completed with Parenting books.');
                    return [2 /*return*/];
            }
        });
    });
}
main()
    .catch(function (e) {
    console.error(e);
    process.exit(1);
})
    .finally(function () { return __awaiter(void 0, void 0, void 0, function () {
    return __generator(this, function (_a) {
        switch (_a.label) {
            case 0: return [4 /*yield*/, prisma.$disconnect()];
            case 1:
                _a.sent();
                return [2 /*return*/];
        }
    });
}); });
