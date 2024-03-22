<script setup lang="ts">
import BaseLayout from '@/components/layout/BaseLayout.vue';
import Title from '@/components/Title.vue';
import {useI18n} from 'vue-i18n';


const { t } = useI18n();

</script>

<template>
    <BaseLayout>
        <!-- Calendar heading -->
        <div class="flex justify-content-between align-items-center mb-6">
            <!--Calender title -->
            <Title class="m-0">{{ t('views.calendar.title') }}</Title>
        </div>
    </BaseLayout>
</template>

<style scoped lang="scss">

</style>