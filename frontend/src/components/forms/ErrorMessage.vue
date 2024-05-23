<script setup lang="ts">
import Message from 'primevue/message';

/* Props */
defineProps<{ field: any }>();
</script>

<template>
    <Message severity="warn" v-if="field.$error" :closable="false">
        {{ field.$errors[0].$message }}
    </Message>
</template>

<style scoped lang="scss">
.p-error {
    display: block;
}
</style>
