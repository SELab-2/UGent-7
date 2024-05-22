<script setup lang="ts">
import Header from '@/views/layout/base/BaseHeader.vue';
import Body from '@/views/layout/Body.vue';
import Footer from '@/views/layout/Footer.vue';
</script>

<template>
    <div id="layout" class="w-12 lg:w-11 xl:w-9 mx-auto">
        <Header />

        <Body id="body">
            <slot />
        </Body>

        <Footer />
    </div>
</template>

<style scoped>
#layout {
    max-width: 1460px;
    height: 100vh;

    #body {
        min-height: calc(100vh - (180px + 175px));
    }
}
</style>
