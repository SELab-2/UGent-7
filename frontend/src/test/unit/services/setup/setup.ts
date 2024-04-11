import { afterAll, afterEach, beforeAll } from 'vitest';
import { setupServer } from 'msw/node';
import { createApp } from 'vue';
import { createPinia } from 'pinia';
import { JSDOM } from 'jsdom';

import { restHandlers } from './request_handlers';

const server = setupServer(...restHandlers);

beforeAll(() => {
    // throw an error when a request without a handler is encountered
    server.listen({ onUnhandledRequest: 'error' });

    // Set up jdom
    const dom = new JSDOM(`<div></div>`);
    global.document = dom.window.document;
    global.window = dom.window as unknown as Window & typeof globalThis;

    // Set up the app with pinia
    const pinia = createPinia();
    const app = createApp({
        template: '<p>App</p>',
    });
    app.use(pinia);
});

afterAll(() => {
    server.close();
});

afterEach(() => {
    server.resetHandlers();
});
