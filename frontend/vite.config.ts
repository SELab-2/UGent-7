/// <reference types="vitest" />
import vue from '@vitejs/plugin-vue';
import { resolve } from 'path';
import { defineConfig } from 'vite';

// https://vitejs.dev/config/
export default defineConfig({
    plugins: [vue()],
    resolve: {
        alias: {
            'font': resolve(__dirname, './src/assets/scss/theme/font'),
            '@': resolve(__dirname, './src')
        }
    },
    server: {
        host: '0.0.0.0',
        port: 5173,
        proxy: {
            '/hmr': {
                target: 'ws://localhost:5173',
                ws: true
            },
        },
        hmr: {
            path: "/hmr",
            port: 443
        }
    },
    test: {
        setupFiles: "./src/test/unit/setup.ts"
    }
});
