import axios from 'axios';
import Cookie from 'js-cookie';
import { i18n } from '@/config/i18n.ts';

const { locale } = i18n.global;

axios.defaults.xsrfHeaderName = 'X-CSRFToken';
axios.defaults.xsrfCookieName = 'csrftoken';

// Todo: wrap with setupCache.
export const client = axios.create({
    headers: {
        'Content-Type': 'application/json',
        Accept: 'application/json',
        'X-CSRFToken': Cookie.get('csrftoken'),
        'Accept-Language': locale.value,
    },
    withCredentials: true,
    xsrfHeaderName: 'X-CSRFToken',
    xsrfCookieName: 'csrftoken',
});
