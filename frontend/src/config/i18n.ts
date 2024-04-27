import 'moment/dist/locale/nl';
import AppNL from '@/assets/lang/app/nl.json';
import AppEN from '@/assets/lang/app/en.json';
import InfoNL from '@/assets/lang/info/nl.json';
import InfoEN from '@/assets/lang/info/en.json';
import { createI18n } from 'vue-i18n';
import { useLocalStorage } from '@vueuse/core';

const localeStorage = useLocalStorage('locale', 'nl');

export const i18n = createI18n({
    locale: localeStorage.value,
    fallbackLocale: 'en',
    legacy: false,
    messages: {
        en: {
            ...AppEN,
            info: InfoEN,
        },
        nl: {
            ...AppNL,
            info: InfoNL,
        },
    },
});
