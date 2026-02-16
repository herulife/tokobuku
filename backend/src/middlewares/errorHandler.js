"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.errorHandler = void 0;
var logger_1 = require("../utils/logger");
var errorHandler = function (err, req, res, next) {
    err.statusCode = err.statusCode || 500;
    err.status = err.status || 'error';
    // Log all errors
    logger_1.default.error("".concat(err.statusCode, " - ").concat(err.message), {
        method: req.method,
        url: req.originalUrl,
        ip: req.ip,
        stack: err.stack,
        error: err.name
    });
    if (process.env.NODE_ENV === 'development') {
        res.status(err.statusCode).json({
            status: err.status,
            error: err,
            message: err.message,
            stack: err.stack,
        });
    }
    else {
        if (err.isOperational) {
            res.status(err.statusCode).json({
                status: err.status,
                message: err.message,
            });
        }
        else {
            // Programming or unknown error: don't leak details
            logger_1.default.error('UNEXPECTED ERROR 💥', { error: err });
            res.status(500).json({
                status: 'error',
                message: 'Something went very wrong!',
            });
        }
    }
};
exports.errorHandler = errorHandler;
