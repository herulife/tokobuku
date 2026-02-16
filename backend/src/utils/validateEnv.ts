import logger from './logger';

const requiredEnvVars = [
    'DATABASE_URL',
    'JWT_SECRET',
    'PORT',
    'CLIENT_URL',
];

export const validateEnv = (): void => {
    const missingVars: string[] = [];

    requiredEnvVars.forEach((varName) => {
        if (!process.env[varName]) {
            missingVars.push(varName);
        }
    });

    if (missingVars.length > 0) {
        const errorMsg = `Missing required environment variables: ${missingVars.join(', ')}`;
        logger.error(errorMsg);
        console.error(`\n❌ ${errorMsg}\n`);
        console.error('Please check your .env file and ensure all required variables are set.\n');
        process.exit(1);
    }

    // Validate JWT_SECRET strength (at least 32 characters)
    const jwtSecret = process.env.JWT_SECRET as string;
    if (jwtSecret.length < 32) {
        const warningMsg = 'JWT_SECRET should be at least 32 characters for security';
        logger.warn(warningMsg);
        console.warn(`\n⚠️  ${warningMsg}\n`);
    }

    logger.info('Environment variables validated successfully');
};
