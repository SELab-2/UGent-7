import path from 'path';
import { defineConfig } from 'cypress';
import vitePreprocessor from 'cypress-vite';

const preprocessor = vitePreprocessor('./vite.config.ts');

export default defineConfig({
    e2e: {
        setupNodeEvents(on, config) {
            on('file:preprocessor',
                vitePreprocessor('./vite.config.ts')
            );
            on('before:run',
                () => {
                    preprocessor();
                    import('@/test/e2e/setup/seed.ts').then(async (module) => {
                        await module.seed();
                    });
                }
            );
            // on('task', {
            //     async 'db:seed'(seed) {
            //         await seed();
            //     }
            // });
        },
        baseUrl: 'https://nginx',
        specPattern: 'src/test/e2e/**/*.cy.{js,jsx,ts,tsx}',
        supportFile: 'src/test/e2e/setup/e2e.ts',
    },
});
