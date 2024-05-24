<script setup lang="ts">
import { PrimeIcons } from 'primevue/api';
/* Props */
defineProps<{
    href: string;
    title: string;
}>();
</script>

<template>
    <a class="surface-100 align-items-center p-3 flex gap-3 no-style" :href="href" download>
        <i :class="PrimeIcons.DOWNLOAD" class="text-primary text-xl" />
        {{ title }}
    </a>
</template>

<style scoped lang="scss"></style>
