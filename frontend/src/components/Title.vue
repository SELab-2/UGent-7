<script setup lang="ts">

</script>

<template>
    <h1 class="title">
        <slot/>
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
        bottom: -8px;
        display: block;
        width: 100%;
        border-top: 4px solid var(--primary-color);;
    }
}
</style>