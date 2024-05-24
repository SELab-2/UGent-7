<script setup lang="ts">
import Footer from '@/views/layout/Footer.vue';
import Body from '@/views/layout/Body.vue';
import AdminHeader from '@/views/layout/admin/AdminHeader.vue';
</script>

<template>
    <div id="layout" class="w-12 lg:w-9 mx-auto">
        <AdminHeader />

        <Body id="body">
            <div class="grid">
                <slot />
            </div>
        </Body>

        <Footer />
    </div>
</template>

<style scoped lang="scss">
#layout {
    max-width: 1460px;

    #body {
        min-height: calc(100vh - (170px));
    }
}
</style>
