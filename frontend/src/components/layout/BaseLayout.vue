<script setup lang="ts">
import Header from '@/components/Header.vue';
import Body from '@/components/Body.vue';
import Footer from '@/components/Footer.vue';
</script>

<template>
    <div class="w-12 lg:w-9 mx-auto">
        <Header/>

        <Body>
            <slot/>
        </Body>

        <Footer/>
    </div>
</template>

<style scoped>

</style>