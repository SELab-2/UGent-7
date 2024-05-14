import { defineConfig } from 'cypress';

export default defineConfig({
    e2e: {
        baseUrl: 'https://nginx',
        specPattern: 'src/test/e2e/**/*.cy.{js,jsx,ts,tsx}',
    },
});
