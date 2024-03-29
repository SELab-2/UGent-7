import App from '@/views/App.vue';
import router from '@/router/router';
import PrimeVue from 'primevue/config';
import ToastService from 'primevue/toastservice';
import Ripple from 'primevue/ripple';
import {i18n} from '@/composables/i18n';
import {createApp} from 'vue';
import {createPinia} from 'pinia';

const app = createApp(App);

/* Bind application plugins */
app.use(createPinia());

app.use(ToastService);

app.use(i18n);

app.use(router)

app.use(PrimeVue, {
    ripple: true
});

/* Bind app directives */
app.directive('ripple', Ripple);

/* Mount the application */
app.mount('#app');