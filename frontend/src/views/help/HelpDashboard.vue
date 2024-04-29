<script setup lang="ts">
import HelpBaseLayout from '@/components/help/HelpBaseLayout.vue';
import Button from 'primevue/button';
import { RouterLink } from 'vue-router';
//TODO add menu

const items = [
  { label: 'Home', route: 'help-student' },
  { label: 'About', route: 'help-teacher' },
  // Add more sidebar items as needed
];
</script>

<template>
    <HelpBaseLayout>
        <div>
            
        </div>
    </HelpBaseLayout>
</template>

<style scoped></style>