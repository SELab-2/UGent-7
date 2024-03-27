import 'moment/dist/locale/nl';
import en from '@/assets/lang/en.json';
import nl from '@/assets/lang/nl.json';
import {createI18n} from 'vue-i18n';

export const i18n = createI18n({
    locale: 'nl',
    fallbackLocale: 'en',
    legacy: false,
    messages: { en, nl }
});