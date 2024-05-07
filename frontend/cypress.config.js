import { defineConfig } from 'cypress';

export default defineConfig({
    e2e: {
        baseUrl: 'http://nginx',
        specPattern: 'src/test/e2e/**/*.cy.{js,jsx,ts,tsx}',
    },
});
