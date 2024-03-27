import axios from 'axios';
import Cookie from 'js-cookie';
import { i18n } from '@/composables/i18n';

const { locale } = i18n.global;

axios.defaults.xsrfHeaderName = "X-CSRFToken";
axios.defaults.xsrfCookieName = "csrftoken";

export const client = axios.create({
    headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'X-CSRFToken': Cookie.get('csrftoken'),
        'Accept-Language': locale.value
    },
    withCredentials: true,
    xsrfHeaderName: "X-CSRFToken",
    xsrfCookieName: "csrftoken"
});