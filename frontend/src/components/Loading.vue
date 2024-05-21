<script setup lang="ts">
import ProgressSpinner from 'primevue/progressspinner';
import { useTimeout } from '@vueuse/core';

withDefaults(defineProps<{ height?: string }>(), {
    height: '4rem',
});

const show = useTimeout(250);
</script>

<template>
    <div :style="{ minHeight: height }" class="loader w-full p-3 flex justify-content-center">
        <ProgressSpinner stroke="blue" v-if="show" />
    </div>
</template>

<style scoped lang="scss"></style>
