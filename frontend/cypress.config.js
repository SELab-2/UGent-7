import { defineConfig } from 'cypress';
import vitePreprocessor from 'cypress-vite';

export default defineConfig({
    e2e: {
        setupNodeEvents(on, config) {
            on('file:preprocessor',
                vitePreprocessor('./vite.config.ts')
            );
        },
        baseUrl: 'https://nginx',
        specPattern: 'src/test/e2e/**/*.cy.{js,jsx,ts,tsx}',
    },
});
