<script setup lang="ts">
import { useRoute } from 'vue-router';
</script>

<template>
    <h1>Unfinished Route: {{ useRoute().path }}</h1>
</template>
