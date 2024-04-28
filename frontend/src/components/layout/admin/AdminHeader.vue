<script setup lang="ts">
import Header from '@/components/layout/Header.vue';
import { useI18n } from 'vue-i18n';
import { computed } from 'vue';

/* Composables */
const { t } = useI18n();

/* Navigation items */
const items = computed(() => [
    {
        label: t('admin.users.title'),
        route: 'admin-users',
    },
]);
</script>

<template>
    <Header :items="items" />
</template>

<style lang="scss"></style>
