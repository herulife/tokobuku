"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.asyncHandler = void 0;
var asyncHandler = function (fn) {
    return function (req, res, next) {
        fn(req, res, next).catch(next);
    };
};
exports.asyncHandler = asyncHandler;
