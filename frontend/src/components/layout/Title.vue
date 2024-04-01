<script setup lang="ts">
withDefaults(defineProps<{ color?: 'primary' | 'contrast' }>(), {
    color: 'primary'
})
</script>

<template>
    <h1 class="title" :class="color">
        <slot />
    </h1>
</template>

<style lang="scss" scoped>
.title {
    margin-top: 0;
    color: var(--primary-color);
    position: relative;
    display: inline-block;

    &::after {
        content: '';
        position: absolute;
        left: 0;
        bottom: -14px;
        display: block;
        width: 100%;
        border-top: 4px solid var(--primary-color);
    }

    &.contrast {
        color: var(--primary-color-text);

        &::after {
            border-color: var(--primary-color-text);
        }
    }
}
</style>
