<script setup lang="ts">
import Button from 'primevue/button';
import BaseLayout from '@/components/layout/BaseLayout.vue';
import {PrimeIcons} from 'primevue/api';
import Title from '@/components/Title.vue';
</script>

<template>
    <BaseLayout>
        <Title>
            Hier komt een mooie titel
        </Title>
        <p class="w-12 lg:w-6">
            Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec pulvinar sed mauris id cursus. Vivamus pretium laoreet quam,
            ac pulvinar magna ultricies id. Donec ullamcorper aliquam leo quis malesuada.
        </p>
        <Button :icon="PrimeIcons.ARROW_RIGHT" icon-pos="right" label="Hellaur" class="mt-3" :rounded="false"></Button>
        <Button severity="secondary" :icon="PrimeIcons.ARROW_RIGHT" icon-pos="right" label="Hellaur" class="mt-3" :rounded="false"></Button>
    </BaseLayout>
</template>

<style scoped>

</style>