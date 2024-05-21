import { defineConfig } from 'cypress';
import { client } from '@/config/axios.ts';
import { seed } from '@/test/e2e/setup/seed.ts';

export default defineConfig({
    e2e: {
        setupNodeEvents(on, config) {
            on('task', {
                async 'db:seed'() {
                    await seed(client);
                }
            })
        },
        baseUrl: 'https://localhost',
        specPattern: 'src/test/e2e/**/*.cy.{js,jsx,ts,tsx}',
        supportFile: 'src/test/e2e/setup/e2e.ts',
    },
});
