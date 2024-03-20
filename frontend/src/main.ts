import nl from '@/assets/lang/nl.json';
import en from '@/assets/lang/en.json';
import App from '@/views/App.vue';
import {createApp} from 'vue';
import {createI18n} from 'vue-i18n';
import {routes} from '@/router/routes.ts';
import {createPinia} from 'pinia';
import {createRouter, createWebHistory} from 'vue-router';

const app = createApp(App);

/* Bind application plugins */

app.use(createPinia());

app.use(createI18n({
    locale: 'nl',
    fallbackLocale: 'en',
    legacy: false,
    messages: { en, nl }
}));

app.use(createRouter({
    history: createWebHistory(), routes
}));

/* Mount the application */
app.mount('#app');