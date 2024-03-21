<script setup lang="ts">
import enLogo from '@/assets/img/logo-white-en.png';
import nlLogo from '@/assets/img/logo-white-nl.png';
import {useI18n} from 'vue-i18n';

/* Translation composable */
const { t, locale } = useI18n();

/* Available localized images */
const logo: {[key: string]: string} = { nl: nlLogo, en: enLogo };
</script>

<template>
    <div id="footer" class="p-4 py-3">
        <div class="w-full lg:w-2 flex align-items-center py-3">
            <img class="w-full max-w-9rem" :src="logo[locale]" :alt="t('layout.header.logo')">
        </div>
    </div>
</template>

<style lang="scss" scoped>
#footer {
    background: var(--primary-color);
}
</style>