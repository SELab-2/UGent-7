<script setup lang="ts">
import AdminLayout from '@/components/layout/admin/AdminLayout.vue';
import Title from '@/components/layout/Title.vue';
import {useI18n} from 'vue-i18n';

const { t } = useI18n();
</script>

<template>
    <AdminLayout>
        <Title>
            {{ t('admin.users.title') }}
        </Title>
    </AdminLayout>
</template>

<style scoped lang="scss">

</style>