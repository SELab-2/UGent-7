<script setup lang="ts">
import BaseLayout from '@/components/layout/BaseLayout.vue';
import {useRoute, useRouter} from 'vue-router';
import {useAuthStore} from '@/store/authentication.store.ts';
import {onMounted} from 'vue';
import Title from '@/components/Title.vue';

const { query } = useRoute();
const { push } = useRouter();
const { login, popIntent } = useAuthStore();

onMounted(async () => {
    await login(query.ticket as string).then(() => {
        push(popIntent());
    });
});
</script>

<template>
    <BaseLayout>
        <div class="w-8 mx-auto border-round surface-100 p-4">
            <Title>Inloggen</Title>
            <div class="flex align-items-center mt-3">
                <span class="mr-2">Je wordt zo meteen doorverwezen</span> <span class="pi pi-spin pi-spinner"/>
            </div>
        </div>
    </BaseLayout>
</template>

<style scoped lang="scss">

</style>