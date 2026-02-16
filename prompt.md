# 🚀 Prompt AI Agent: Bangun Toko Buku **"Koalisi Cinta Buku"** – Next.js + Express + PostgreSQL

Anda adalah AI *full‑stack engineer*. Tugas Anda adalah membangun aplikasi web **Toko Buku "Koalisi Cinta Buku"** (domain **cintabuku.com**) yang **siap production**, dengan spesifikasi sebagai berikut.

---

## 📌 1. INSTRUKSI UMUM

- **Teknologi Wajib**  
  - Frontend: **Next.js 15 (App Router)** + Tailwind CSS + TypeScript  
  - Backend: **Express.js** (ES6 modules) + **Prisma ORM**  
  - Database: **PostgreSQL**  
  - State Management: **Zustand** (cart & auth)  
  - Autentikasi: JWT (httpOnly cookie) + bcrypt  

- **Desain UI**  
  Gunakan persis **template UI biru premium** yang sudah dilampirkan (navbar glassmorphism, hero gradient, card dengan hover effect, badge, tombol gradient, footer, dll).  
  Warna dominan: **biru & indigo** (`blue-600`, `indigo-600`, `blue-50`, dll).  
  Selalu tampilkan nama **"Koalisi Cinta Buku"**.

- **Fitur**  
  Hanya **fitur inti** (katalog, pencarian, filter, keranjang, wishlist, akun, pre‑order, order).  
  **TIDAK ADA** fitur tambahan seperti AR, audio snippet, subscription box, rental, komunitas, event, donasi, buku bekas, bundling, dashboard penerbit, dll.

- **Target Akhir**  
  Aplikasi **fungsional penuh**, terintegrasi database, siap *deploy*, dengan kode rapi, TypeScript, dan dokumentasi singkat.

---

## 🧱 2. ARSITEKTUR PROYEK

gunakan layout di file template

Buat struktur berikut (monorepo sederhana):

```
cintabuku/
├── frontend/               # Next.js app
│   ├── app/                # App Router
│   ├── components/         # Komponen reusable
│   ├── lib/                # Utilities, API client
│   ├── store/              # Zustand stores
│   ├── public/             # Aset statis
│   └── ...
├── backend/                # Express.js app
│   ├── prisma/             # Schema & migrations
│   ├── src/
│   │   ├── controllers/
│   │   ├── routes/
│   │   ├── middlewares/
│   │   ├── utils/
│   │   └── index.js
│   └── ...
├── docker-compose.yml      # Opsional, untuk PostgreSQL lokal
└── README.md
```

---

## 🗄️ 3. DATABASE SCHEMA (PRISMA)

Buat `prisma/schema.prisma` dengan model berikut.  
Gunakan **PostgreSQL**, generator `prisma-client-js`.

```prisma
model User {
  id             String    @id @default(cuid())
  email          String    @unique
  password       String
  name           String
  avatar         String?   @default("https://i.pravatar.cc/150?u=default")
  role           Role      @default(USER)
  wishlists      Wishlist[]
  carts          Cart[]
  orders         Order[]
  createdAt      DateTime  @default(now())
  updatedAt      DateTime  @updatedAt
}

enum Role {
  USER
  ADMIN
}

model Book {
  id            String       @id @default(cuid())
  title         String
  slug          String       @unique // dari title
  author        String
  publisher     String?
  isbn          String?      @unique
  description   String?      @db.Text
  price         Int
  discountPrice Int?
  stock         Int          @default(0)
  coverImage    String
  samplePdf     String?
  categoryId    String
  category      Category     @relation(fields: [categoryId], references: [id])
  isPreorder    Boolean      @default(false)
  preorderDate  DateTime?
  rating        Float?       @default(0)
  totalRating   Int          @default(0)
  createdAt     DateTime     @default(now())
  updatedAt     DateTime     @updatedAt
  wishlistItems Wishlist[]
  cartItems     CartItem[]
  orderItems    OrderItem[]
}

model Category {
  id     String   @id @default(cuid())
  name   String   @unique
  slug   String   @unique
  books  Book[]
}

model Wishlist {
  id        String   @id @default(cuid())
  userId    String
  user      User     @relation(fields: [userId], references: [id], onDelete: Cascade)
  bookId    String
  book      Book     @relation(fields: [bookId], references: [id], onDelete: Cascade)
  createdAt DateTime @default(now())

  @@unique([userId, bookId])
}

model Cart {
  id        String     @id @default(cuid())
  userId    String     @unique
  user      User       @relation(fields: [userId], references: [id], onDelete: Cascade)
  items     CartItem[]
  updatedAt DateTime   @updatedAt
}

model CartItem {
  id        String   @id @default(cuid())
  cartId    String
  cart      Cart     @relation(fields: [cartId], references: [id], onDelete: Cascade)
  bookId    String
  book      Book     @relation(fields: [bookId], references: [id], onDelete: Cascade)
  quantity  Int      @default(1)
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt

  @@unique([cartId, bookId])
}

model Order {
  id              String        @id @default(cuid())
  invoiceNumber   String        @unique // format: INV/YYYYMMDD/xxxx
  userId          String
  user            User          @relation(fields: [userId], references: [id])
  items           OrderItem[]
  total           Int
  status          OrderStatus   @default(PENDING)
  paymentMethod   String?
  paymentProof    String?
  shippingAddress String        @db.Text
  courier         String?
  resi            String?
  paidAt          DateTime?
  shippedAt       DateTime?
  deliveredAt     DateTime?
  createdAt       DateTime      @default(now())
  updatedAt       DateTime      @updatedAt
}

enum OrderStatus {
  PENDING
  PAID
  PROCESSING
  SHIPPED
  DELIVERED
  CANCELLED
}

model OrderItem {
  id        String   @id @default(cuid())
  orderId   String
  order     Order    @relation(fields: [orderId], references: [id], onDelete: Cascade)
  bookId    String
  book      Book     @relation(fields: [bookId], references: [id])
  quantity  Int
  price     Int      // harga saat dibeli (sudah termasuk diskon)
  createdAt DateTime @default(now())
}
```

**Seeder wajib**:  
- Kategori: `Fiksi`, `Nonfiksi`, `Anak`, `Self Improvement`, `Bisnis`, `Komik`.  
- Minimal 12 contoh buku dengan berbagai variasi (best seller, diskon, pre‑order, baru).

---

## 🔧 4. BACKEND API ENDPOINTS

Prefix: `/api/v1`.  
Semua response JSON format `{ success: boolean, data?: any, message?: string }`.  
Gunakan **httpOnly cookie** untuk JWT.

### 🧑‍💻 **Auth**
| Method | Endpoint             | Description                          |
|--------|----------------------|--------------------------------------|
| POST   | `/auth/register`     | register, set cookie                |
| POST   | `/auth/login`        | login, set cookie                  |
| POST   | `/auth/logout`       | hapus cookie                       |
| GET    | `/auth/me`           | ambil data user saat ini           |

### 📚 **Books**
| Method | Endpoint                    | Description                                      |
|--------|-----------------------------|--------------------------------------------------|
| GET    | `/books`                    | list buku (query: page, limit, search, category, minPrice, maxPrice, inStock, sort) |
| GET    | `/books/:id`                | detail buku by id                               |
| GET    | `/books/slug/:slug`         | detail buku by slug                             |
| POST   | `/books`                    | (admin) tambah buku                             |
| PUT    | `/books/:id`                | (admin) edit buku                               |
| DELETE | `/books/:id`                | (admin) hapus buku                             |

### 🛒 **Cart**
| Method | Endpoint               | Description                                  |
|--------|------------------------|----------------------------------------------|
| GET    | `/cart`                | ambil cart user saat ini                    |
| POST   | `/cart/items`          | tambah item (bookId, quantity)             |
| PUT    | `/cart/items/:bookId`  | update quantity                            |
| DELETE | `/cart/items/:bookId`  | hapus item                                 |
| DELETE | `/cart`                | kosongkan cart                             |

### ❤️ **Wishlist**
| Method | Endpoint                | Description            |
|--------|-------------------------|------------------------|
| GET    | `/wishlist`             | ambil wishlist user   |
| POST   | `/wishlist`             | { bookId }            |
| DELETE | `/wishlist/:bookId`     | hapus dari wishlist   |

### 📦 **Orders**
| Method | Endpoint                         | Description                      |
|--------|----------------------------------|----------------------------------|
| POST   | `/orders`                       | checkout (address, paymentMethod) |
| GET    | `/orders`                       | riwayat order user              |
| GET    | `/orders/:id`                  | detail order                    |
| PUT    | `/orders/:id/cancel`           | batalkan order (status PENDING) |
| GET    | `/admin/orders`                | (admin) semua order             |
| PUT    | `/admin/orders/:id/status`     | (admin) update status, resi     |

### 🏷️ **Categories**
| Method | Endpoint        | Description        |
|--------|-----------------|--------------------|
| GET    | `/categories`   | daftar kategori   |

### 👤 **User Profile**
| Method | Endpoint        | Description          |
|--------|-----------------|----------------------|
| GET    | `/user/profile` | profil user         |
| PUT    | `/user/profile` | update nama, avatar |

---

## 🎨 5. FRONTEND (NEXT.JS)

### 5.1 Halaman yang harus dibuat

| Route                     | Deskripsi                                                                 |
|---------------------------|---------------------------------------------------------------------------|
| `/`                       | Home: hero, daftar buku terlaris / rekomendasi, kategori                 |
| `/books`                  | Katalog: sidebar filter, grid buku, pagination, sortir                   |
| `/books/[id]`             | Detail buku: cover, info, harga, stok, tombol cart/wishlist, sample PDF  |
| `/cart`                   | Keranjang: list item, edit quantity, subtotal, tombol checkout           |
| `/wishlist`               | Wishlist: grid buku yang disukai, tombol pindah ke cart                  |
| `/checkout`               | Checkout: form alamat, pilihan pembayaran (dummy), ringkasan pesanan     |
| `/profile`                | Profil: data user, tab "Pesanan Saya", "Wishlist", "Rak Saya" (statistik)|
| `/auth/login`             | Login form                                                               |
| `/auth/register`          | Register form                                                            |
| `/admin`                  | (Role ADMIN) Dashboard admin: kelola buku, stok, pesanan                 |
| `/admin/books`            | (ADMIN) CRUD buku                                                        |
| `/admin/orders`           | (ADMIN) Daftar order + update status                                     |

### 5.2 Komponen Reusable (wajib)

- `Navbar` – glassmorphism, logo + domain, search bar, ikon wishlist/cart/user, kategori.
- `Footer` – premium, biru.
- `BookCard` – persis desain UI: cover, badge, tombol wishlist (hover biru), info buku, harga, tombol "Tambah".
- `RatingStars` – komponen bintang.
- `FilterSidebar` – kategori, harga, rating, stok.
- `Pagination` – navigasi halaman.
- `LoadingSpinner` – indikator loading.
- `ErrorBoundary` – fallback UI.

### 5.3 State Management (Zustand)

**Auth Store**  
- `user`, `isAuthenticated`, `login()`, `logout()`, `fetchUser()`.

**Cart Store**  
- `items`, `totalItems`, `totalPrice`, `addItem()`, `removeItem()`, `updateQuantity()`, `clearCart()`.  
- **Sinkronisasi**: setelah login, tarik cart dari API dan merge dengan localStorage.

**Wishlist Store** (opsional, bisa pakai React Query) – lebih baik polling via API.

### 5.4 API Client

Buat `lib/api-client.ts`:

```ts
const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:5000/api/v1';

async function apiClient(endpoint: string, options: RequestInit = {}) {
  const res = await fetch(`${API_BASE}${endpoint}`, {
    credentials: 'include',
    headers: { 'Content-Type': 'application/json', ...options.headers },
    ...options,
  });
  const data = await res.json();
  if (!res.ok) throw new Error(data.message || 'Something went wrong');
  return data;
}
```

Gunakan custom hooks: `useBooks`, `useBook`, `useCart`, `useWishlist`, `useAuth`, `useOrders`.

### 5.5 Validasi Form

- **React Hook Form** + **Zod** untuk login, register, checkout, admin form.

### 5.6 SEO & Metadata

Setiap halaman harus memiliki `generateMetadata` dengan title & description dinamis.

---

## 🔐 6. KEAMANAN & PRODUCTION

### Backend
- **Helmet**, **cors** (origin = `CLIENT_URL`), **express-rate-limit**.
- **express-validator** untuk validasi input.
- **bcrypt** (salt rounds = 12) untuk hash password.
- **JWT** disimpan di **httpOnly cookie**, `secure: true` di production, `sameSite: 'lax'`.
- **Prisma** – gunakan connection pooling untuk production (contoh: `?pgbouncer=true&connection_limit=1`).
- Environment variables di `.env`:

```env
PORT=5000
DATABASE_URL=postgresql://...
JWT_SECRET=your_jwt_secret
CLIENT_URL=http://localhost:3000
NODE_ENV=development
```

### Frontend
- **Next.js standalone output** (`output: 'standalone'` di `next.config.js`).
- Optimasi gambar dengan `next/image`.
- **Metadata** untuk SEO.
- **Error boundary** di root layout.

---

## 📦 7. DEPLOYMENT READY

Buat file berikut:

**frontend/.env.local.example**  
```
NEXT_PUBLIC_API_URL=http://localhost:5000/api/v1
```

**backend/.env.example**  
```
PORT=5000
DATABASE_URL=
JWT_SECRET=
CLIENT_URL=http://localhost:3000
NODE_ENV=development
```

**docker-compose.yml** (opsional, untuk PostgreSQL lokal)  
```yaml
version: '3.8'
services:
  db:
    image: postgres:15-alpine
    container_name: cintabuku_db
    restart: always
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: cintabuku
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
volumes:
  postgres_data:
```

**package.json** scripts (backend)  
```json
"scripts": {
  "dev": "nodemon src/index.js",
  "build": "prisma generate",
  "start": "node src/index.js",
  "migrate": "prisma migrate deploy",
  "seed": "node prisma/seed.js"
}
```

**README.md**  
Berisi:
- Deskripsi proyek
- Prasyarat (Node.js, PostgreSQL)
- Cara instalasi & konfigurasi environment
- Migrasi & seeding
- Menjalankan development
- Build & production

---

## 📋 8. PRIORITAS IMPLEMENTASI

1. **Setup proyek** – inisialisasi Next.js & Express, Prisma, koneksi DB.  
2. **Model & Seeder** – buat schema, migrasi, seed categories & buku contoh.  
3. **Backend Auth** – register, login, logout, me.  
4. **Frontend Auth** – halaman login/register, Zustand auth store.  
5. **Backend Buku** – endpoint list, detail, filter, sort, pagination.  
6. **Frontend Katalog** – halaman `/books`, `BookCard`, filter sidebar, pagination.  
7. **Frontend Detail Buku** – halaman `/books/[id]`.  
8. **Backend Cart & Wishlist** – semua endpoint.  
9. **Frontend Cart & Wishlist** – halaman, store, sinkronisasi.  
10. **Backend Order** – checkout, riwayat, admin order.  
11. **Frontend Checkout & Profile** – halaman checkout, pesanan saya.  
12. **Admin Panel** – CRUD buku, update status order.  
13. **Polish** – loading state, error handling, SEO, responsive.  
14. **Dokumentasi & Production check**.

---

## 🚨 9. CATATAN PENTING

- **Desain WAJIB persis** template UI biru yang sudah dilampirkan. Gunakan komponen yang sama: glass navbar, hero gradient, card dengan hover, badge, tombol gradient, footer premium.  
- **Tidak ada fitur tambahan** – fokus 100% pada fitur inti di atas.  
- **Gunakan TypeScript** di seluruh kode (strict mode).  
- **Komentari** bagian kritis.  
- **Gunakan Font Awesome 6** (CDN atau paket npm `@fortawesome/react-fontawesome`).  
- **App Router** – jangan gunakan Pages Router.  
- **Pastikan mobile responsive**.  
- **Jangan gunakan placeholder / fake data** – semua harus terintegrasi dengan database.

---

## ✅ HASIL AKHIR YANG DIHARAPKAN

Aplikasi toko buku **"Koalisi Cinta Buku"** yang:
- ✅ Fungsional penuh sesuai fitur inti.
- ✅ Desain premium, responsif, identik dengan template biru.
- ✅ Kode TypeScript rapi, terstruktur, siap production.
- ✅ Dokumentasi jelas untuk deployment.

**MULAI KERJAKAN!** 🚀💙📚