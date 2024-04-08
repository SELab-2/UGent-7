import { defineConfig } from 'cypress';

export default defineConfig({
    e2e: {
        baseUrl: 'http://test_nginx',
        specPattern: 'src/test/e2e/**/*.cy.{js,jsx,ts,tsx}',
    },
});
