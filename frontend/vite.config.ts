import vue from '@vitejs/plugin-vue';
import { resolve } from 'path';
import { defineConfig } from 'vite';
import ViteRestart from 'vite-plugin-restart';

// https://vitejs.dev/config/
export default defineConfig({
    plugins: [
        vue(),
        ViteRestart({
            restart: [
              'trigger.txt',
            ],
          }),
    ],
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
    }
});
