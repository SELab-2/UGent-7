import path from 'path';
import { defineConfig } from 'cypress';
import vitePreprocessor from 'cypress-vite';

import { seed } from '@/test/e2e/setup/seed.ts';

export default defineConfig({
    e2e: {
        setupNodeEvents(on, config) {
            on('file:preprocessor',
                vitePreprocessor('./vite.config.ts')
            );
            on('before:run',
                async (_) => {
                    await seed();
                }
            );
            // on('task', {
            //     async 'db:seed'() {
            //         // import { seed } from '@/test/e2e/setup/seed.ts';
            //         // import { client } from '@/config/axios.ts';
            //         await seed(client);
            //     }
            // });
        },
        baseUrl: 'https://nginx',
        specPattern: 'src/test/e2e/**/*.cy.{js,jsx,ts,tsx}',
        supportFile: 'src/test/e2e/setup/e2e.ts',
    },
});
