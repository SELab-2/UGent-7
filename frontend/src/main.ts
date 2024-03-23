import nl from '@/assets/lang/nl.json';
import en from '@/assets/lang/en.json';
import App from '@/views/App.vue';
import PrimeVue from 'primevue/config';
import Ripple from 'primevue/ripple';
import {createApp} from 'vue';
import {createI18n} from 'vue-i18n';
import router from './router/router';
import {createPinia} from 'pinia';

const app = createApp(App);

/* Bind application plugins */

app.use(createPinia());

app.use(createI18n({
    locale: 'nl',
    fallbackLocale: 'en',
    legacy: false,
    messages: { en, nl }
}));

app.use(router)

app.use(PrimeVue, {
    ripple: true
});

/* Bind app directives */

app.directive('ripple', Ripple);

/* Mount the application */
app.mount('#app');