<script setup lang="ts">
import Button from 'primevue/button';
import BaseLayout from '@/components/layout/BaseLayout.vue';
import {PrimeIcons} from 'primevue/api';
</script>

<template>
    <BaseLayout>
        <h1>
            Hier komt een mooie titel
        </h1>
        <p class="w-12 lg:w-6">
            Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec pulvinar sed mauris id cursus. Vivamus pretium laoreet quam,
            ac pulvinar magna ultricies id. Donec ullamcorper aliquam leo quis malesuada.
        </p>
        <Button :icon="PrimeIcons.ARROW_RIGHT" icon-pos="right" label="Hellaur" class="mt-3"></Button>
    </BaseLayout>
</template>

<style scoped>

</style>