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
var API_URL = 'http://localhost:5000/api/v1';
function test() {
    return __awaiter(this, void 0, void 0, function () {
        var email, regRes, regData, token, bookRes, bookData, bookId, addCartRes, addCartData, getCartRes, getCartData, wishRes, wishData, getWishRes, getWishData, error_1;
        var _a;
        return __generator(this, function (_b) {
            switch (_b.label) {
                case 0:
                    _b.trys.push([0, 13, , 14]);
                    email = "testcart_".concat(Date.now(), "@example.com");
                    console.log("Registering user: ".concat(email));
                    return [4 /*yield*/, fetch("".concat(API_URL, "/auth/register"), {
                            method: 'POST',
                            headers: { 'Content-Type': 'application/json' },
                            body: JSON.stringify({
                                email: email,
                                password: 'password123',
                                confirmPassword: 'password123',
                                name: 'Cart Tester'
                            })
                        })];
                case 1:
                    regRes = _b.sent();
                    return [4 /*yield*/, regRes.json()];
                case 2:
                    regData = _b.sent();
                    if (!regRes.ok)
                        throw new Error("Register failed: ".concat(JSON.stringify(regData)));
                    token = regData.token;
                    console.log('User registered. Token:', token ? 'OK' : 'MISSING');
                    // 2. Get Books
                    console.log('Fetching books...');
                    return [4 /*yield*/, fetch("".concat(API_URL, "/books?limit=1"))];
                case 3:
                    bookRes = _b.sent();
                    return [4 /*yield*/, bookRes.json()];
                case 4:
                    bookData = _b.sent();
                    if (!bookRes.ok)
                        throw new Error("Get books failed: ".concat(JSON.stringify(bookData)));
                    bookId = (_a = bookData.data.books[0]) === null || _a === void 0 ? void 0 : _a.id;
                    if (!bookId)
                        throw new Error('No books found to test with');
                    console.log("Using Book ID: ".concat(bookId));
                    // 3. Add to Cart
                    console.log('Adding to cart...');
                    return [4 /*yield*/, fetch("".concat(API_URL, "/cart/items"), {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json',
                                'Authorization': "Bearer ".concat(token)
                            },
                            body: JSON.stringify({ bookId: bookId, quantity: 1 })
                        })];
                case 5:
                    addCartRes = _b.sent();
                    return [4 /*yield*/, addCartRes.json()];
                case 6:
                    addCartData = _b.sent();
                    if (!addCartRes.ok)
                        throw new Error("Add to cart failed: ".concat(JSON.stringify(addCartData)));
                    console.log('Added to cart. Items:', addCartData.data.cart.items.length);
                    // 4. Get Cart
                    console.log('Fetching cart...');
                    return [4 /*yield*/, fetch("".concat(API_URL, "/cart"), {
                            headers: { 'Authorization': "Bearer ".concat(token) }
                        })];
                case 7:
                    getCartRes = _b.sent();
                    return [4 /*yield*/, getCartRes.json()];
                case 8:
                    getCartData = _b.sent();
                    if (!getCartRes.ok)
                        throw new Error("Get cart failed: ".concat(JSON.stringify(getCartData)));
                    console.log('Cart fetched. Items:', getCartData.data.cart.items.length);
                    // 5. Add to Wishlist
                    console.log('Adding to wishlist...');
                    return [4 /*yield*/, fetch("".concat(API_URL, "/wishlist"), {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json',
                                'Authorization': "Bearer ".concat(token)
                            },
                            body: JSON.stringify({ bookId: bookId })
                        })];
                case 9:
                    wishRes = _b.sent();
                    return [4 /*yield*/, wishRes.json()];
                case 10:
                    wishData = _b.sent();
                    if (!wishRes.ok)
                        throw new Error("Add to wishlist failed: ".concat(JSON.stringify(wishData)));
                    console.log('Added to wishlist.');
                    // 6. Get Wishlist
                    console.log('Fetching wishlist...');
                    return [4 /*yield*/, fetch("".concat(API_URL, "/wishlist"), {
                            headers: { 'Authorization': "Bearer ".concat(token) }
                        })];
                case 11:
                    getWishRes = _b.sent();
                    return [4 /*yield*/, getWishRes.json()];
                case 12:
                    getWishData = _b.sent();
                    if (!getWishRes.ok)
                        throw new Error("Get wishlist failed: ".concat(JSON.stringify(getWishData)));
                    console.log('Wishlist fetched. Items:', getWishData.data.wishlist.length);
                    console.log('ALL TESTS PASSED');
                    return [3 /*break*/, 14];
                case 13:
                    error_1 = _b.sent();
                    console.error('TEST FAILED:', error_1.message);
                    process.exit(1);
                    return [3 /*break*/, 14];
                case 14: return [2 /*return*/];
            }
        });
    });
}
test();
