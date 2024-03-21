import { defineConfig } from 'vite'
import { resolve } from 'path';
import vue from '@vitejs/plugin-vue';

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
        hmr: {
            port: 5174
        }
    }
});
