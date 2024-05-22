<script setup lang="ts">
import en from '@/assets/img/logo-en.png';
import nl from '@/assets/img/logo-nl.png';
import { useI18n } from 'vue-i18n';

/* Translation composable */
const { t, locale } = useI18n();

/* Available localized images */
const logo: Record<string, string> = { nl, en };
</script>

<template>
    <div id="footer" class="p-6 py-4 mt-auto text-md">
        <div class="w-full flex flex-column md:flex-row justify-content-between align-items-center gap-4 py-3">
            <!-- Logo -->
            <img class="w-full max-w-9rem" :src="logo[locale]" :alt="t('layout.header.logo')" />

            <div class="flex flex-column gap-3 justify-content-center">
                <!-- Links and Company Info -->
                <div class="flex flex-column md:flex-row align-items-center gap-3">
                    <a class="text-md">{{ t('layout.footer.home') }}</a>
                    <a class="text-md">{{ t('layout.footer.about') }}</a>
                    <a class="text-md">{{ t('layout.footer.contact') }}</a>
                    <a class="text-md">{{ t('layout.footer.privacy') }}</a>
                </div>

                <!-- Social Media Icons -->
                <div class="flex align-items-center text-primary gap-3">
                    <a class="text-md text-primary">
                        <i class="pi pi-discord"></i>
                    </a>
                    <a class="text-md text-primary" href="https://github.com/tyboro2002">
                        <i class="pi pi-github"></i>
                    </a>
                    <a class="text-md text-primary" href="https://paypal.me/ewiev">
                        <i class="pi pi-paypal"></i>
                    </a>
                    <a class="text-md text-primary" href="https://www.facebook.com/profile.php?id=100015599597182">
                        <i class="pi pi-facebook"></i>
                    </a>
                    <a class="text-md text-primary">
                        <i class="pi pi-twitter"></i>
                    </a>
                    <a class="text-md text-primary">
                        <i class="pi pi-instagram"></i>
                    </a>
                    <a class="text-md text-primary" href="https://www.linkedin.com/in/vincent-vallaeys-855637309/">
                        <i class="pi pi-linkedin"></i>
                    </a>
                </div>
            </div>
        </div>
    </div>
    <div class="text-center p-2 text-sm surface-100">
        <span>&copy; {{ new Date().getFullYear() }} Ypovoli. {{ t('layout.footer.rights') }}</span>
    </div>
</template>

<style lang="scss" scoped>
#footer {
    background: var(--primary-color-light);
}
</style>
