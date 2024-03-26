import axios from 'axios';
import {defineStore} from 'pinia';
import {User} from '@/types/User.ts';
import {endpoints} from '@/config/endpoints.ts';
import {ref} from 'vue';
import {useToastStore} from '@/store/toast.store.ts';

const INTENT_KEY = 'intent';

export const useAuthStore = defineStore('auth', {
    state: () => {
        return {
            user: ref<User|null>(null)
        };
    },
    actions: {
        /**
         * Attempt to log in the user by
         * 1. Using a CAS ticket if it is not null.
         * 2. Using a cookie if the ticket is null.
         *
         * @param ticket
         */
        async login(ticket: string|null = null) {
            // Display toast messages.
            const { add } = useToastStore();

            // Attempt to log in the user if the ticket is not null.
            if (ticket !== null) {
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
            }

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
            const intent = localStorage.getItem(INTENT_KEY) || '';
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