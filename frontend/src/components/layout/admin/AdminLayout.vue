<script setup lang="ts">
import Footer from '@/components/layout/Footer.vue';
import Body from '@/components/layout/Body.vue';
import AdminHeader from '@/components/layout/admin/AdminHeader.vue';
import AdminSidebar from '@/components/layout/admin/AdminSidebar.vue';
</script>

<template>
    <div id="layout" class="w-12 lg:w-9 mx-auto">
        <AdminHeader />

        <Body id="body">
            <div class="grid">
                <div class="w-3">
                    <AdminSidebar />
                </div>
                <div class="w-9">
                    <slot />
                </div>
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
