<script setup lang="ts">
import Header from '@/components/Header.vue';
import Body from '@/components/Body.vue';
import Footer from '@/components/Footer.vue';
</script>

<template>
    <div class="w-12 lg:w-8 mx-auto">
        <div class="grid gap-0">
            <div class="col-12">
                <Header/>
            </div>
            <div class="col-12">
                <Body>
                    <slot/>
                </Body>
            </div>
            <div class="col-12">
                <Footer/>
            </div>
        </div>
    </div>
</template>

<style scoped>

</style>