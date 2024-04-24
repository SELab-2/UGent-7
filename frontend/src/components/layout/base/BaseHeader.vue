<script setup lang="ts">
import Header from '@/components/layout/Header.vue';
import { useI18n } from 'vue-i18n';
import { computed } from 'vue';

/* Composables */
const { t } = useI18n();

/* Navigation items */
const items = computed(() => [
    {
        icon: 'home',
        label: t('layout.header.navigation.dashboard'),
        route: 'dashboard',
    },
    {
        icon: 'calendar',
        label: t('layout.header.navigation.calendar'),
        route: 'calendar',
    },
    {
        icon: 'book',
        label: t('layout.header.navigation.courses'),
        route: 'courses',
    },
    {
        icon: 'bookmark',
        label: t('layout.header.navigation.projects'),
        route: 'projects',
    },
]);
</script>

<template>
    <Header :items="items" role-select />
</template>

<style lang="scss"></style>
