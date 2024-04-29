<script setup lang="ts">
import Title from '@/components/layout/Title.vue';
import BaseLayout from '@/components/layout/base/BaseLayout.vue';
</script>

<template>
    <BaseLayout>
        <div class="grid">
            <div class="col-6 md:col-4 m-3">
                <div>
                    <Title>Status</Title>
                </div>
                <div>
                    <Title>File(s)</Title>
                </div>
            </div>
            <div class="col-8 md:col-6">
                <Title>File(s)</Title>
            </div>
        </div>
    </BaseLayout>
</template>

<style scoped lang="scss">

</style>