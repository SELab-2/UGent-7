<script setup lang="ts">
import {useI18n} from 'vue-i18n';
import logoEN from '@/assets/img/logo-en.png';
import logoNL from '@/assets/img/logo-nl.png';

const { t, locale } = useI18n();

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
            <img class="w-full max-w-7rem" :src="locale == 'nl' ? logoNL : logoEN" :alt="t('layout.header.logo')">
        </div>
        <div class="flex flex-column w-full lg:w-10 border-x-1 border-200">
            <div id="header" class="w-full text-white p-4">
                <div class="text-right text-sm">
                    Ingelogd als Lander Maes
                </div>
            </div>
            <div id="navigation" class="w-full h-full flex border-bottom-1 border-200">
                <div class="flex align-items-center w-9rem flex justify-content-center p-3 border-right-1 border-200 cursor-pointer" v-for="item in items">
                    <span :class="'pi mr-3 pi-' + item.icon"/> {{ item.label }}
                </div>
            </div>
        </div>
    </div>
</template>

<style lang="scss" scoped>
@import '@/assets/scss/variables';

#header {
    background: $blue;
}
</style>