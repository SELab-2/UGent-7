<script setup lang="ts">
import {useI18n} from 'vue-i18n';
import en from '@/assets/img/logo-en.png';
import nl from '@/assets/img/logo-nl.png';

const { t, locale } = useI18n();

const logo: {[key: string]: string} = {nl, en};

const items = [
    {icon: 'home', label: t('layout.header.navigation.dashboard'), path: ''},
    {icon: 'calendar', label: t('layout.header.navigation.calendar'), path: ''},
    {icon: 'book', label: t('layout.header.navigation.courses'), path: ''},
    {icon: 'cog', label: t('layout.header.navigation.settings'), path: ''},
    {icon: 'info-circle', label: t('layout.header.navigation.help'), path: ''}
];
</script>

<template>
    <div class="flex w-full">
        <div class="w-full lg:w-2 flex align-items-center px-4 py-3">
            <img class="w-full max-w-7rem" :src="logo[locale]" :alt="t('layout.header.logo')">
        </div>
        <div class="flex flex-column w-full lg:w-10 border-x-1 border-200">
            <div id="header" class="w-full text-white p-4">
                <div class="text-right text-sm">
                    Ingelogd als Lander Maes
                </div>
            </div>
            <div id="navigation" class="w-full h-full flex border-bottom-1 border-200">
                <div class="flex align-items-center w-9rem flex justify-content-center p-3 border-right-1 border-200 cursor-pointer text-primary font-bold" v-for="item in items">
                    <span :class="'pi mr-2 pi-' + item.icon"/> {{ item.label }}
                </div>
            </div>
        </div>
    </div>
</template>

<style lang="scss" scoped>
#header {
    background: var(--primary-color);
}
</style>