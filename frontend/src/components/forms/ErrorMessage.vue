<script setup lang="ts">
/* Props */
const props = defineProps<{ field: any }>();
</script>

<template>
    <span v-if="props.field.$error" class="p-error">{{ props.field.$errors[0].$message }}</span>
</template>

<style scoped lang="scss">
.p-error {
    display: block;
}
</style>
