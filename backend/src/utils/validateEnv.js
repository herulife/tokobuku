"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.validateEnv = void 0;
var logger_1 = require("./logger");
var requiredEnvVars = [
    'DATABASE_URL',
    'JWT_SECRET',
    'PORT',
    'CLIENT_URL',
];
var validateEnv = function () {
    var missingVars = [];
    requiredEnvVars.forEach(function (varName) {
        if (!process.env[varName]) {
            missingVars.push(varName);
        }
    });
    if (missingVars.length > 0) {
        var errorMsg = "Missing required environment variables: ".concat(missingVars.join(', '));
        logger_1.default.error(errorMsg);
        console.error("\n\u274C ".concat(errorMsg, "\n"));
        console.error('Please check your .env file and ensure all required variables are set.\n');
        process.exit(1);
    }
    // Validate JWT_SECRET strength (at least 32 characters)
    var jwtSecret = process.env.JWT_SECRET;
    if (jwtSecret.length < 32) {
        var warningMsg = 'JWT_SECRET should be at least 32 characters for security';
        logger_1.default.warn(warningMsg);
        console.warn("\n\u26A0\uFE0F  ".concat(warningMsg, "\n"));
    }
    logger_1.default.info('Environment variables validated successfully');
};
exports.validateEnv = validateEnv;
