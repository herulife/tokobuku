-- RedefineTables
PRAGMA defer_foreign_keys=ON;
PRAGMA foreign_keys=OFF;
CREATE TABLE "new_Book" (
    "id" TEXT NOT NULL PRIMARY KEY,
    "title" TEXT NOT NULL,
    "slug" TEXT NOT NULL,
    "author" TEXT NOT NULL,
    "publisher" TEXT,
    "isbn" TEXT,
    "description" TEXT,
    "price" INTEGER NOT NULL,
    "discountPrice" INTEGER,
    "stock" INTEGER NOT NULL DEFAULT 0,
    "weight" INTEGER NOT NULL DEFAULT 300,
    "coverImage" TEXT NOT NULL,
    "samplePdf" TEXT,
    "categoryId" TEXT NOT NULL,
    "isPreorder" BOOLEAN NOT NULL DEFAULT false,
    "preorderDate" DATETIME,
    "rating" REAL DEFAULT 0,
    "totalRating" INTEGER NOT NULL DEFAULT 0,
    "pages" INTEGER,
    "language" TEXT DEFAULT 'Indonesia',
    "publishedDate" DATETIME,
    "createdAt" DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" DATETIME NOT NULL,
    CONSTRAINT "Book_categoryId_fkey" FOREIGN KEY ("categoryId") REFERENCES "Category" ("id") ON DELETE RESTRICT ON UPDATE CASCADE
);
INSERT INTO "new_Book" ("author", "categoryId", "coverImage", "createdAt", "description", "discountPrice", "id", "isPreorder", "isbn", "language", "pages", "preorderDate", "price", "publisher", "rating", "samplePdf", "slug", "stock", "title", "totalRating", "updatedAt") SELECT "author", "categoryId", "coverImage", "createdAt", "description", "discountPrice", "id", "isPreorder", "isbn", "language", "pages", "preorderDate", "price", "publisher", "rating", "samplePdf", "slug", "stock", "title", "totalRating", "updatedAt" FROM "Book";
DROP TABLE "Book";
ALTER TABLE "new_Book" RENAME TO "Book";
CREATE UNIQUE INDEX "Book_slug_key" ON "Book"("slug");
CREATE UNIQUE INDEX "Book_isbn_key" ON "Book"("isbn");
PRAGMA foreign_keys=ON;
PRAGMA defer_foreign_keys=OFF;
