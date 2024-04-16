import App from '@/views/App.vue';
import router from '@/router/router';
import PrimeVue from 'primevue/config';
import ToastService from 'primevue/toastservice';
import ConfirmationService from 'primevue/confirmationservice';
import Ripple from 'primevue/ripple';
import Tooltip from 'primevue/tooltip';
import { i18n } from '@/config/i18n.ts';
import { createApp } from 'vue';
import { createPinia } from 'pinia';

/* Create the application */
// eslint-disable-next-line @typescript-eslint/no-unsafe-argument
const app = createApp(App);

/* Bind application plugins */
app.use(createPinia());
app.use(i18n);
app.use(router);
app.use(PrimeVue, { ripple: true });
app.use(ToastService);
app.use(ConfirmationService);

/* Bind app directives */
app.directive('ripple', Ripple);
app.directive('tooltip', Tooltip);


/* Mount the application */
app.mount('#app');
