import { defineConfig } from 'cypress';

export default defineConfig({
    e2e: {
        baseUrl: 'https://localhost',
        specPattern: 'src/test/e2e/**/*.cy.{js,jsx,ts,tsx}',
    },
});
