<script setup lang="ts">
import Header from '@/components/layout/Header.vue';
import Body from '@/components/layout/Body.vue';
import Footer from '@/components/layout/Footer.vue';
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

    #body {
        min-height: calc(100vh - (180px + 175px));
    }
}
</style>
