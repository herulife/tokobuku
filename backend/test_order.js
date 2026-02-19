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
        var email, regRes, regData, token, bookRes, bookData, bookId, orderRes, orderData, orderId, myOrdersRes, myOrdersData, detailRes, error_1;
        var _a;
        return __generator(this, function (_b) {
            switch (_b.label) {
                case 0:
                    _b.trys.push([0, 11, , 12]);
                    email = "testorder_".concat(Date.now(), "@example.com");
                    console.log("Registering user: ".concat(email));
                    return [4 /*yield*/, fetch("".concat(API_URL, "/auth/register"), {
                            method: 'POST',
                            headers: { 'Content-Type': 'application/json' },
                            body: JSON.stringify({
                                email: email,
                                password: 'password123',
                                confirmPassword: 'password123',
                                name: 'Order Tester'
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
                    console.log('User registered.');
                    return [4 /*yield*/, fetch("".concat(API_URL, "/books?limit=1"))];
                case 3:
                    bookRes = _b.sent();
                    return [4 /*yield*/, bookRes.json()];
                case 4:
                    bookData = _b.sent();
                    bookId = (_a = bookData.data.books[0]) === null || _a === void 0 ? void 0 : _a.id;
                    if (!bookId)
                        throw new Error('No books found');
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
                    _b.sent();
                    // 4. Create Order (Checkout)
                    console.log('Creating Order...');
                    return [4 /*yield*/, fetch("".concat(API_URL, "/orders"), {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json',
                                'Authorization': "Bearer ".concat(token)
                            },
                            body: JSON.stringify({
                                shippingAddress: 'Jalan Kenangan No. 123',
                                paymentMethod: 'TRANSFER_BCA',
                                courier: 'JNE'
                            })
                        })];
                case 6:
                    orderRes = _b.sent();
                    return [4 /*yield*/, orderRes.json()];
                case 7:
                    orderData = _b.sent();
                    if (!orderRes.ok)
                        throw new Error("Create Order failed: ".concat(JSON.stringify(orderData)));
                    orderId = orderData.data.order.id;
                    console.log("Order created. ID: ".concat(orderId, ", Invoice: ").concat(orderData.data.order.invoiceNumber));
                    // 5. Get My Orders
                    console.log('Fetching my orders...');
                    return [4 /*yield*/, fetch("".concat(API_URL, "/orders"), {
                            headers: { 'Authorization': "Bearer ".concat(token) }
                        })];
                case 8:
                    myOrdersRes = _b.sent();
                    return [4 /*yield*/, myOrdersRes.json()];
                case 9:
                    myOrdersData = _b.sent();
                    if (myOrdersData.data.orders.length === 0)
                        throw new Error('My orders is empty');
                    console.log("My Orders count: ".concat(myOrdersData.data.orders.length));
                    // 6. Get Order Detail
                    console.log('Fetching order detail...');
                    return [4 /*yield*/, fetch("".concat(API_URL, "/orders/").concat(orderId), {
                            headers: { 'Authorization': "Bearer ".concat(token) }
                        })];
                case 10:
                    detailRes = _b.sent();
                    if (!detailRes.ok)
                        throw new Error('Get order detail failed');
                    console.log('Order detail fetched.');
                    // 7. Test Admin - Login as Admin (Need to seed admin or upgrade user)
                    // For now, we'll just test the user APIs. To test admin properly we need an admin account.
                    // Let's create another user pending cancellation test. But we are good for basic flow.
                    console.log('ALL ORDER TESTS PASSED');
                    return [3 /*break*/, 12];
                case 11:
                    error_1 = _b.sent();
                    console.error('TEST FAILED:', error_1.message);
                    process.exit(1);
                    return [3 /*break*/, 12];
                case 12: return [2 /*return*/];
            }
        });
    });
}
test();
