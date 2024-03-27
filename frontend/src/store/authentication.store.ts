import axios from 'axios';
import {defineStore} from 'pinia';
import {User} from '@/types/User.ts';
import {endpoints} from '@/config/endpoints.ts';
import {ref} from 'vue';
import {useToastStore} from '@/store/toast.store.ts';
import {client} from '@/composables/axios.ts';

const INTENT_KEY = 'intent';

export const useAuthStore = defineStore('auth', {
    state: () => {
        return {
            user: ref<User|null>(null)
        };
    },
    actions: {
        /**
         * Attempt to log in the user using a CAS ticket.
         *
         * @param ticket
         */
        async login(ticket: string) {
            // Display toast messages.
            const { add } = useToastStore();

            // Attempt to log in the user using the ticket.
            await axios.post(endpoints.auth.token.obtain, {
                ticket
            }).then(() => {
                add({
                    severity: 'success',
                    summary: 'Success',
                    detail: 'You have successfully logged in.'
                })
            }).catch((error) => {
                add({
                    severity: 'error',
                    summary: error.response.statusText,
                    detail: error.response.data.detail
                });
            });
        },
        /**
         * Refresh the user objects in the API endpoint.
         */
        async refresh() {
            // Display toast messages.
            const { add } = useToastStore();

            // Get the user information (using a cookie).
            await axios.get(endpoints.auth.whoami).then(response => {
                this.user = User.fromJSON(response.data);
            }).catch((error) => {
                add({
                    severity: 'error',
                    summary: error.response.statusText,
                    detail: error.response.data.detail
                });
            });
        },
        async logout() {
            await client.post(endpoints.auth.logout).catch();
            this.user = null;
        },
        /**
         * Save the intent URL in the local storage.
         *
         * @param intent
         */
        pushIntent(intent: string): void {
            localStorage.setItem(INTENT_KEY, intent);
        },
        /**
         * Get the intent URL from the local storage.
         *
         * @return string
         */
        popIntent(): string {
            const intent = localStorage.getItem(INTENT_KEY) || '/';
            localStorage.removeItem(INTENT_KEY);
            return intent;
        }
    },
    getters: {
        /**
         * Check if the user is authenticated.
         *
         * @param state
         */
        isAuthenticated(state): boolean {
            return state.user !== null;
        }
    }
});