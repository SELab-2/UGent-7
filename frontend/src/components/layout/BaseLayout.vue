<script setup lang="ts">
import Header from '@/components/Header.vue';
import Body from '@/components/Body.vue';
import Footer from '@/components/Footer.vue';
</script>

<template>
    <div id="layout" class="w-12 lg:w-9 mx-auto">
        <Header/>

        <Body id="body">
            <slot/>
        </Body>

        <Footer/>
    </div>
</template>

<style scoped>
#layout {
    max-width: 1460px;

    #body {
        min-height: calc(100vh - (180 + 174));
    }
}
</style>