import { defineConfig } from 'cypress';
import task from '@cypress/code-coverage/task';

export default defineConfig({
    e2e: {
        setupNodeEvents(on, config) {
            task(on, config);
            // include any other plugins code...

            return config;
        },
        baseUrl: 'https://localhost',
        specPattern: 'src/test/e2e/**/*.cy.{js,jsx,ts,tsx}',
    },
});
