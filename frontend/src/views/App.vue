<script setup lang="ts">
import Toast from 'primevue/toast';
import {watch} from 'vue';
import {PrimeVueLocaleOptions, usePrimeVue} from 'primevue/config';
import {useI18n} from 'vue-i18n';
import {useToastStore} from '@/store/toast.store.ts';
import {useToast} from 'primevue/usetoast';
import {storeToRefs} from 'pinia';

/* Composables */
const { locale, messages } = useI18n();
const { config } = usePrimeVue();
const { add } = useToast();
const { message } = storeToRefs(useToastStore());

/* Set the PrimeVue locale when the locale changes */
watch(locale, () => {
    const translations = messages.value[locale.value]['primevue'];
    config.locale = translations as PrimeVueLocaleOptions;
}, { immediate: true });

/* Show a toast message when a new message is added */
watch(message, () => {
    if (message.value !== null) {
        add(message.value);
    }
});
</script>

<template>
    <Toast/>
    <RouterView/>
</template>

<style lang="scss">
@import '@/main.scss';
</style>